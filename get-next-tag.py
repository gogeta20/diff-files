#!/usr/bin/env python3
"""
Get next tag version based on current SDK tag and release notes.

Usage:
    python3 get-next-tag.py [release_version]

Example:
    python3 get-next-tag.py v1.3.0
    python3 get-next-tag.py          # Auto-detect latest release
"""

import os
import re
import sys
import subprocess
from pathlib import Path

# Paths
SDK_REPO = Path.home() / "projects" / "jotelulu" / "php-bundle-client-hal-dns"
RELEASES_DIR = Path(__file__).parent / "releases"


def get_current_tag():
    """Get the latest tag from SDK repo."""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=SDK_REPO,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def parse_version(tag):
    """Parse version string into (major, minor, patch)."""
    # Remove 'v' prefix if present
    tag = tag.lstrip('v')
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)', tag)
    if match:
        return tuple(map(int, match.groups()))
    return None


def get_bump_type(release_version):
    """Read bump type from RELEASE-NOTES.md."""
    release_dir = RELEASES_DIR / release_version
    release_notes = release_dir / "RELEASE-NOTES.md"

    if not release_notes.exists():
        print(f"❌ Error: {release_notes} not found")
        return None

    with open(release_notes, 'r') as f:
        content = f.read()

    # Look for line like: "🟡 **Type:** MINOR (New features, backward compatible)"
    match = re.search(r'\*\*Type:\*\*\s+(MAJOR|MINOR|PATCH)', content, re.IGNORECASE)
    if match:
        return match.group(1).upper()

    return None


def calculate_next_version(current_version, bump_type):
    """Calculate next version based on bump type."""
    major, minor, patch = current_version

    if bump_type == "MAJOR":
        return (major + 1, 0, 0)
    elif bump_type == "MINOR":
        return (major, minor + 1, 0)
    elif bump_type == "PATCH":
        return (major, minor, patch + 1)
    else:
        return None


def find_latest_release():
    """Find the latest release directory."""
    if not RELEASES_DIR.exists():
        return None

    releases = [d.name for d in RELEASES_DIR.iterdir() if d.is_dir()]
    if not releases:
        return None

    # Sort by version (assumes vX.Y.Z format)
    releases.sort(key=lambda x: [int(n) for n in x.lstrip('v').split('.')])
    return releases[-1]


def main():
    print("=" * 60)
    print("🏷️  Next Tag Calculator")
    print("=" * 60)
    print()

    # Get release version (from args or auto-detect)
    if len(sys.argv) > 1:
        release_version = sys.argv[1]
    else:
        release_version = find_latest_release()
        if not release_version:
            print("❌ Error: No releases found in releases/")
            print("   Create a release folder first (e.g., releases/v1.3.0/)")
            sys.exit(1)
        print(f"📦 Auto-detected release: {release_version}")
        print()

    # Get current tag from SDK repo
    current_tag = get_current_tag()
    if not current_tag:
        print("❌ Error: No tags found in SDK repo")
        print(f"   Location: {SDK_REPO}")
        sys.exit(1)

    current_version = parse_version(current_tag)
    if not current_version:
        print(f"❌ Error: Invalid tag format: {current_tag}")
        sys.exit(1)

    print(f"📍 Current SDK tag: {current_tag}")
    print(f"   Version: {'.'.join(map(str, current_version))}")
    print()

    # Get bump type from release notes
    bump_type = get_bump_type(release_version)
    if not bump_type:
        print(f"❌ Error: Could not determine bump type from release notes")
        print(f"   Location: {RELEASES_DIR / release_version / 'RELEASE-NOTES.md'}")
        sys.exit(1)

    # Determine emoji and description
    bump_emoji = {
        "MAJOR": "🔴",
        "MINOR": "🟡",
        "PATCH": "✅"
    }
    bump_desc = {
        "MAJOR": "Breaking changes",
        "MINOR": "New features (backward compatible)",
        "PATCH": "Bug fixes"
    }

    print(f"{bump_emoji.get(bump_type, '❓')} Bump type: {bump_type}")
    print(f"   Description: {bump_desc.get(bump_type, 'Unknown')}")
    print()

    # Calculate next version
    next_version = calculate_next_version(current_version, bump_type)
    if not next_version:
        print(f"❌ Error: Could not calculate next version")
        sys.exit(1)

    next_tag = '.'.join(map(str, next_version))

    print("─" * 60)
    print()
    print(f"✨ Next tag: {next_tag}")
    print()
    print("=" * 60)
    print()

    # Show command to create tag
    print("📝 Next steps:")
    print()
    print(f"   1. Generate release files:")
    print(f"      python3 generate-release-files.py {release_version}")
    print()
    print(f"   2. Review generated files in:")
    print(f"      {RELEASES_DIR / release_version}/")
    print()
    print(f"   3. Apply changes to SDK repo")
    print(f"   4. Create tag: git tag -a {next_tag}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
