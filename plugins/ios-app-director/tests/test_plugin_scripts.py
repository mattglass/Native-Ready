from __future__ import annotations

import importlib.util
import json
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace


PLUGIN_ROOT = Path(__file__).resolve().parents[1]


def load_script(module_name: str, relative_path: str) -> ModuleType:
    path = PLUGIN_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


baton = load_script(
    "ready_validate_baton",
    "skills/ios-app-director/scripts/validate_baton_frontmatter.py",
)
feature_map = load_script(
    "ready_replace_feature_map",
    "skills/ios-feature-map/scripts/replace_app_feature_inventory.py",
)
native_scaffold = load_script(
    "ready_native_scaffold",
    "skills/ios-native-scaffold/scripts/render_ios_native_scaffold.py",
)
intake_manifest = load_script(
    "ready_intake_manifest",
    "skills/stitch-ios-intake/scripts/build_intake_manifest.py",
)
image_assets = load_script(
    "ready_image_assets",
    "skills/stitch-ios-intake/scripts/extract_stitch_image_assets.py",
)
screen_artifacts = load_script(
    "ready_screen_artifacts",
    "skills/stitch-ios-intake/scripts/save_stitch_screen_artifacts.py",
)
stitch_operations = load_script(
    "ready_stitch_operations",
    "skills/stitch-ios-concept-builder/scripts/stitch_operation_journal.py",
)
bootstrap_receipt = load_script(
    "ready_bootstrap_receipt",
    "skills/ios-app-bootstrap/scripts/render_bootstrap_receipt.py",
)
template_deployer = load_script(
    "ready_template_deployer",
    "skills/ios-app-bootstrap/scripts/deploy_ready_template.py",
)


def baton_text(platform: str = "iPhone and iPad") -> str:
    return f"""---
platform: {platform}
roadmap_task: APP-001
task_type: native_scaffold
feature: app-shell
screen: App shell
mode: native
device: universal
app_maturity: prototype
destination: SoccerQuestApp/SoccerQuest/
validation_tier: tier1_compile
regression_scope: none
evidence_expectation: standard
---

Create the native app shell.
"""


class BatonValidatorTests(unittest.TestCase):
    def validate_text(self, text: str, *, allow_placeholders: bool = False):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "next-prompt.md"
            path.write_text(text, encoding="utf-8")
            return baton.validate(path, allow_placeholders=allow_placeholders)

    def test_accepts_bootstrapped_baton(self) -> None:
        errors, warnings, fields = self.validate_text(baton_text())
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(fields["platform"], "iPhone and iPad")

    def test_rejects_unresolved_template_placeholder_by_default(self) -> None:
        errors, _, _ = self.validate_text(baton_text('"[PRIMARY_PLATFORM]"'))
        self.assertTrue(any("unresolved template placeholder" in error for error in errors))

    def test_allows_placeholder_only_when_explicitly_requested(self) -> None:
        errors, _, fields = self.validate_text(
            baton_text('"[PRIMARY_PLATFORM]"'),
            allow_placeholders=True,
        )
        self.assertEqual(errors, [])
        self.assertEqual(fields["platform"], "[PRIMARY_PLATFORM]")


class FeatureMapTests(unittest.TestCase):
    def test_replaces_section_nine_and_preserves_following_sections(self) -> None:
        app_text = "# App\n\n## 9. App Feature Inventory & Requirements Map\n\nOld\n\n## 10. Notes\n\nKeep\n"
        result = feature_map.replace_section(app_text, "New inventory")
        self.assertIn("## 9. App Feature Inventory & Requirements Map\n\nNew inventory", result)
        self.assertNotIn("Old", result)
        self.assertIn("## 10. Notes\n\nKeep", result)


class NativeScaffoldHelperTests(unittest.TestCase):
    def test_derives_safe_native_names(self) -> None:
        self.assertEqual(native_scaffold.pascal_identifier("Soccer Quest Kids"), "SoccerQuestKids")
        self.assertEqual(native_scaffold.bundle_slug("Soccer Quest Kids"), "soccerquestkids")

    def test_rejects_generic_target(self) -> None:
        with self.assertRaises(ValueError):
            native_scaffold.pascal_identifier("My App")

    def test_scaffold_records_app_derived_test_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / ".stitch").mkdir()
            (root / "docs").mkdir()
            (root / ".stitch" / "metadata.json").write_text(
                json.dumps({"app": {}, "riskRegister": []}), encoding="utf-8"
            )
            (root / "AGENTS.md").write_text(
                "- Main app target: `[MAIN_TARGET_NAME]`\n"
                "- Test target: `[TEST_TARGET_NAME]`\n",
                encoding="utf-8",
            )
            result = native_scaffold.create_scaffold(
                SimpleNamespace(
                    repo_root=str(root),
                    app_name="Kitty Keeper",
                    target_name="",
                    bundle_id="",
                    platform="iphone-and-ipad",
                    deployment_target=native_scaffold.DEFAULT_DEPLOYMENT_TARGET,
                    force=False,
                ),
                xcode_version_output="Xcode 16.4\nBuild version 16F6",
            )
            metadata = json.loads((root / ".stitch" / "metadata.json").read_text())
            project = (
                root
                / "KittyKeeperApp"
                / "KittyKeeper.xcodeproj"
                / "project.pbxproj"
            ).read_text(encoding="utf-8")
            app_icon = json.loads(
                (
                    root
                    / "KittyKeeperApp"
                    / "KittyKeeper"
                    / "Assets.xcassets"
                    / "AppIcon.appiconset"
                    / "Contents.json"
                ).read_text(encoding="utf-8")
            )
            app_view_model = (
                root / "KittyKeeperApp" / "KittyKeeper" / "AppViewModel.swift"
            ).read_text(encoding="utf-8")
            self.assertEqual(result["plannedTestTarget"], "KittyKeeperTests")
            self.assertEqual(result["xcodeVersion"], "16.4")
            self.assertEqual(metadata["app"]["nativeTestTarget"], "KittyKeeperTests")
            self.assertEqual(metadata["nativeScaffold"]["minimumXcodeMajor"], 16)
            self.assertEqual(metadata["nativeScaffold"]["swiftLanguageMode"], "6.0")
            self.assertEqual(metadata["nativeScaffold"]["deploymentTarget"], "18.0")
            self.assertEqual(metadata["setupRun"]["toolchainStatus"], "supported")
            self.assertIn("KittyKeeperTests", (root / "AGENTS.md").read_text())
            self.assertIn("objectVersion = 77;", project)
            self.assertIn("CreatedOnToolsVersion = 16.0;", project)
            self.assertIn("PBXFileSystemSynchronizedRootGroup", project)
            self.assertIn("fileSystemSynchronizedGroups", project)
            self.assertIn("IPHONEOS_DEPLOYMENT_TARGET = 18.0;", project)
            self.assertIn("SWIFT_VERSION = 6.0;", project)
            self.assertNotIn("SWIFT_VERSION = 5.0;", project)
            self.assertIn("@MainActor", app_view_model)
            self.assertEqual(len(app_icon["images"]), 3)
            self.assertEqual(app_icon["images"][0]["idiom"], "universal")

    def test_scaffold_rejects_xcode_15_before_writing_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            with self.assertRaisesRegex(RuntimeError, "Unsupported Xcode 15.2"):
                native_scaffold.create_scaffold(
                    SimpleNamespace(
                        repo_root=str(root),
                        app_name="Kitty Keeper",
                        target_name="",
                        bundle_id="",
                        platform="iphone-and-ipad",
                        deployment_target=native_scaffold.DEFAULT_DEPLOYMENT_TARGET,
                        force=False,
                    ),
                    xcode_version_output="Xcode 15.2\nBuild version 15C500b",
                )
            self.assertFalse((root / "KittyKeeperApp").exists())


class IntakeManifestTests(unittest.TestCase):
    def test_builds_manifest_from_local_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo_root = Path(temporary_directory)
            html_dir = repo_root / ".stitch" / "intake" / "html"
            screenshot_dir = repo_root / ".stitch" / "intake" / "screenshots"
            html_dir.mkdir(parents=True)
            screenshot_dir.mkdir(parents=True)
            (html_dir / "home.html").write_text(
                "<html><head><title>Home Screen</title></head></html>",
                encoding="utf-8",
            )
            png = b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR" + struct.pack(">II", 390, 844)
            (screenshot_dir / "home.png").write_bytes(png)

            manifest = intake_manifest.build_manifest(repo_root)

            self.assertEqual(manifest["counts"], {"html": 1, "screenshots": 1})
            html_record = next(item for item in manifest["artifacts"] if item["category"] == "html")
            image_record = next(item for item in manifest["artifacts"] if item["category"] == "screenshots")
            self.assertEqual(html_record["title"], "Home Screen")
            self.assertEqual(image_record["dimensions"], {"width": 390, "height": 844})


class ImageAssetTests(unittest.TestCase):
    def test_parses_only_remote_image_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "screen.html"
            path.write_text(
                "<html><head><title>Skills</title></head><body>"
                '<img src="https://example.com/ball.png" alt="Soccer ball">'
                '<img src="local.png" alt="Local">'
                "</body></html>",
                encoding="utf-8",
            )
            title, images = image_assets.parse_html(path)
            self.assertEqual(title, "Skills")
            self.assertEqual(len(images), 1)
            self.assertEqual(images[0]["alt"], "Soccer ball")

    def test_identifies_png_data(self) -> None:
        media_type, extension = image_assets.image_type(b"\x89PNG\r\n\x1a\ncontent", None)
        self.assertEqual((media_type, extension), ("image/png", ".png"))


class ScreenArtifactTests(unittest.TestCase):
    def test_normalizes_slug_and_loads_queue(self) -> None:
        self.assertEqual(screen_artifacts.safe_slug("  Level One!  "), "level-one")
        with tempfile.TemporaryDirectory() as temporary_directory:
            queue = Path(temporary_directory) / "queue.json"
            queue.write_text(json.dumps({"artifacts": [{"slug": "home"}]}), encoding="utf-8")
            self.assertEqual(screen_artifacts.load_queue(queue), [{"slug": "home"}])

    def test_rejects_invalid_artifact_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "bad.png"
            path.write_bytes(b"not a png")
            with self.assertRaises(RuntimeError):
                screen_artifacts.validate_png(path)


class StitchOperationJournalTests(unittest.TestCase):
    def journal(self, max_replacement_attempts=1, replacement_mode="autonomous"):
        journal = stitch_operations.new_journal(
            "setup-001",
            "Example App Concepts",
            required_capabilities=["stitch"],
            optional_capabilities=["cloudflare"],
            max_replacement_attempts=max_replacement_attempts,
            replacement_mode=replacement_mode,
        )
        stitch_operations.adopt_project(
            journal,
            "project-123",
            "created_current_run",
            "Example App Concepts",
        )
        return journal

    def prepare(
        self,
        journal,
        operation_id="welcome-001",
        screen_role="welcome",
        prompt="Generate the welcome screen.",
        requested_screen_roles=None,
        replacement_for=None,
    ):
        return stitch_operations.prepare_operation(
            journal,
            operation_id,
            "generate_screen",
            "project-123",
            screen_role,
            ["existing-screen"],
            replacement_for=replacement_for,
            prompt=prompt,
            requested_screen_roles=requested_screen_roles,
        )

    def reconcile_timeout(self, journal, operation_id="welcome-001"):
        stitch_operations.transition_operation(
            journal,
            operation_id,
            "polling",
            failure_class="timeout_or_connection",
        )
        stitch_operations.transition_operation(
            journal,
            operation_id,
            "ambiguous_timeout",
        )
        return stitch_operations.record_final_reconciliation(
            journal,
            operation_id,
            ["existing-screen"],
            "2026-07-22T12:00:00Z",
            "no_matching_output",
            True,
        )

    def test_rejects_second_active_project_after_successful_creation(self) -> None:
        journal = self.journal()
        with self.assertRaises(stitch_operations.JournalError):
            stitch_operations.adopt_project(
                journal,
                "project-456",
                "created_current_run",
                "Fallback Project",
            )

    def test_rejects_project_outside_current_run_provenance(self) -> None:
        journal = self.journal()
        with self.assertRaises(stitch_operations.JournalError):
            stitch_operations.ensure_project_known(journal, "unrelated-project")
        with self.assertRaises(stitch_operations.JournalError):
            stitch_operations.prepare_operation(
                journal,
                "foreign-001",
                "generate_screen",
                "unrelated-project",
                "welcome",
            )

    def test_allows_registered_secondary_project_for_read_provenance(self) -> None:
        journal = self.journal()
        stitch_operations.register_reference_project(
            journal,
            "reference-project",
            "repo_metadata",
            "Secondary Design Reference",
        )
        stitch_operations.ensure_project_known(journal, "reference-project")
        with self.assertRaises(stitch_operations.JournalError):
            stitch_operations.prepare_operation(
                journal,
                "reference-write",
                "generate_screen",
                "reference-project",
                "welcome",
            )

    def test_invalid_argument_keeps_original_project_available(self) -> None:
        journal = self.journal()
        self.prepare(journal)
        stitch_operations.transition_operation(journal, "welcome-001", "submitted")
        stitch_operations.transition_operation(
            journal,
            "welcome-001",
            "failed",
            failure_class="invalid_argument",
        )
        self.assertEqual(journal["activeProject"]["id"], "project-123")
        stitch_operations.prepare_operation(
            journal,
            "welcome-schema-corrected",
            "generate_screen",
            "project-123",
            "welcome",
            prompt="Generate the welcome screen with the corrected payload.",
        )

    def test_prepare_requires_the_exact_prompt(self) -> None:
        journal = self.journal()
        with self.assertRaisesRegex(
            stitch_operations.JournalError, "exact mutation prompt"
        ):
            stitch_operations.prepare_operation(
                journal,
                "welcome-without-prompt",
                "generate_screen",
                "project-123",
                "welcome",
            )

    def test_timeout_requires_linked_replacement_authorization(self) -> None:
        journal = self.journal()
        self.prepare(journal)
        stitch_operations.transition_operation(journal, "welcome-001", "submitted")
        stitch_operations.transition_operation(
            journal,
            "welcome-001",
            "ambiguous_timeout",
            failure_class="timeout_or_connection",
        )
        with self.assertRaisesRegex(
            stitch_operations.JournalError, "at least one recorded poll"
        ):
            stitch_operations.transition_operation(
                journal,
                "welcome-001",
                "replacement_authorized",
            )
        with self.assertRaises(stitch_operations.JournalError):
            stitch_operations.prepare_operation(
                journal,
                "welcome-002",
                "generate_screen",
                "project-123",
                "welcome",
                prompt="Generate the welcome screen again.",
            )
        stitch_operations.transition_operation(journal, "welcome-001", "polling")
        stitch_operations.transition_operation(
            journal,
            "welcome-001",
            "ambiguous_timeout",
        )
        with self.assertRaisesRegex(
            stitch_operations.JournalError, "final same-project reconciliation"
        ):
            stitch_operations.transition_operation(
                journal,
                "welcome-001",
                "replacement_authorized",
            )
        stitch_operations.record_final_reconciliation(
            journal,
            "welcome-001",
            ["existing-screen"],
            "2026-07-22T12:00:00Z",
            "no_matching_output",
            True,
        )
        stitch_operations.transition_operation(
            journal,
            "welcome-001",
            "replacement_authorized",
        )
        stitch_operations.prepare_operation(
            journal,
            "welcome-002",
            "generate_screen",
            "project-123",
            "welcome",
            replacement_for="welcome-001",
            prompt="Generate the welcome screen again.",
        )
        self.assertEqual(journal["operations"][-1]["replacementFor"], "welcome-001")

    def test_replacement_link_cannot_bypass_authorization_with_a_new_role(self) -> None:
        journal = self.journal()
        self.prepare(
            journal,
            screen_role="onboarding-set",
            requested_screen_roles=["welcome", "goals"],
        )
        stitch_operations.transition_operation(journal, "welcome-001", "submitted")
        stitch_operations.transition_operation(
            journal,
            "welcome-001",
            "ambiguous_timeout",
            failure_class="timeout_or_connection",
        )

        with self.assertRaisesRegex(
            stitch_operations.JournalError, "replacement target is not authorized"
        ):
            self.prepare(
                journal,
                operation_id="goals-focused",
                screen_role="goals",
                requested_screen_roles=["goals"],
                replacement_for="welcome-001",
            )

    def test_persists_exact_prompt_and_flags_compound_screen_requests(self) -> None:
        journal = self.journal()
        prompt = "Generate onboarding screens.\nPreserve this exact wording.\n"
        operation = self.prepare(
            journal,
            screen_role="onboarding-set",
            prompt=prompt,
            requested_screen_roles=["welcome", "goals"],
        )

        self.assertEqual(operation["request"]["prompt"], prompt)
        self.assertEqual(
            operation["request"]["promptSha256"],
            stitch_operations.prompt_sha256(prompt),
        )
        self.assertTrue(operation["recovery"]["decompositionRecommended"])
        _, warnings, _ = stitch_operations.audit_journal(journal)
        self.assertTrue(any("multiple screen roles" in item for item in warnings))

    def test_ambiguous_timeout_records_polls_and_requires_immediate_decision(self) -> None:
        journal = self.journal()
        self.prepare(
            journal,
            screen_role="onboarding-set",
            requested_screen_roles=["welcome", "goals"],
        )
        stitch_operations.transition_operation(journal, "welcome-001", "submitted")
        stitch_operations.transition_operation(
            journal,
            "welcome-001",
            "polling",
            failure_class="timeout_or_connection",
        )
        stitch_operations.transition_operation(journal, "welcome-001", "polling")
        operation = stitch_operations.transition_operation(
            journal,
            "welcome-001",
            "ambiguous_timeout",
        )

        self.assertEqual(operation["recovery"]["pollCount"], 2)
        self.assertEqual(
            operation["recovery"]["decisionStatus"],
            "final_reconciliation_required",
        )
        self.assertIsNotNone(operation["recovery"]["decisionRequiredAt"])
        _, warnings, _ = stitch_operations.audit_journal(journal)
        immediate = [
            item
            for item in warnings
            if item.startswith("FINAL RECONCILIATION REQUIRED:")
        ]
        self.assertEqual(len(immediate), 1)

        operation = stitch_operations.record_final_reconciliation(
            journal,
            "welcome-001",
            ["existing-screen"],
            "2026-07-22T12:00:00Z",
            "no_matching_output",
            True,
        )
        self.assertEqual(
            operation["recovery"]["decisionStatus"], "autonomous_recovery_ready"
        )
        _, warnings, _ = stitch_operations.audit_journal(journal)
        immediate = [
            item for item in warnings if item.startswith("AUTONOMOUS RECOVERY:")
        ]
        self.assertEqual(len(immediate), 1)
        self.assertIn("decompose the compound request", immediate[0])

    def test_manual_recovery_mode_still_requires_a_user_decision(self) -> None:
        journal = self.journal(replacement_mode="manual")
        self.prepare(journal)
        stitch_operations.transition_operation(journal, "welcome-001", "submitted")
        stitch_operations.transition_operation(
            journal,
            "welcome-001",
            "polling",
            failure_class="timeout_or_connection",
        )
        operation = stitch_operations.transition_operation(
            journal, "welcome-001", "ambiguous_timeout"
        )

        self.assertEqual(
            operation["recovery"]["decisionStatus"],
            "final_reconciliation_required",
        )
        operation = stitch_operations.record_final_reconciliation(
            journal,
            "welcome-001",
            ["existing-screen"],
            "2026-07-22T12:00:00Z",
            "no_matching_output",
            True,
        )
        self.assertEqual(operation["recovery"]["decisionStatus"], "required")
        _, warnings, _ = stitch_operations.audit_journal(journal)
        self.assertTrue(
            any(
                item.startswith("IMMEDIATE RECOVERY DECISION:")
                for item in warnings
            )
        )

    def test_legacy_journal_without_policy_remains_manual(self) -> None:
        journal = self.journal()
        del journal["recoveryPolicy"]
        operation = self.prepare(journal)
        del operation["request"]
        del operation["recovery"]

        self.assertEqual(
            stitch_operations.recovery_policy(journal)["replacementMode"],
            "manual",
        )
        stitch_operations.transition_operation(journal, "welcome-001", "submitted")
        operation = self.reconcile_timeout(journal)
        self.assertEqual(operation["recovery"]["decisionStatus"], "required")

        stitch_operations.set_recovery_policy(
            journal,
            replacement_mode="autonomous",
        )
        self.assertEqual(
            stitch_operations.recovery_policy(journal)["replacementMode"],
            "autonomous",
        )

    def test_final_reconciliation_adopts_matching_output(self) -> None:
        journal = self.journal()
        self.prepare(journal)
        stitch_operations.transition_operation(journal, "welcome-001", "submitted")
        stitch_operations.transition_operation(
            journal,
            "welcome-001",
            "polling",
            failure_class="timeout_or_connection",
        )
        stitch_operations.transition_operation(
            journal, "welcome-001", "ambiguous_timeout"
        )

        operation = stitch_operations.record_final_reconciliation(
            journal,
            "welcome-001",
            ["existing-screen", "welcome-screen"],
            "2026-07-22T12:00:00Z",
            "matching_output",
            True,
            matching_screen_ids=["welcome-screen"],
        )

        self.assertEqual(operation["status"], "succeeded")
        self.assertEqual(operation["newScreenIds"], ["welcome-screen"])
        self.assertEqual(
            operation["recovery"]["finalReconciliation"]["outcome"],
            "matching_output",
        )

    def test_truncated_final_reconciliation_cannot_authorize_replacement(self) -> None:
        journal = self.journal()
        self.prepare(journal)
        stitch_operations.transition_operation(journal, "welcome-001", "submitted")
        stitch_operations.transition_operation(
            journal,
            "welcome-001",
            "polling",
            failure_class="timeout_or_connection",
        )
        stitch_operations.transition_operation(
            journal, "welcome-001", "ambiguous_timeout"
        )

        with self.assertRaisesRegex(
            stitch_operations.JournalError, "truncated.*inconclusive"
        ):
            stitch_operations.record_final_reconciliation(
                journal,
                "welcome-001",
                ["existing-screen"],
                "2026-07-22T12:00:00Z",
                "no_matching_output",
                False,
            )

    def test_default_replacement_budget_stops_a_repeated_timeout(self) -> None:
        journal = self.journal()
        self.prepare(journal)
        stitch_operations.transition_operation(journal, "welcome-001", "submitted")
        self.reconcile_timeout(journal)
        stitch_operations.transition_operation(
            journal, "welcome-001", "replacement_authorized"
        )
        self.prepare(
            journal,
            operation_id="welcome-002",
            replacement_for="welcome-001",
        )
        stitch_operations.transition_operation(journal, "welcome-002", "submitted")
        self.reconcile_timeout(journal, "welcome-002")

        with self.assertRaisesRegex(
            stitch_operations.JournalError, "replacement budget exhausted"
        ):
            stitch_operations.transition_operation(
                journal, "welcome-002", "replacement_authorized"
            )

    def test_replacement_budget_is_configurable(self) -> None:
        journal = self.journal(max_replacement_attempts=2)
        self.prepare(journal)
        stitch_operations.transition_operation(journal, "welcome-001", "submitted")
        self.reconcile_timeout(journal)
        stitch_operations.transition_operation(
            journal, "welcome-001", "replacement_authorized"
        )
        self.prepare(
            journal,
            operation_id="welcome-002",
            replacement_for="welcome-001",
        )
        stitch_operations.transition_operation(journal, "welcome-002", "submitted")
        self.reconcile_timeout(journal, "welcome-002")
        operation = stitch_operations.transition_operation(
            journal, "welcome-002", "replacement_authorized"
        )
        self.assertEqual(
            operation["recovery"]["decisionStatus"], "replacement_authorized"
        )

    def test_authorized_compound_replacement_can_be_decomposed_once(self) -> None:
        journal = self.journal()
        self.prepare(
            journal,
            screen_role="onboarding-set",
            requested_screen_roles=["welcome", "goals"],
        )
        stitch_operations.transition_operation(journal, "welcome-001", "submitted")
        self.reconcile_timeout(journal)
        stitch_operations.transition_operation(
            journal, "welcome-001", "replacement_authorized"
        )

        with self.assertRaisesRegex(
            stitch_operations.JournalError, "must decompose a compound request"
        ):
            self.prepare(
                journal,
                operation_id="onboarding-repeated",
                screen_role="onboarding-set",
                requested_screen_roles=["welcome", "goals"],
                replacement_for="welcome-001",
            )

        welcome = self.prepare(
            journal,
            operation_id="welcome-focused",
            screen_role="welcome",
            requested_screen_roles=["welcome"],
            replacement_for="welcome-001",
        )
        goals = self.prepare(
            journal,
            operation_id="goals-focused",
            screen_role="goals",
            requested_screen_roles=["goals"],
            replacement_for="welcome-001",
        )
        self.assertEqual(welcome["recovery"]["replacementStrategy"], "decomposed")
        self.assertEqual(goals["recovery"]["replacementStrategy"], "decomposed")
        stitch_operations.transition_operation(
            journal, "welcome-focused", "submitted"
        )
        stitch_operations.transition_operation(
            journal,
            "welcome-focused",
            "succeeded",
            new_screen_ids=["welcome-screen"],
        )
        with self.assertRaisesRegex(
            stitch_operations.JournalError, "already produced the requested screen roles"
        ):
            self.prepare(
                journal,
                operation_id="welcome-duplicate",
                screen_role="welcome",
                requested_screen_roles=["welcome"],
                replacement_for="welcome-001",
            )

    def test_late_original_success_cancels_a_prepared_replacement(self) -> None:
        journal = self.journal()
        self.prepare(journal)
        stitch_operations.transition_operation(journal, "welcome-001", "submitted")
        self.reconcile_timeout(journal)
        stitch_operations.transition_operation(
            journal, "welcome-001", "replacement_authorized"
        )
        self.prepare(
            journal,
            operation_id="welcome-002",
            replacement_for="welcome-001",
        )
        stitch_operations.transition_operation(
            journal,
            "welcome-001",
            "succeeded",
            new_screen_ids=["late-welcome-screen"],
        )

        with self.assertRaisesRegex(
            stitch_operations.JournalError, "no longer authorized"
        ):
            stitch_operations.transition_operation(
                journal, "welcome-002", "submitted"
            )
        replacement = stitch_operations.transition_operation(
            journal, "welcome-002", "abandoned"
        )
        self.assertEqual(replacement["status"], "abandoned")

    def test_completed_role_can_be_explored_again(self) -> None:
        journal = self.journal()
        self.prepare(journal)
        stitch_operations.transition_operation(journal, "welcome-001", "submitted")
        stitch_operations.transition_operation(
            journal,
            "welcome-001",
            "succeeded",
            new_screen_ids=["welcome-screen"],
        )
        stitch_operations.prepare_operation(
            journal,
            "welcome-variant-001",
            "generate_screen",
            "project-123",
            "welcome",
            prompt="Generate a distinct welcome exploration.",
        )

    def test_optional_capability_failure_is_non_blocking(self) -> None:
        journal = self.journal()
        stitch_operations.set_capability(
            journal, "stitch", "required", "ready"
        )
        stitch_operations.set_capability(
            journal, "cloudflare", "optional", "unavailable"
        )
        errors, warnings, info = stitch_operations.audit_journal(journal)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertTrue(any("cloudflare" in item for item in info))

    def test_required_capability_failure_blocks_audit(self) -> None:
        journal = self.journal()
        stitch_operations.set_capability(
            journal, "stitch", "required", "unavailable"
        )
        errors, _, _ = stitch_operations.audit_journal(journal)
        self.assertTrue(any("stitch" in item for item in errors))

    def test_required_missing_concept_role_needs_expansion_task(self) -> None:
        errors, warnings = stitch_operations.audit_concept_coverage(
            [
                {
                    "role": "Primary detail",
                    "required": True,
                    "status": "missing",
                    "linkedTask": None,
                }
            ]
        )
        self.assertTrue(any("Primary detail" in item for item in errors))
        self.assertEqual(warnings, [])

    def test_coverage_roles_are_product_driven_not_fixed_count(self) -> None:
        errors, warnings = stitch_operations.audit_concept_coverage(
            [
                {
                    "role": "Creation result",
                    "required": True,
                    "status": "missing",
                    "linkedTask": "APP-004",
                },
                {
                    "role": "Settings",
                    "required": False,
                    "status": "not_needed",
                },
            ]
        )
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])


class BootstrapReceiptTests(unittest.TestCase):
    def write_repo(self, root: Path, *, create_project: bool = True) -> None:
        stitch = root / ".stitch"
        stitch.mkdir(parents=True)
        metadata = {
            "app": {
                "name": "Kitty Keeper",
                "nativeTarget": "KittyKeeper",
                "nativeProjectPath": "KittyKeeperApp/KittyKeeper.xcodeproj",
                "bundleIdentifier": "com.example.kittykeeper",
            },
            "stitchProjects": {
                "primaryConceptProject": {"projectId": "project-123"}
            },
            "riskRegister": [],
        }
        (stitch / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
        (stitch / "next-prompt.md").write_text(
            "---\nroadmap_task: APP-002\ntask_type: feature_delivery\n---\n\n"
            "Build the first slice.\n",
            encoding="utf-8",
        )
        if create_project:
            project = root / "KittyKeeperApp" / "KittyKeeper.xcodeproj"
            project.mkdir(parents=True)
            (project / "project.pbxproj").write_text("// test", encoding="utf-8")

    def test_ready_receipt_records_required_identity_and_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write_repo(root)
            text = bootstrap_receipt.render_receipt(
                root,
                first_build_result="succeeded",
                baton_validation="passed",
                stitch_status="auto",
                build_evidence=".stitch/evidence/bootstrap/launch.png",
                notes=[],
                scheme_discovered="yes",
                first_launch_result="succeeded",
                launch_evidence=".stitch/evidence/bootstrap/launch.png",
                toolchain_status="supported",
            )
            self.assertIn("Completion state: `ready_for_delivery`", text)
            self.assertIn("Stitch project ID: `project-123`", text)
            self.assertIn("Target: `KittyKeeper`", text)
            self.assertIn("Active roadmap task: `APP-002`", text)
            self.assertIn("Active task type: `feature_delivery`", text)
            self.assertIn("Provisional `com.example` identifier: `yes`", text)

    def test_undiscovered_scheme_keeps_receipt_partial(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write_repo(root)
            text = bootstrap_receipt.render_receipt(
                root,
                first_build_result="succeeded",
                baton_validation="passed",
                stitch_status="auto",
                build_evidence=".stitch/evidence/bootstrap/launch.png",
                notes=[],
                scheme_discovered="unknown",
                first_launch_result="succeeded",
                toolchain_status="supported",
            )
            self.assertIn("Completion state: `partial`", text)
            self.assertIn("scheme-discovery: unknown", text)

    def test_completed_scaffold_baton_cannot_report_delivery_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write_repo(root)
            (root / ".stitch" / "next-prompt.md").write_text(
                "---\nroadmap_task: APP-001\ntask_type: native_scaffold\n---\n\n"
                "Create the scaffold.\n",
                encoding="utf-8",
            )
            text = bootstrap_receipt.render_receipt(
                root,
                first_build_result="succeeded",
                baton_validation="passed",
                stitch_status="auto",
                build_evidence=".stitch/evidence/bootstrap/launch.png",
                notes=[],
                scheme_discovered="yes",
                first_launch_result="succeeded",
                toolchain_status="supported",
            )
            self.assertIn("Completion state: `partial`", text)
            self.assertIn("does not identify the next delivery task", text)

    def test_missing_project_still_renders_actionable_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write_repo(root, create_project=False)
            text = bootstrap_receipt.render_receipt(
                root,
                first_build_result="not_run",
                baton_validation="passed",
                stitch_status="unavailable",
                build_evidence=None,
                notes=["Stitch authentication needs attention"],
                first_launch_result="not_run",
                toolchain_status="supported",
            )
            self.assertIn("Completion state: `blocked`", text)
            self.assertIn("recorded native project was not found", text)
            self.assertIn("Stitch authentication needs attention", text)

    def test_receipt_records_missing_stitch_api_key_precisely(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write_repo(root)
            text = bootstrap_receipt.render_receipt(
                root,
                first_build_result="succeeded",
                baton_validation="passed",
                stitch_status="api_key_required",
                build_evidence=".stitch/evidence/bootstrap/launch.png",
                notes=["Set STITCH_API_KEY, restart Codex Desktop, and resume Stitch."],
                scheme_discovered="yes",
                first_launch_result="succeeded",
                toolchain_status="supported",
            )
            self.assertIn("Stitch status: `api_key_required`", text)
            self.assertIn("Set STITCH_API_KEY, restart Codex Desktop", text)

    def test_receipt_cli_accepts_api_key_required_status(self) -> None:
        args = bootstrap_receipt.build_parser().parse_args(
            ["--repo-root", ".", "--stitch-status", "api_key_required"]
        )
        self.assertEqual(args.stitch_status, "api_key_required")

    def test_successful_build_with_failed_launch_stays_partial(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write_repo(root)
            text = bootstrap_receipt.render_receipt(
                root,
                first_build_result="succeeded",
                first_launch_result="failed",
                baton_validation="passed",
                stitch_status="api_key_required",
                build_evidence="BUILD SUCCEEDED",
                launch_evidence="simulator showed only a boot spinner",
                notes=[],
                scheme_discovered="yes",
                toolchain_status="supported",
            )
            self.assertIn("Completion state: `partial`", text)
            self.assertIn("First build: `succeeded`", text)
            self.assertIn("First launch: `failed`", text)
            self.assertIn("first-launch: failed", text)
            self.assertIn("simulator showed only a boot spinner", text)

    def test_unsupported_toolchain_blocks_even_when_project_exists(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write_repo(root)
            text = bootstrap_receipt.render_receipt(
                root,
                first_build_result="not_run",
                first_launch_result="not_run",
                baton_validation="not_run",
                stitch_status="api_key_required",
                build_evidence=None,
                notes=["Installed Xcode is 15.2."],
                scheme_discovered="unknown",
                toolchain_status="unsupported_toolchain",
            )
            self.assertIn("Completion state: `blocked`", text)
            self.assertIn("Xcode toolchain: `unsupported_toolchain`", text)
            self.assertIn("Install and select Xcode 16 or newer", text)

    def test_receipt_cli_accepts_unsupported_toolchain_status(self) -> None:
        args = bootstrap_receipt.build_parser().parse_args(
            ["--repo-root", ".", "--toolchain-status", "unsupported_toolchain"]
        )
        self.assertEqual(args.toolchain_status, "unsupported_toolchain")


class TemplateDeploymentTests(unittest.TestCase):
    def test_deploys_complete_hidden_file_template_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo_root = Path(temporary_directory) / "NewNativeApp"
            first = template_deployer.deploy_template(repo_root)
            expected_files = {
                path.relative_to(template_deployer.TEMPLATE_ROOT).as_posix()
                for path in template_deployer.template_files()
            }

            self.assertEqual(set(first["created"]), expected_files)
            self.assertTrue((repo_root / ".gitignore").is_file())
            marketplace = json.loads(
                (repo_root / ".agents/plugins/marketplace.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(marketplace["plugins"], [])
            self.assertFalse((repo_root / "plugins/ios-app-director").exists())

            second = template_deployer.deploy_template(repo_root)
            self.assertEqual(second["created"], [])
            self.assertEqual(second["preserved"], [])
            self.assertEqual(set(second["unchanged"]), expected_files)

    def test_preserves_differing_files_unless_overwrite_is_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo_root = Path(temporary_directory) / "ExistingApp"
            template_deployer.deploy_template(repo_root)
            readme = repo_root / "README.md"
            readme.write_text("User-owned README\n", encoding="utf-8")

            preserved = template_deployer.deploy_template(repo_root)
            self.assertIn("README.md", preserved["preserved"])
            self.assertEqual(readme.read_text(encoding="utf-8"), "User-owned README\n")

            overwritten = template_deployer.deploy_template(repo_root, overwrite=True)
            self.assertIn("README.md", overwritten["overwritten"])
            self.assertEqual(
                readme.read_bytes(),
                (template_deployer.TEMPLATE_ROOT / "README.md").read_bytes(),
            )

    def test_preserves_symlinked_destinations_even_with_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            repo_root = root / "ExistingApp"
            outside = root / "outside"
            repo_root.mkdir()
            outside.mkdir()
            (repo_root / "docs").symlink_to(outside, target_is_directory=True)

            result = template_deployer.deploy_template(repo_root, overwrite=True)

            self.assertIn("docs/app-build-spec.md", result["preserved"])
            self.assertFalse((outside / "app-build-spec.md").exists())

    def test_relocated_installed_skill_can_deploy_without_source_repo(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            installed_skill = root / "codex-cache/ios-app-director/skills/ios-app-bootstrap"
            shutil.copytree(
                PLUGIN_ROOT / "skills/ios-app-bootstrap",
                installed_skill,
            )
            repo_root = root / "standalone-app"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(installed_skill / "scripts/deploy_ready_template.py"),
                    "--repo-root",
                    str(repo_root),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("Deployment complete", completed.stdout)
            self.assertTrue((repo_root / "AGENTS.md").is_file())
            self.assertTrue((repo_root / ".stitch/next-prompt.md").is_file())
            self.assertTrue((repo_root / "docs/app-build-spec.md").is_file())
            self.assertFalse((repo_root / "plugins").exists())


class DistributionContractTests(unittest.TestCase):
    def test_plugin_declares_stitch_api_key_mcp_contract(self) -> None:
        ready_root = PLUGIN_ROOT.parent.parent
        manifest = json.loads(
            (PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        mcp = json.loads((PLUGIN_ROOT / ".mcp.json").read_text(encoding="utf-8"))
        stitch = mcp["mcpServers"]["stitch"]
        xcodebuildmcp = mcp["mcpServers"]["xcodebuildmcp"]
        cloudflare = mcp["mcpServers"]["cloudflare-api"]

        self.assertEqual(manifest["version"], "0.5.5")
        self.assertEqual(manifest["mcpServers"], "./.mcp.json")
        self.assertEqual(
            xcodebuildmcp["env"]["XCODEBUILDMCP_ENABLED_WORKFLOWS"],
            "simulator,ui-automation,debugging",
        )
        self.assertNotIn(
            "logging",
            xcodebuildmcp["env"]["XCODEBUILDMCP_ENABLED_WORKFLOWS"],
        )
        self.assertEqual(stitch["url"], "https://stitch.googleapis.com/mcp")
        self.assertEqual(
            stitch["env_http_headers"],
            {"X-Goog-Api-Key": "STITCH_API_KEY"},
        )
        self.assertEqual(stitch["tool_timeout_sec"], 300)
        self.assertIn("generic OAuth Authenticate action is not", stitch["note"])
        self.assertEqual(cloudflare["url"], "https://mcp.cloudflare.com/mcp")
        self.assertIs(cloudflare["enabled"], False)
        self.assertIn("disabled by default", cloudflare["note"])

        plugin_readme = (PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")
        setup = (ready_root / "SETUP.md").read_text(encoding="utf-8")
        for document in (plugin_readme, setup):
            self.assertIn("https://stitch.withgoogle.com/settings", document)
            self.assertIn("STITCH_API_KEY", document)
            self.assertIn("Google AI Studio", document)
            self.assertIn("never paste", document.lower())
            self.assertIn("cloudflare-api", document)
            self.assertIn("disabled by default", document.lower())

        helper_path = PLUGIN_ROOT / "scripts/configure-stitch-api-key-macos.sh"
        helper = helper_path.read_text(encoding="utf-8")
        self.assertTrue(helper_path.stat().st_mode & 0o111)
        self.assertIn("read -r -s stitch_api_key", helper)
        self.assertIn("launchctl setenv STITCH_API_KEY", helper)
        self.assertIn("launchctl unsetenv STITCH_API_KEY", helper)
        self.assertNotIn("echo $stitch_api_key", helper)

    def test_stitch_timeout_matches_generated_project_config(self) -> None:
        ready_root = PLUGIN_ROOT.parent.parent
        source_config = (ready_root / ".codex/config.toml").read_text(
            encoding="utf-8"
        )
        template_config = (
            PLUGIN_ROOT
            / "skills/ios-app-bootstrap/templates/ai-app-engine/.codex/config.toml"
        ).read_text(encoding="utf-8")

        self.assertIn("tool_timeout_sec = 300", source_config)
        self.assertIn("tool_timeout_sec = 300", template_config)
        self.assertNotIn("tool_timeout_sec = 60", source_config)
        self.assertNotIn("tool_timeout_sec = 60", template_config)

    def test_plugin_image_assets_are_png_at_required_sizes(self) -> None:
        manifest = json.loads(
            (PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        expected_assets = {
            "composerIcon": ("./assets/ios-app-director-icon.png", (128, 128)),
            "logo": ("./assets/ios-app-director-logo.png", (512, 512)),
        }

        for field, (relative_path, expected_size) in expected_assets.items():
            with self.subTest(field=field):
                self.assertEqual(manifest["interface"][field], relative_path)
                asset_path = PLUGIN_ROOT / relative_path.removeprefix("./")
                data = asset_path.read_bytes()
                self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(struct.unpack(">II", data[16:24]), expected_size)

        agent_card = (PLUGIN_ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("./assets/ios-app-director-icon.png", agent_card)
        self.assertIn("./assets/ios-app-director-logo.png", agent_card)
        self.assertNotIn(".svg", agent_card)

        self.assertFalse((PLUGIN_ROOT / "assets/ios-app-director-icon.svg").exists())
        self.assertFalse((PLUGIN_ROOT / "assets/ios-app-director-logo.svg").exists())

    def test_license_separates_apache_engine_from_mit_plugin(self) -> None:
        ready_root = PLUGIN_ROOT.parent.parent
        source_license = (ready_root / "LICENSE").read_bytes()
        source_notice = (ready_root / "NOTICE").read_bytes()
        plugin_license = (PLUGIN_ROOT / "LICENSE").read_bytes()
        template_root = (
            PLUGIN_ROOT / "skills/ios-app-bootstrap/templates/ai-app-engine"
        )
        template_license = (
            template_root / "LICENSES/NATIVE-READY-APACHE-2.0.txt"
        ).read_bytes()
        template_notice = (
            template_root / "LICENSES/NATIVE-READY-NOTICE.txt"
        ).read_bytes()

        self.assertEqual(source_license, template_license)
        self.assertEqual(source_notice, template_notice)
        self.assertIn(b"Apache License", source_license)
        self.assertIn(b"Version 2.0, January 2004", source_license)
        self.assertIn(b"Copyright 2026 Matt Glass", source_notice)

        self.assertNotEqual(source_license, plugin_license)
        self.assertIn(b"MIT License", plugin_license)
        self.assertIn(b"Copyright (c) 2026 Matt Glass", plugin_license)
        self.assertFalse(
            (template_root / "LICENSES/NATIVE-READY-MIT.txt").exists()
        )

        repo_licensing = (ready_root / "LICENSING.md").read_text(encoding="utf-8")
        plugin_licensing = (PLUGIN_ROOT / "LICENSING.md").read_text(encoding="utf-8")
        template_path = "skills/ios-app-bootstrap/templates/ai-app-engine/"
        self.assertIn("Apache License 2.0", repo_licensing)
        self.assertIn("MIT License", repo_licensing)
        self.assertIn(template_path, plugin_licensing)
        self.assertIn("excluded from that MIT grant", plugin_licensing)

        manifest = json.loads(
            (PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["author"]["name"], "Matt Glass")
        self.assertEqual(manifest["license"], "MIT")

    def test_marketplace_distribution_separates_source_and_generated_apps(self) -> None:
        ready_root = PLUGIN_ROOT.parent.parent
        marketplace = json.loads(
            (ready_root / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
        )
        entry = next(
            plugin
            for plugin in marketplace["plugins"]
            if plugin["name"] == "ios-app-director"
        )
        self.assertEqual(marketplace["name"], "repo-local-plugins")
        self.assertEqual(
            entry["source"],
            {"source": "local", "path": "./plugins/ios-app-director"},
        )
        plugin_path = ready_root / entry["source"]["path"]
        self.assertTrue((plugin_path / ".codex-plugin/plugin.json").is_file())
        self.assertEqual(
            entry["policy"],
            {"installation": "AVAILABLE", "authentication": "ON_USE"},
        )
        self.assertEqual(entry["category"], "Coding")
        opt_in_marketplace = json.loads(
            (
                ready_root
                / ".agents/plugins/marketplace.opt-in-ios-app-director.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(marketplace, opt_in_marketplace)

        nested = PLUGIN_ROOT / "skills/ios-app-bootstrap/templates/ai-app-engine"
        nested_marketplace = json.loads(
            (nested / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
        )
        self.assertEqual(nested_marketplace["name"], marketplace["name"])
        self.assertEqual(nested_marketplace["interface"], marketplace["interface"])
        self.assertEqual(nested_marketplace["plugins"], [])

        nested_opt_in_marketplace = json.loads(
            (
                nested
                / ".agents/plugins/marketplace.opt-in-ios-app-director.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(nested_opt_in_marketplace, opt_in_marketplace)

    def test_template_baton_quotes_placeholder_values_for_yaml(self) -> None:
        ready_root = PLUGIN_ROOT.parent.parent
        next_prompt = (ready_root / ".stitch/next-prompt.md").read_text(encoding="utf-8")
        self.assertIn('platform: "[PRIMARY_PLATFORM]"', next_prompt)
        self.assertIn(
            'destination: "[NATIVE_SOURCE_ROOT] native project scaffold and feature folders"',
            next_prompt,
        )

    def test_root_and_nested_template_operating_files_match(self) -> None:
        ready_root = PLUGIN_ROOT.parent.parent
        nested = PLUGIN_ROOT / "skills/ios-app-bootstrap/templates/ai-app-engine"
        intentional_template_exceptions = {
            ".agents/plugins/marketplace.json",
            "LICENSES/NATIVE-READY-APACHE-2.0.txt",
            "LICENSES/NATIVE-READY-NOTICE.txt",
            "LICENSING.md",
        }
        template_paths = {
            path.relative_to(nested).as_posix()
            for path in template_deployer.template_files(nested)
        }
        shared = sorted(template_paths - intentional_template_exceptions)

        self.assertTrue(intentional_template_exceptions <= template_paths)
        for relative_path in shared:
            with self.subTest(path=relative_path):
                self.assertTrue((ready_root / relative_path).is_file())
                self.assertEqual(
                    (ready_root / relative_path).read_bytes(),
                    (nested / relative_path).read_bytes(),
                )

    def test_standalone_skills_do_not_require_repo_local_plugin_scripts(self) -> None:
        ready_root = PLUGIN_ROOT.parent.parent
        bootstrap_skill = (
            PLUGIN_ROOT / "skills/ios-app-bootstrap/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("scripts/deploy_ready_template.py", bootstrap_skill)

        hardcoded_commands: list[str] = []
        for path in (PLUGIN_ROOT / "skills").rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for command in ("python3 plugins/ios-app-director/", "python3 scripts/"):
                if command in text:
                    hardcoded_commands.append(
                        f"{path.relative_to(PLUGIN_ROOT)}: {command}"
                    )
        self.assertEqual(hardcoded_commands, [])

        config = (ready_root / ".codex/config.toml").read_text(encoding="utf-8")
        self.assertIn("[mcp_servers.xcodebuildmcp]", config)
        self.assertNotIn("[mcp_servers.XcodeBuildMCP]", config)
        self.assertIn(
            'XCODEBUILDMCP_ENABLED_WORKFLOWS = "simulator,ui-automation,debugging"',
            config,
        )

    def test_distribution_excludes_retired_or_foreign_skill_names(self) -> None:
        ready_root = PLUGIN_ROOT.parent.parent
        excluded = ("stitch" + "-design", "CLAUDE" + "mdTests")
        matches: list[str] = []
        for path in ready_root.rglob("*"):
            if not path.is_file() or path.suffix not in {".md", ".toml", ".json", ".yaml"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for term in excluded:
                if term in text:
                    matches.append(f"{path.relative_to(ready_root)}: {term}")
        self.assertEqual(matches, [])


if __name__ == "__main__":
    unittest.main()
