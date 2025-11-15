import sys
from rich.console import Console
from rich.panel import Panel

from utils import (
    load_yaml,
    sanitize_openapi,
    normalize_schema_structure,
    dict_diff_keys,
    compare_schema_details
)

console = Console()

# Markdown flag
IS_MARKDOWN = "--markdown" in sys.argv
IS_BREAKING_ONLY = "--breaking" in sys.argv

def out(text):
    # Filter non-breaking content when --breaking is active
    if IS_BREAKING_ONLY:
        # Do not show added lines or non-breaking modifications
        if (
            text.startswith("[green]+")
            or text.startswith("+ ")
            or text.startswith("### Added")
            or text.startswith("### Modified")
            or text.startswith("    [green]+")
            or ("Added response" in text)
        ):
            return  # skip non-breaking changes

        # For schema/response deep diff lines
        if "Added" in text and "response" not in text:
            return

        if "Modified" in text:
            if not is_breaking_line(text):
                return

    # Markdown mode
    if IS_MARKDOWN:
        clean = (
            text.replace("[green]", "")
                .replace("[/green]", "")
                .replace("[red]", "")
                .replace("[/red]", "")
                .replace("[yellow]", "")
                .replace("[/yellow]", "")
                .replace("[cyan]", "")
                .replace("[/cyan]", "")
                .replace("[bold]", "")
                .replace("[/bold]", "")
        )
        print(clean)
    else:
        console.print(text)



# ------------------------------------------------------------------------------
# VERSION CHANGE TRACKER
# ------------------------------------------------------------------------------

changes = {
    "major": 0,
    "minor": 0,
    "patch": 0
}


def determine_version_bump(changes):
    if changes["major"] > 0:
        return "major"
    if changes["minor"] > 0:
        return "minor"
    return "patch"


# ------------------------------------------------------------------------------
# PATH DIFF
# ------------------------------------------------------------------------------

def compare_paths(old, new):
    out("\n")
    out("## Paths\n")

    old_paths = old.get("paths", {})
    new_paths = new.get("paths", {})

    added, removed, common = dict_diff_keys(old_paths, new_paths)

    out("### Added")
    for p in added:
        out(f"[green]+ {p}")
        changes["minor"] += 1

    out("\n### Removed")
    for p in removed:
        out(f"[red]- {p}")
        changes["major"] += 1

    out("\n### Modified")
    for p in common:
        if old_paths[p] != new_paths[p]:
            out(f"[yellow]* {p}")
            changes["patch"] += 1


# ------------------------------------------------------------------------------
# SCHEMA DIFF
# ------------------------------------------------------------------------------

def compare_schemas(old, new):
    out("\n## Schemas\n")

    old_components = old.get("components", {}).get("schemas", {})
    new_components = new.get("components", {}).get("schemas", {})

    added, removed, common = dict_diff_keys(old_components, new_components)

    out("### Added")
    for s in added:
        out(f"[green]+ {s}")
        changes["minor"] += 1

    out("\n### Removed")
    for s in removed:
        out(f"[red]- {s}")
        changes["major"] += 1

    out("\n### Modified")
    for s in common:
        if old_components[s] != new_components[s]:
            out(f"[yellow]* {s}[/yellow]")

            details = compare_schema_details(
                old_components[s],
                new_components[s],
                s
            )

            for line in details:
                out("    " + line)

                # Changes impact
                if line.startswith("[red]-"):
                    changes["major"] += 1
                elif "→" in line or "type:" in line:
                    changes["major"] += 1
                elif line.startswith("[green]+"):
                    changes["minor"] += 1
                else:
                    changes["patch"] += 1


# ------------------------------------------------------------------------------
# RESPONSE DIFF (NEW FEATURE)
# ------------------------------------------------------------------------------

def compare_responses(old, new):
    out("\n## Responses\n")

    old_paths = old.get("paths", {})
    new_paths = new.get("paths", {})

    for path, old_item in old_paths.items():
        if path not in new_paths:
            continue

        new_item = new_paths[path]

        for method, old_method in old_item.items():
            if method not in new_item:
                continue

            new_method = new_item[method]

            old_res = old_method.get("responses", {})
            new_res = new_method.get("responses", {})

            added, removed, common = dict_diff_keys(old_res, new_res)

            if added or removed or any(
                old_res[c] != new_res[c] for c in common
            ):
                out(f"[cyan]{path} [{method.upper()}][/cyan]")

            for code in added:
                out(f"    [green]+ Added response {code}")
                changes["minor"] += 1

            for code in removed:
                out(f"    [red]- Removed response {code}")
                changes["major"] += 1

            for code in common:
                if old_res[code] != new_res[code]:
                    out(f"    [yellow]~ Modified response {code}[/yellow]")
                    details = compare_schema_details(
                        old_res[code],
                        new_res[code],
                        f"{path}::{method}::{code}"
                    )
                    for line in details:
                        out("       " + line)

def is_breaking_line(line: str) -> bool:
    """
    Determine if a diff line should appear in breaking-only mode.
    """
    # Removed items
    if line.startswith("[red]-"):
        return True

    # Type changes
    if "→" in line or "type:" in line:
        return True

    # Response removed
    if "Removed response" in line:
        return True

    return False


# ------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        console.print("Usage: python compare.py old.yaml new.yaml [--markdown]")
        sys.exit(1)

    old_file = sys.argv[1]
    new_file = sys.argv[2]

    out(f"# OpenAPI Diff Tool\n")
    out(f"Comparing:\n- {old_file}\n- {new_file}\n")

    old_yaml = normalize_schema_structure(
        sanitize_openapi(load_yaml(old_file))
    )
    new_yaml = normalize_schema_structure(
        sanitize_openapi(load_yaml(new_file))
    )

    compare_paths(old_yaml, new_yaml)
    compare_schemas(old_yaml, new_yaml)
    compare_responses(old_yaml, new_yaml)

    bump = determine_version_bump(changes)
    out("\n")
    out(f"## Suggested version bump: **{bump.upper()}**")


if __name__ == "__main__":
    main()
