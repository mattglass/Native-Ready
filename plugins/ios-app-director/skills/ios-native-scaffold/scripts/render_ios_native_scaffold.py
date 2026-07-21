#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


GENERATOR = "ios-native-scaffold"
DEFAULT_BUNDLE_PREFIX = "com.example"
GENERIC_TARGETS = {"app", "myapp", "testapp", "untitledapp"}


def pascal_identifier(value: str) -> str:
    tokens = re.findall(r"[A-Za-z0-9]+", value)
    if not tokens:
        raise ValueError("Could not derive a target name from the app name.")
    result = "".join(token[:1].upper() + token[1:] for token in tokens)
    if result[0].isdigit():
        result = f"App{result}"
    if result.lower() in GENERIC_TARGETS:
        raise ValueError(f"Refusing to scaffold with generic target name: {result}")
    return result


def bundle_slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "", value.lower())
    if not result:
        raise ValueError("Could not derive a bundle id slug.")
    return result


def pbx_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_text(path: Path, text: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists. Use --force to overwrite scaffold files.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_if_changed(path: Path, text: str) -> bool:
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing == text:
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def replace_text(path: Path, replacements: list[tuple[str, str]]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    original = text
    for before, after in replacements:
        text = text.replace(before, after)
    if text == original:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def project_pbxproj(
    target_name: str,
    display_name: str,
    bundle_id: str,
    deployment_target: str,
    targeted_device_family: str,
) -> str:
    replacements = {
        "__TARGET_NAME__": target_name,
        "__DISPLAY_NAME__": pbx_string(display_name),
        "__BUNDLE_ID__": pbx_string(bundle_id),
        "__DEPLOYMENT_TARGET__": deployment_target,
        "__TARGETED_DEVICE_FAMILY__": targeted_device_family,
    }
    text = PBXPROJ_TEMPLATE
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


def swift_files(app_name: str, target_name: str) -> dict[str, str]:
    app_entry_type = f"{target_name}App"
    return {
        f"{target_name}App.swift": APP_SWIFT_TEMPLATE.replace("__APP_ENTRY_TYPE__", app_entry_type),
        "ContentView.swift": CONTENT_VIEW_TEMPLATE,
        "AppViewModel.swift": APP_VIEW_MODEL_TEMPLATE,
        "Features/AppShell/AppSection.swift": APP_SECTION_TEMPLATE,
        "Features/AppShell/RootTabView.swift": ROOT_TAB_VIEW_TEMPLATE,
        "Features/Onboarding/OnboardingView.swift": ONBOARDING_VIEW_TEMPLATE.replace("__APP_NAME__", app_name),
        "Features/Today/TodayView.swift": TODAY_VIEW_TEMPLATE,
        "Features/Explore/ExploreView.swift": EXPLORE_VIEW_TEMPLATE,
        "Features/Settings/SettingsView.swift": SETTINGS_VIEW_TEMPLATE,
        "Shared/DesignSystem/DesignTokens.swift": DESIGN_TOKENS_TEMPLATE,
        "Shared/Persistence/.gitkeep": "",
    }


def update_metadata(
    repo_root: Path,
    app_name: str,
    target_name: str,
    bundle_id: str,
    project_rel: str,
    source_rel: str,
    platform: str,
) -> bool:
    path = repo_root / ".stitch" / "metadata.json"
    if not path.exists():
        return False
    data = json.loads(path.read_text(encoding="utf-8"))
    app = data.setdefault("app", {})
    app["name"] = app_name
    app["platform"] = "iPhone and iPad" if platform == "iphone-and-ipad" else "iPhone"
    app["framework"] = "SwiftUI"
    app["nativeTarget"] = target_name
    app["nativeTestTarget"] = f"{target_name}Tests"
    app["nativeProjectStatus"] = "created"
    app["nativeProjectPath"] = project_rel
    app["nativeSourceRoot"] = source_rel
    app["nativeProjectContainer"] = f"{target_name}App"
    app["bundleIdentifier"] = bundle_id
    app["appEntryType"] = f"{target_name}App"
    app["nativeDesignSource"] = ".stitch/DESIGN.md"

    maturity = data.get("appMaturity")
    if isinstance(maturity, dict):
        note = maturity.get("note")
        if isinstance(note, str) and "native project not created" in note.lower():
            maturity["note"] = f"Native project scaffold created at {project_rel}; ready for first build/run validation."

    source_of_truth = data.setdefault("sourceOfTruth", {})
    source_of_truth.setdefault("designDocument", ".stitch/DESIGN.md")
    source_of_truth.setdefault("appDocument", ".stitch/APP.md")
    source_of_truth.setdefault("roadmap", ".stitch/ROADMAP.md")
    source_of_truth.setdefault("baton", ".stitch/next-prompt.md")
    source_of_truth.setdefault("bootstrapReceipt", "docs/bootstrap-receipt.md")

    destinations = data.get("nativeDestinations")
    if isinstance(destinations, list):
        for item in destinations:
            if isinstance(item, dict) and isinstance(item.get("path"), str):
                item["path"] = (
                    item["path"]
                    .replace("MyApp/", source_rel)
                    .replace("[NATIVE_SOURCE_ROOT]", source_rel)
                    .replace("[MAIN_TARGET_NAME]/", source_rel)
                    .replace("[MAIN_TARGET_NAME]", target_name)
                )

    core_destinations = [
        {"feature": "App shell", "path": f"{source_rel}Features/AppShell/"},
        {"feature": "Onboarding", "path": f"{source_rel}Features/Onboarding/"},
        {"feature": "Today", "path": f"{source_rel}Features/Today/"},
        {"feature": "Explore", "path": f"{source_rel}Features/Explore/"},
        {"feature": "Settings", "path": f"{source_rel}Features/Settings/"},
        {"feature": "Design system", "path": f"{source_rel}Shared/DesignSystem/"},
        {"feature": "Persistence", "path": f"{source_rel}Shared/Persistence/"},
    ]
    if not isinstance(destinations, list):
        data["nativeDestinations"] = core_destinations
    else:
        existing_features = {
            item.get("feature")
            for item in destinations
            if isinstance(item, dict) and isinstance(item.get("feature"), str)
        }
        for destination in core_destinations:
            if destination["feature"] not in existing_features:
                destinations.append(destination)

    data["nativeScaffold"] = {
        "generator": GENERATOR,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "projectPath": project_rel,
        "sourceRoot": source_rel,
        "target": target_name,
        "plannedTestTarget": f"{target_name}Tests",
        "scheme": target_name,
        "bundleIdentifier": bundle_id,
        "appEntryType": f"{target_name}App",
    }

    setup_run = data.setdefault("setupRun", {})
    setup_run["nativeScaffoldCreated"] = True
    setup_run["nativeTestTarget"] = f"{target_name}Tests"
    setup_run["swiftFilesEdited"] = True

    for risk in data.get("riskRegister", []):
        if isinstance(risk, dict) and risk.get("id") == "risk-native-project-missing":
            risk["status"] = "resolved"
            risk["note"] = f"Native project scaffold created at {project_rel}."

    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return True


def update_memory_files(
    repo_root: Path,
    app_name: str,
    target_name: str,
    bundle_id: str,
    project_rel: str,
    source_rel: str,
) -> list[str]:
    replacements = [
        ("[APP_NAME]", app_name),
        ("[MAIN_TARGET_NAME]", target_name),
        ("[TEST_TARGET_NAME]", f"{target_name}Tests"),
        ("[NATIVE_PROJECT_PATH]", project_rel),
        ("[NATIVE_SOURCE_ROOT]", source_rel),
        ("[BUNDLE_IDENTIFIER]", bundle_id),
        ("[APP_ENTRY_TYPE]", f"{target_name}App"),
        ("`MyApp` until the native project is created or renamed", f"`{target_name}`"),
        ("`MyApp` or an explicitly chosen replacement name", f"`{target_name}`"),
        ("`MyApp` unless intentionally renamed", f"`{target_name}`"),
        ("`MyApp` iOS", f"`{target_name}` iOS"),
        ("Proposed target: `MyApp` unless intentionally renamed", f"Target: `{target_name}`"),
        ("App target: `MyApp` unless renamed during native scaffold", f"App target: `{target_name}`"),
        ("Native project: not present yet", f"Native project: `{project_rel}`"),
        ("Native Xcode project: not present in this repo", f"Native Xcode project: `{project_rel}` created in this repo"),
        ("MyApp/", source_rel),
        ("destination: MyApp native project scaffold and feature folders", f"destination: {source_rel} native project scaffold and feature folders"),
        ("App shell: `MyApp", f"App shell: `{source_rel.rstrip('/')}"),
        ("Build target: `MyApp`", f"Build target: `{target_name}`"),
        ("Main app target: `MyApp`", f"Main app target: `{target_name}`"),
    ]
    files = [
        repo_root / "AGENTS.md",
        repo_root / ".stitch" / "APP.md",
        repo_root / ".stitch" / "ROADMAP.md",
        repo_root / ".stitch" / "next-prompt.md",
        repo_root / "docs" / "app-build-spec.md",
    ]
    changed = []
    for path in files:
        if replace_text(path, replacements):
            changed.append(str(path.relative_to(repo_root)))

    report = f"""# Native Scaffold

- App name: {app_name}
- Target / scheme: {target_name}
- Planned test target: {target_name}Tests
- Bundle id: {bundle_id}
- Project path: {project_rel}
- Source root: {source_rel}
- App entry type: {target_name}App
- Generator: {GENERATOR}
- Created: {datetime.now(timezone.utc).isoformat()}

## Next Validation

1. Confirm the generated scheme with XcodeBuildMCP.
2. Build and run on an iOS Simulator.
3. Record the build/run evidence in `.stitch/metadata.json`.
4. Hand off to `ios-app-director` for APP-001 delivery.
"""
    if write_if_changed(repo_root / "docs" / "native-scaffold.md", report):
        changed.append("docs/native-scaffold.md")
    return changed


def create_scaffold(args: argparse.Namespace) -> dict[str, str | list[str]]:
    repo_root = Path(args.repo_root).expanduser().resolve()
    if not repo_root.exists():
        raise FileNotFoundError(f"Repo root does not exist: {repo_root}")

    app_name = args.app_name.strip()
    target_name = args.target_name.strip() if args.target_name else pascal_identifier(app_name)
    if target_name.lower() in GENERIC_TARGETS:
        raise ValueError(f"Refusing to scaffold with generic target name: {target_name}")

    bundle_id = args.bundle_id.strip() if args.bundle_id else f"{DEFAULT_BUNDLE_PREFIX}.{bundle_slug(target_name)}"
    app_container = f"{target_name}App"
    project_rel = f"{app_container}/{target_name}.xcodeproj"
    source_rel = f"{app_container}/{target_name}/"
    project_root = repo_root / app_container
    source_root = project_root / target_name
    xcodeproj = project_root / f"{target_name}.xcodeproj"
    targeted_device_family = '"1,2"' if args.platform == "iphone-and-ipad" else "1"

    if xcodeproj.exists() and not args.force:
        raise FileExistsError(f"Project already exists: {xcodeproj}. Use --force to overwrite scaffold files.")

    write_text(
        xcodeproj / "project.pbxproj",
        project_pbxproj(target_name, app_name, bundle_id, args.deployment_target, targeted_device_family),
        args.force,
    )
    write_text(
        xcodeproj / "project.xcworkspace" / "contents.xcworkspacedata",
        WORKSPACE_XML,
        args.force,
    )

    for relative_path, text in swift_files(app_name, target_name).items():
        write_text(source_root / relative_path, text, args.force)

    write_text(source_root / "Assets.xcassets" / "Contents.json", ASSET_CATALOG_JSON, args.force)
    write_text(source_root / "Assets.xcassets" / "AccentColor.colorset" / "Contents.json", ACCENT_COLOR_JSON, args.force)
    write_text(source_root / "Assets.xcassets" / "AppIcon.appiconset" / "Contents.json", APP_ICON_JSON, args.force)

    metadata_changed = update_metadata(repo_root, app_name, target_name, bundle_id, project_rel, source_rel, args.platform)
    changed_memory = update_memory_files(repo_root, app_name, target_name, bundle_id, project_rel, source_rel)

    return {
        "appName": app_name,
        "targetName": target_name,
        "plannedTestTarget": f"{target_name}Tests",
        "scheme": target_name,
        "bundleIdentifier": bundle_id,
        "projectPath": str((repo_root / project_rel).resolve()),
        "sourceRoot": str((repo_root / source_rel).resolve()),
        "metadataUpdated": str(metadata_changed),
        "memoryFilesChanged": changed_memory,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a minimal SwiftUI Xcode project for an iOS App Director repo.")
    parser.add_argument("--repo-root", required=True, help="Repo root that contains AGENTS.md, docs, and .stitch.")
    parser.add_argument("--app-name", required=True, help="User-facing app display name.")
    parser.add_argument("--target-name", default="", help="Xcode target/scheme/module name. Derived from app name when omitted.")
    parser.add_argument("--bundle-id", default="", help="Bundle identifier. Derived when omitted.")
    parser.add_argument("--platform", choices=["iphone", "iphone-and-ipad"], default="iphone-and-ipad")
    parser.add_argument("--deployment-target", default="26.0")
    parser.add_argument("--force", action="store_true", help="Overwrite scaffold files when the project already exists.")
    args = parser.parse_args()

    try:
        result = create_scaffold(args)
    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2))
    return 0


PBXPROJ_TEMPLATE = """// !$*UTF8*$!
{
	archiveVersion = 1;
	classes = {
	};
	objectVersion = 77;
	objects = {

/* Begin PBXFileReference section */
		A00000000000000000000009 /* __TARGET_NAME__.app */ = {isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = __TARGET_NAME__.app; sourceTree = BUILT_PRODUCTS_DIR; };
/* End PBXFileReference section */

/* Begin PBXFileSystemSynchronizedRootGroup section */
		A0000000000000000000000B /* __TARGET_NAME__ */ = {
			isa = PBXFileSystemSynchronizedRootGroup;
			path = __TARGET_NAME__;
			sourceTree = "<group>";
		};
/* End PBXFileSystemSynchronizedRootGroup section */

/* Begin PBXFrameworksBuildPhase section */
		A00000000000000000000006 /* Frameworks */ = {
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		};
/* End PBXFrameworksBuildPhase section */

/* Begin PBXGroup section */
		A00000000000000000000001 = {
			isa = PBXGroup;
			children = (
				A0000000000000000000000B /* __TARGET_NAME__ */,
				A0000000000000000000000A /* Products */,
			);
			sourceTree = "<group>";
		};
		A0000000000000000000000A /* Products */ = {
			isa = PBXGroup;
			children = (
				A00000000000000000000009 /* __TARGET_NAME__.app */,
			);
			name = Products;
			sourceTree = "<group>";
		};
/* End PBXGroup section */

/* Begin PBXNativeTarget section */
		A00000000000000000000008 /* __TARGET_NAME__ */ = {
			isa = PBXNativeTarget;
			buildConfigurationList = A00000000000000000000014 /* Build configuration list for PBXNativeTarget "__TARGET_NAME__" */;
			buildPhases = (
				A00000000000000000000005 /* Sources */,
				A00000000000000000000006 /* Frameworks */,
				A00000000000000000000007 /* Resources */,
			);
			buildRules = (
			);
			dependencies = (
			);
			fileSystemSynchronizedGroups = (
				A0000000000000000000000B /* __TARGET_NAME__ */,
			);
			name = __TARGET_NAME__;
			packageProductDependencies = (
			);
			productName = __TARGET_NAME__;
			productReference = A00000000000000000000009 /* __TARGET_NAME__.app */;
			productType = "com.apple.product-type.application";
		};
/* End PBXNativeTarget section */

/* Begin PBXProject section */
		A00000000000000000000002 /* Project object */ = {
			isa = PBXProject;
			attributes = {
				BuildIndependentTargetsInParallel = 1;
				LastSwiftUpdateCheck = 2640;
				LastUpgradeCheck = 2640;
				TargetAttributes = {
					A00000000000000000000008 = {
						CreatedOnToolsVersion = 26.4;
					};
				};
			};
			buildConfigurationList = A00000000000000000000013 /* Build configuration list for PBXProject "__TARGET_NAME__" */;
			developmentRegion = en;
			hasScannedForEncodings = 0;
			knownRegions = (
				en,
				Base,
			);
			mainGroup = A00000000000000000000001;
			minimizedProjectReferenceProxies = 1;
			preferredProjectObjectVersion = 77;
			productRefGroup = A0000000000000000000000A /* Products */;
			projectDirPath = "";
			projectRoot = "";
			targets = (
				A00000000000000000000008 /* __TARGET_NAME__ */,
			);
		};
/* End PBXProject section */

/* Begin PBXResourcesBuildPhase section */
		A00000000000000000000007 /* Resources */ = {
			isa = PBXResourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		};
/* End PBXResourcesBuildPhase section */

/* Begin PBXSourcesBuildPhase section */
		A00000000000000000000005 /* Sources */ = {
			isa = PBXSourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		};
/* End PBXSourcesBuildPhase section */

/* Begin XCBuildConfiguration section */
		A0000000000000000000000F /* Debug */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ALWAYS_SEARCH_USER_PATHS = NO;
				ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS = YES;
				CLANG_ANALYZER_NONNULL = YES;
				CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE;
				CLANG_CXX_LANGUAGE_STANDARD = "gnu++20";
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CLANG_ENABLE_OBJC_WEAK = YES;
				CLANG_WARN_BLOCK_CAPTURE_AUTORELEASING = YES;
				CLANG_WARN_BOOL_CONVERSION = YES;
				CLANG_WARN_COMMA = YES;
				CLANG_WARN_CONSTANT_CONVERSION = YES;
				CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS = YES;
				CLANG_WARN_DIRECT_OBJC_ISA_USAGE = YES_ERROR;
				CLANG_WARN_DOCUMENTATION_COMMENTS = YES;
				CLANG_WARN_EMPTY_BODY = YES;
				CLANG_WARN_ENUM_CONVERSION = YES;
				CLANG_WARN_INFINITE_RECURSION = YES;
				CLANG_WARN_INT_CONVERSION = YES;
				CLANG_WARN_NON_LITERAL_NULL_CONVERSION = YES;
				CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF = YES;
				CLANG_WARN_OBJC_LITERAL_CONVERSION = YES;
				CLANG_WARN_OBJC_ROOT_CLASS = YES_ERROR;
				CLANG_WARN_QUOTED_INCLUDE_IN_FRAMEWORK_HEADER = YES;
				CLANG_WARN_RANGE_LOOP_ANALYSIS = YES;
				CLANG_WARN_STRICT_PROTOTYPES = YES;
				CLANG_WARN_SUSPICIOUS_MOVE = YES;
				CLANG_WARN_UNGUARDED_AVAILABILITY = YES_AGGRESSIVE;
				CLANG_WARN_UNREACHABLE_CODE = YES;
				CLANG_WARN__DUPLICATE_METHOD_MATCH = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = dwarf;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				ENABLE_TESTABILITY = YES;
				ENABLE_USER_SCRIPT_SANDBOXING = YES;
				GCC_C_LANGUAGE_STANDARD = gnu17;
				GCC_DYNAMIC_NO_PIC = NO;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_OPTIMIZATION_LEVEL = 0;
				GCC_PREPROCESSOR_DEFINITIONS = (
					"DEBUG=1",
					"$(inherited)",
				);
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				IPHONEOS_DEPLOYMENT_TARGET = __DEPLOYMENT_TARGET__;
				LOCALIZATION_PREFERS_STRING_CATALOGS = YES;
				MTL_ENABLE_DEBUG_INFO = INCLUDE_SOURCE;
				MTL_FAST_MATH = YES;
				ONLY_ACTIVE_ARCH = YES;
				SDKROOT = iphoneos;
				SWIFT_ACTIVE_COMPILATION_CONDITIONS = "DEBUG $(inherited)";
				SWIFT_OPTIMIZATION_LEVEL = "-Onone";
			};
			name = Debug;
		};
		A00000000000000000000010 /* Release */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ALWAYS_SEARCH_USER_PATHS = NO;
				ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS = YES;
				CLANG_ANALYZER_NONNULL = YES;
				CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE;
				CLANG_CXX_LANGUAGE_STANDARD = "gnu++20";
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CLANG_ENABLE_OBJC_WEAK = YES;
				CLANG_WARN_BLOCK_CAPTURE_AUTORELEASING = YES;
				CLANG_WARN_BOOL_CONVERSION = YES;
				CLANG_WARN_COMMA = YES;
				CLANG_WARN_CONSTANT_CONVERSION = YES;
				CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS = YES;
				CLANG_WARN_DIRECT_OBJC_ISA_USAGE = YES_ERROR;
				CLANG_WARN_DOCUMENTATION_COMMENTS = YES;
				CLANG_WARN_EMPTY_BODY = YES;
				CLANG_WARN_ENUM_CONVERSION = YES;
				CLANG_WARN_INFINITE_RECURSION = YES;
				CLANG_WARN_INT_CONVERSION = YES;
				CLANG_WARN_NON_LITERAL_NULL_CONVERSION = YES;
				CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF = YES;
				CLANG_WARN_OBJC_LITERAL_CONVERSION = YES;
				CLANG_WARN_OBJC_ROOT_CLASS = YES_ERROR;
				CLANG_WARN_QUOTED_INCLUDE_IN_FRAMEWORK_HEADER = YES;
				CLANG_WARN_RANGE_LOOP_ANALYSIS = YES;
				CLANG_WARN_STRICT_PROTOTYPES = YES;
				CLANG_WARN_SUSPICIOUS_MOVE = YES;
				CLANG_WARN_UNGUARDED_AVAILABILITY = YES_AGGRESSIVE;
				CLANG_WARN_UNREACHABLE_CODE = YES;
				CLANG_WARN__DUPLICATE_METHOD_MATCH = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = "dwarf-with-dsym";
				ENABLE_NS_ASSERTIONS = NO;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				ENABLE_USER_SCRIPT_SANDBOXING = YES;
				GCC_C_LANGUAGE_STANDARD = gnu17;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				IPHONEOS_DEPLOYMENT_TARGET = __DEPLOYMENT_TARGET__;
				LOCALIZATION_PREFERS_STRING_CATALOGS = YES;
				MTL_ENABLE_DEBUG_INFO = NO;
				MTL_FAST_MATH = YES;
				SDKROOT = iphoneos;
				SWIFT_COMPILATION_MODE = wholemodule;
				VALIDATE_PRODUCT = YES;
			};
			name = Release;
		};
		A00000000000000000000011 /* Debug */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				ENABLE_PREVIEWS = YES;
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_KEY_CFBundleDisplayName = __DISPLAY_NAME__;
				INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES;
				INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents = YES;
				INFOPLIST_KEY_UILaunchScreen_Generation = YES;
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad = "UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone = "UIInterfaceOrientationPortrait UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				IPHONEOS_DEPLOYMENT_TARGET = __DEPLOYMENT_TARGET__;
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = __BUNDLE_ID__;
				PRODUCT_NAME = "$(TARGET_NAME)";
				STRING_CATALOG_GENERATE_SYMBOLS = YES;
				SWIFT_APPROACHABLE_CONCURRENCY = YES;
				SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor;
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_STRICT_CONCURRENCY = complete;
				SWIFT_UPCOMING_FEATURE_MEMBER_IMPORT_VISIBILITY = YES;
				SWIFT_VERSION = 6.0;
				TARGETED_DEVICE_FAMILY = __TARGETED_DEVICE_FAMILY__;
			};
			name = Debug;
		};
		A00000000000000000000012 /* Release */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				ENABLE_PREVIEWS = YES;
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_KEY_CFBundleDisplayName = __DISPLAY_NAME__;
				INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES;
				INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents = YES;
				INFOPLIST_KEY_UILaunchScreen_Generation = YES;
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad = "UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone = "UIInterfaceOrientationPortrait UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				IPHONEOS_DEPLOYMENT_TARGET = __DEPLOYMENT_TARGET__;
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = __BUNDLE_ID__;
				PRODUCT_NAME = "$(TARGET_NAME)";
				STRING_CATALOG_GENERATE_SYMBOLS = YES;
				SWIFT_APPROACHABLE_CONCURRENCY = YES;
				SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor;
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_STRICT_CONCURRENCY = complete;
				SWIFT_UPCOMING_FEATURE_MEMBER_IMPORT_VISIBILITY = YES;
				SWIFT_VERSION = 6.0;
				TARGETED_DEVICE_FAMILY = __TARGETED_DEVICE_FAMILY__;
			};
			name = Release;
		};
/* End XCBuildConfiguration section */

/* Begin XCConfigurationList section */
		A00000000000000000000013 /* Build configuration list for PBXProject "__TARGET_NAME__" */ = {
			isa = XCConfigurationList;
			buildConfigurations = (
				A0000000000000000000000F /* Debug */,
				A00000000000000000000010 /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		};
		A00000000000000000000014 /* Build configuration list for PBXNativeTarget "__TARGET_NAME__" */ = {
			isa = XCConfigurationList;
			buildConfigurations = (
				A00000000000000000000011 /* Debug */,
				A00000000000000000000012 /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		};
/* End XCConfigurationList section */
	};
	rootObject = A00000000000000000000002 /* Project object */;
}
"""


WORKSPACE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Workspace
   version = "1.0">
   <FileRef
      location = "self:">
   </FileRef>
</Workspace>
"""


APP_SWIFT_TEMPLATE = """import SwiftUI

@main
struct __APP_ENTRY_TYPE__: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
"""


CONTENT_VIEW_TEMPLATE = """import SwiftUI

struct ContentView: View {
    @State private var viewModel = AppViewModel()

    var body: some View {
        if viewModel.didCompleteOnboarding {
            RootTabView(viewModel: viewModel)
        } else {
            OnboardingView(viewModel: viewModel)
        }
    }
}

#Preview {
    ContentView()
}
"""


APP_VIEW_MODEL_TEMPLATE = """import Foundation
import Observation

@Observable
@MainActor
final class AppViewModel {
    var didCompleteOnboarding = false

    func completeOnboarding() {
        didCompleteOnboarding = true
    }
}
"""


APP_SECTION_TEMPLATE = """import SwiftUI

enum AppSection: String, CaseIterable, Identifiable {
    case today
    case explore
    case settings

    var id: String { rawValue }

    var title: String {
        switch self {
        case .today:
            "Today"
        case .explore:
            "Explore"
        case .settings:
            "Settings"
        }
    }

    var symbolName: String {
        switch self {
        case .today:
            "sparkles"
        case .explore:
            "square.grid.2x2"
        case .settings:
            "gearshape"
        }
    }
}
"""


ROOT_TAB_VIEW_TEMPLATE = """import SwiftUI

struct RootTabView: View {
    let viewModel: AppViewModel
    @State private var selectedSection: AppSection = .today

    var body: some View {
        TabView(selection: $selectedSection) {
            TodayView()
                .tabItem {
                    Label(AppSection.today.title, systemImage: AppSection.today.symbolName)
                }
                .tag(AppSection.today)

            ExploreView()
                .tabItem {
                    Label(AppSection.explore.title, systemImage: AppSection.explore.symbolName)
                }
                .tag(AppSection.explore)

            SettingsView()
                .tabItem {
                    Label(AppSection.settings.title, systemImage: AppSection.settings.symbolName)
                }
                .tag(AppSection.settings)
        }
        .tint(DesignTokens.accent)
    }
}

#Preview {
    RootTabView(viewModel: AppViewModel())
}
"""


ONBOARDING_VIEW_TEMPLATE = """import SwiftUI

struct OnboardingView: View {
    let viewModel: AppViewModel

    var body: some View {
        NavigationStack {
            VStack(alignment: .leading, spacing: 24) {
                Spacer()

                Image(systemName: "sparkles.rectangle.stack.fill")
                    .font(.system(size: 52, weight: .semibold))
                    .foregroundStyle(DesignTokens.accent)

                VStack(alignment: .leading, spacing: 10) {
                    Text("__APP_NAME__")
                        .font(.largeTitle.weight(.bold))

                    Text("Start with a clean native shell, then let the roadmap turn design evidence into real SwiftUI features.")
                        .font(.title3)
                        .foregroundStyle(.secondary)
                        .fixedSize(horizontal: false, vertical: true)
                }

                Spacer()

                Button {
                    viewModel.completeOnboarding()
                } label: {
                    Label("Begin", systemImage: "arrow.right")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.borderedProminent)
                .controlSize(.large)
            }
            .padding(28)
            .background(DesignTokens.background)
        }
    }
}

#Preview {
    OnboardingView(viewModel: AppViewModel())
}
"""


TODAY_VIEW_TEMPLATE = """import SwiftUI

struct TodayView: View {
    var body: some View {
        NavigationStack {
            List {
                Section {
                    VStack(alignment: .leading, spacing: 12) {
                        Label("Today's starting point", systemImage: "sparkle.magnifyingglass")
                            .font(.headline)

                        Text("Use this tab for the first daily-use workflow once the feature map is ready.")
                            .foregroundStyle(.secondary)
                    }
                    .padding(.vertical, 8)
                }

                Section("Starter surfaces") {
                    Label("Primary action", systemImage: "bolt")
                    Label("Recent state", systemImage: "clock")
                    Label("Suggested next step", systemImage: "arrow.up.right.circle")
                }
            }
            .navigationTitle("Today")
        }
    }
}

#Preview {
    TodayView()
}
"""


EXPLORE_VIEW_TEMPLATE = """import SwiftUI

struct ExploreView: View {
    var body: some View {
        NavigationStack {
            VStack(spacing: 18) {
                Image(systemName: "square.grid.2x2")
                    .font(.system(size: 48, weight: .medium))
                    .foregroundStyle(DesignTokens.accent)

                Text("Explore will become the home for the app-specific feature surfaces chosen from the roadmap.")
                    .font(.title3)
                    .multilineTextAlignment(.center)
                    .foregroundStyle(.secondary)
                    .padding(.horizontal)
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .background(DesignTokens.background)
            .navigationTitle("Explore")
        }
    }
}

#Preview {
    ExploreView()
}
"""


SETTINGS_VIEW_TEMPLATE = """import SwiftUI

struct SettingsView: View {
    var body: some View {
        NavigationStack {
            List {
                Section("Project") {
                    Label("Design system", systemImage: "paintpalette")
                    Label("Data and privacy", systemImage: "lock.shield")
                    Label("Build readiness", systemImage: "checkmark.seal")
                }
            }
            .navigationTitle("Settings")
        }
    }
}

#Preview {
    SettingsView()
}
"""


DESIGN_TOKENS_TEMPLATE = """import SwiftUI

enum DesignTokens {
    static let accent = Color(red: 0.20, green: 0.48, blue: 0.94)
    static let background = Color(.systemGroupedBackground)
}
"""


ASSET_CATALOG_JSON = """{
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
"""


ACCENT_COLOR_JSON = """{
  "colors" : [
    {
      "idiom" : "universal"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
"""


APP_ICON_JSON = """{
  "images" : [
    {
      "idiom" : "universal",
      "platform" : "ios",
      "size" : "1024x1024"
    },
    {
      "appearances" : [
        {
          "appearance" : "luminosity",
          "value" : "dark"
        }
      ],
      "idiom" : "universal",
      "platform" : "ios",
      "size" : "1024x1024"
    },
    {
      "appearances" : [
        {
          "appearance" : "luminosity",
          "value" : "tinted"
        }
      ],
      "idiom" : "universal",
      "platform" : "ios",
      "size" : "1024x1024"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
"""


if __name__ == "__main__":
    raise SystemExit(main())
