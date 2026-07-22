from __future__ import annotations

import importlib.util
import json
import struct
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
                    deployment_target="26.0",
                    force=False,
                )
            )
            metadata = json.loads((root / ".stitch" / "metadata.json").read_text())
            self.assertEqual(result["plannedTestTarget"], "KittyKeeperTests")
            self.assertEqual(metadata["app"]["nativeTestTarget"], "KittyKeeperTests")
            self.assertIn("KittyKeeperTests", (root / "AGENTS.md").read_text())


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
    def journal(self):
        journal = stitch_operations.new_journal(
            "setup-001",
            "Example App Concepts",
            required_capabilities=["stitch"],
            optional_capabilities=["cloudflare"],
        )
        stitch_operations.adopt_project(
            journal,
            "project-123",
            "created_current_run",
            "Example App Concepts",
        )
        return journal

    def prepare(self, journal, operation_id="welcome-001", screen_role="welcome"):
        stitch_operations.prepare_operation(
            journal,
            operation_id,
            "generate_screen",
            "project-123",
            screen_role,
            ["existing-screen"],
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
        with self.assertRaises(stitch_operations.JournalError):
            stitch_operations.prepare_operation(
                journal,
                "welcome-002",
                "generate_screen",
                "project-123",
                "welcome",
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
        )
        self.assertEqual(journal["operations"][-1]["replacementFor"], "welcome-001")

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
            )
            self.assertIn("Completion state: `blocked`", text)
            self.assertIn("recorded native project was not found", text)
            self.assertIn("Stitch authentication needs attention", text)


class DistributionContractTests(unittest.TestCase):
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
            {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
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
        shared = [
            "AGENTS.md",
            "README.md",
            "SETUP.md",
            ".agents/plugins/marketplace.opt-in-ios-app-director.json",
            ".codex/config.toml",
            ".stitch/APP.md",
            ".stitch/DESIGN.md",
            ".stitch/ROADMAP.md",
            ".stitch/next-prompt.md",
            ".stitch/metadata.json",
            "docs/ai-app-development-engine-spec.md",
            "docs/app-build-spec.md",
            "docs/bootstrap-prompt.md",
            "docs/definition-of-done.md",
            "docs/design-first-setup-prompt.md",
            "docs/example-build-spec.md",
            "workers/README.md",
        ]
        for relative_path in shared:
            with self.subTest(path=relative_path):
                self.assertEqual(
                    (ready_root / relative_path).read_bytes(),
                    (nested / relative_path).read_bytes(),
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
