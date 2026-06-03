#!/usr/bin/env python3
"""
validate_site.py

Validates the MkDocs site structure:
  1. Parses mkdocs.yml to find all nav file references.
  2. Checks each referenced file exists in docs/.
  3. Checks no referenced file is shorter than 100 characters.
  4. Checks that site/ directory exists and contains index.html (if the site has been built).
  5. Prints PASS or FAIL with detail for each check.
  6. Exits with code 1 if any check fails, 0 if all pass.
"""

import os
import sys
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MKDOCS_YML = os.path.join(BASE_DIR, "mkdocs.yml")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
SITE_DIR = os.path.join(BASE_DIR, "site")

failures = []
passes = []


def result(label: str, passed: bool, detail: str = "") -> None:
    tag = "PASS" if passed else "FAIL"
    msg = f"[{tag}] {label}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    if passed:
        passes.append(label)
    else:
        failures.append(label)


def collect_nav_files(nav_entry, files=None):
    """Recursively walk the nav structure and collect all .md file paths."""
    if files is None:
        files = []
    if isinstance(nav_entry, str):
        files.append(nav_entry)
    elif isinstance(nav_entry, dict):
        for value in nav_entry.values():
            collect_nav_files(value, files)
    elif isinstance(nav_entry, list):
        for item in nav_entry:
            collect_nav_files(item, files)
    return files


def check_mkdocs_yml_exists():
    exists = os.path.isfile(MKDOCS_YML)
    result("mkdocs.yml exists", exists, MKDOCS_YML if not exists else "")
    return exists


def _make_permissive_loader():
    """Return a YAML Loader that treats unknown tags (e.g. !!python/name:…)
    as plain scalars instead of raising a ConstructorError."""
    class PermissiveLoader(yaml.SafeLoader):
        pass

    def _ignore_unknown_tag(loader, tag_suffix, node):
        if isinstance(node, yaml.ScalarNode):
            return loader.construct_scalar(node)
        if isinstance(node, yaml.SequenceNode):
            return loader.construct_sequence(node)
        return loader.construct_mapping(node)

    PermissiveLoader.add_multi_constructor("", _ignore_unknown_tag)
    return PermissiveLoader


def load_mkdocs_yml():
    try:
        with open(MKDOCS_YML, "r", encoding="utf-8") as fh:
            config = yaml.load(fh, Loader=_make_permissive_loader())
        result("mkdocs.yml is valid YAML", True)
        return config
    except yaml.YAMLError as exc:
        result("mkdocs.yml is valid YAML", False, str(exc))
        return None


def check_nav_files(config):
    nav = config.get("nav", [])
    if not nav:
        result("nav section present in mkdocs.yml", False, "nav key is empty or missing")
        return []
    result("nav section present in mkdocs.yml", True)

    nav_files = collect_nav_files(nav)

    # Deduplicate while preserving order
    seen = set()
    unique_files = []
    for f in nav_files:
        if f not in seen:
            seen.add(f)
            unique_files.append(f)

    print(f"\n  Found {len(unique_files)} unique file references in nav.\n")

    missing = []
    too_short = []

    for rel_path in unique_files:
        full_path = os.path.join(DOCS_DIR, rel_path)

        # --- existence check ---
        if not os.path.isfile(full_path):
            result(f"File exists: {rel_path}", False, f"Not found at {full_path}")
            missing.append(rel_path)
            continue

        result(f"File exists: {rel_path}", True)

        # --- minimum length check ---
        try:
            size = os.path.getsize(full_path)
            if size < 100:
                result(
                    f"File length >= 100 chars: {rel_path}",
                    False,
                    f"Only {size} bytes",
                )
                too_short.append(rel_path)
            else:
                result(f"File length >= 100 chars: {rel_path}", True, f"{size} bytes")
        except OSError as exc:
            result(f"File length >= 100 chars: {rel_path}", False, str(exc))
            too_short.append(rel_path)

    return unique_files


def check_site_built():
    """Check whether the built site directory exists and contains index.html."""
    site_exists = os.path.isdir(SITE_DIR)
    if not site_exists:
        result(
            "Built site/ directory exists",
            False,
            "Run 'make build' first to generate the site.",
        )
        return

    result("Built site/ directory exists", True)

    index_html = os.path.join(SITE_DIR, "index.html")
    result(
        "site/index.html exists",
        os.path.isfile(index_html),
        "" if os.path.isfile(index_html) else "Missing — site may not have built correctly.",
    )


def main():
    print("=" * 60)
    print("MkDocs Site Validator")
    print(f"Base directory : {BASE_DIR}")
    print(f"Docs directory : {DOCS_DIR}")
    print(f"Site directory : {SITE_DIR}")
    print("=" * 60)
    print()

    # 1. Check mkdocs.yml exists
    if not check_mkdocs_yml_exists():
        print("\nCannot continue without mkdocs.yml.")
        sys.exit(1)

    # 2. Load and validate YAML
    config = load_mkdocs_yml()
    if config is None:
        print("\nCannot continue with invalid YAML.")
        sys.exit(1)

    # 3. Check nav files exist and are long enough
    check_nav_files(config)

    # 4. Check built site (non-blocking — only relevant after 'make build')
    print()
    check_site_built()

    # Summary
    print()
    print("=" * 60)
    print(f"SUMMARY: {len(passes)} passed, {len(failures)} failed")
    if failures:
        print("\nFailed checks:")
        for f in failures:
            print(f"  - {f}")
        print()
        sys.exit(1)
    else:
        print("\nAll checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
