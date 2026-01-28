#!/usr/bin/env python3
"""
Generate release files for SDK based on RELEASE-NOTES.md

Usage:
    python3 generate-release-files.py [release_version]

Example:
    python3 generate-release-files.py v1.3.0
    python3 generate-release-files.py          # Auto-detect latest release
"""

import os
import re
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Paths
SDK_REPO = Path.home() / "projects" / "jotelulu" / "php-bundle-client-hal-dns"
RELEASES_DIR = Path(__file__).parent / "releases"


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


def parse_release_notes(release_version):
    """Parse RELEASE-NOTES.md and extract key information."""
    release_dir = RELEASES_DIR / release_version
    release_notes = release_dir / "RELEASE-NOTES.md"

    if not release_notes.exists():
        print(f"❌ Error: {release_notes} not found")
        return None

    with open(release_notes, 'r') as f:
        content = f.read()

    data = {
        'version': release_version.lstrip('v'),
        'version_with_v': release_version,
    }

    # Extract date
    match = re.search(r'\*\*Date:\*\*\s+(\d{4}-\d{2}-\d{2})', content)
    data['date'] = match.group(1) if match else datetime.now().strftime('%Y-%m-%d')

    # Extract previous tag
    match = re.search(r'\*\*Previous Tag:\*\*\s+(v?[\d.]+)', content)
    data['previous_tag'] = match.group(1) if match else 'unknown'

    # Extract type
    match = re.search(r'\*\*Type:\*\*\s+(🔴|🟡|✅)?\s*(MAJOR|MINOR|PATCH)', content)
    data['type'] = match.group(2).upper() if match else 'MINOR'
    data['type_emoji'] = match.group(1) if match and match.group(1) else '🟡'

    # Extract summary
    match = re.search(r'## 📋 Summary\s+(.*?)(?=\n##|\Z)', content, re.DOTALL)
    data['summary'] = match.group(1).strip() if match else ''

    # Extract branch
    match = re.search(r'\*\*NEW \(current\):\*\*\s+`([^`]+)`', content)
    data['branch'] = match.group(1) if match else 'unknown'

    # Extract detailed changes section
    match = re.search(r'## 📊 Detailed Changes\s+(.*?)(?=\n##|\Z)', content, re.DOTALL)
    data['detailed_changes'] = match.group(1).strip() if match else ''

    return data


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


def generate_changelog(data, current_changelog_path):
    """Generate updated CHANGELOG.md"""
    # Read current changelog
    with open(current_changelog_path, 'r') as f:
        current_content = f.read()

    # Parse summary to extract changes
    summary = data['summary']

    # Default entry
    added = []
    changed = []
    removed = []

    # Try to extract specific changes from summary
    if 'added' in summary.lower() or 'new' in summary.lower():
        # Extract what was added
        if '404 response' in summary.lower():
            added.append(f"Response 404 to `/api/zones/import` endpoint for cluster not found errors")
        elif 'endpoint' in summary.lower():
            added.append(summary.split('.')[0])

    # Build the new entry
    new_entry = f"""## [{data['version']}] - {data['date']}

### Added
"""
    if added:
        for item in added:
            new_entry += f"- {item}\n"
    else:
        new_entry += "- N/A\n"

    new_entry += """
### Changed
"""
    if changed:
        for item in changed:
            new_entry += f"- {item}\n"
    else:
        new_entry += "- N/A\n"

    new_entry += """
### Removed
"""
    if removed:
        for item in removed:
            new_entry += f"- {item}\n"
    else:
        new_entry += "- N/A\n"

    new_entry += "\n"

    # Insert new entry after "# Changelog" header
    updated_content = current_content.replace(
        "# Changelog\n",
        f"# Changelog\n\n{new_entry}",
        1
    )

    return updated_content


def generate_readme(data, current_readme_path):
    """Generate updated README.md"""
    with open(current_readme_path, 'r') as f:
        content = f.read()

    old_version = data['previous_tag'].lstrip('v')
    new_version = data['version']

    # Extract major.minor from versions
    old_major_minor = '.'.join(old_version.split('.')[:2])
    new_major_minor = '.'.join(new_version.split('.')[:2])

    # Update version references
    # Pattern 1: ^X.Y format in composer require
    content = re.sub(
        r'(composer require jotelulu/php-bundle-client-hal-dns:)\^\d+\.\d+',
        rf'\1^{new_major_minor}',
        content
    )

    # Pattern 2: Exact version X.Y.Z in text
    content = re.sub(
        rf'\b{re.escape(old_version)}\b',
        new_version,
        content
    )

    # Pattern 3: Version comments (current version (`X.Y.Z`))
    content = re.sub(
        r'\(current version \(`[\d.]+`\)\)',
        f'(current version (`{new_version}`))',
        content
    )

    # Pattern 4: "current version (`X.Y.Z`)" or similar
    content = re.sub(
        r'current version \(`[\d.]+`\)',
        f'current version (`{new_version}`)',
        content
    )

    return content


def generate_commit_message(data):
    """Generate commit message for the release."""
    # Extract JIRA ticket from branch if present
    ticket = ""
    if 'PROD-' in data['branch']:
        match = re.search(r'(PROD-\d+)', data['branch'])
        ticket = match.group(1) if match else ""

    if not ticket:
        ticket = "RELEASE"

    # Build commit message
    msg = f"""{ticket}: Prepare {data['version']} release

{data['summary'].split('.')[0] if data['summary'] else 'Release ' + data['version']}

Updated README.md and CHANGELOG.md

made: mau"""

    return msg


def generate_tag_message(data):
    """Generate tag annotation message."""
    msg = f"""Release {data['version']}

{data['summary']}"""

    # Add type description
    type_desc = {
        'MAJOR': 'Breaking changes',
        'MINOR': 'Backward compatible',
        'PATCH': 'Bug fixes'
    }
    if data['type'] in type_desc:
        msg += f"\n- {type_desc[data['type']]} ({data['type']} release)"

    return msg


def generate_gitlab_release(data):
    """Generate GitLab release description in markdown."""
    # Determine what was added/changed based on summary
    added_items = []
    changed_items = []

    if '404 response' in data['summary'].lower():
        added_items.append("- Response 404 to `/api/zones/import` endpoint")
        added_items.append("  - Error: Cluster {cluster} not found")
        added_items.append("  - ErrorCode: `ClusterNotFoundException::ERROR_CODE`")
        added_items.append("  - Backward compatible: existing clients continue working")

    md = f"""## 🚀 What's New in {data['version']}

"""

    if added_items:
        md += """### ✅ Added
"""
        for item in added_items:
            md += f"{item}\n"
        md += "\n"

    if changed_items:
        md += """### ♻️ Changed
"""
        for item in changed_items:
            md += f"{item}\n"
        md += "\n"
    else:
        md += """### ♻️ Changed
- N/A

"""

    # Extract major.minor version
    major_minor = '.'.join(data['version'].split('.')[:2])

    md += f"""---

📦 Install this version via:

```bash
composer require jotelulu/php-bundle-client-hal-dns:^{major_minor}
```

🔧 Requirements: PHP 8.1+ and Symfony 6.3+

📘 See `README.md` and `CHANGELOG.md` for full details.
"""

    return md


def main():
    print("=" * 60)
    print("📝 Release Files Generator")
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
        print(f"📦 Using release: {release_version}")
        print()

    # Parse release notes
    data = parse_release_notes(release_version)
    if not data:
        sys.exit(1)

    print(f"✅ Parsed release notes")
    print(f"   Version: {data['version']}")
    print(f"   Type: {data['type_emoji']} {data['type']}")
    print(f"   Date: {data['date']}")
    print()

    # Create output directory
    release_dir = RELEASES_DIR / release_version
    output_dir = release_dir / "generated"
    output_dir.mkdir(exist_ok=True)

    print(f"📁 Output directory: {output_dir}")
    print()

    # Generate files
    print("🔨 Generating files...")
    print()

    # 1. CHANGELOG.md
    current_changelog = SDK_REPO / "CHANGELOG.md"
    if current_changelog.exists():
        changelog_content = generate_changelog(data, current_changelog)
        changelog_out = output_dir / "CHANGELOG.md"
        with open(changelog_out, 'w') as f:
            f.write(changelog_content)
        print(f"   ✅ {changelog_out.name}")
    else:
        print(f"   ⚠️  CHANGELOG.md not found in SDK repo")

    # 2. README.md
    current_readme = SDK_REPO / "README.md"
    if current_readme.exists():
        readme_content = generate_readme(data, current_readme)
        readme_out = output_dir / "README.md"
        with open(readme_out, 'w') as f:
            f.write(readme_content)
        print(f"   ✅ {readme_out.name}")
    else:
        print(f"   ⚠️  README.md not found in SDK repo")

    # 3. commit-message.txt
    commit_msg = generate_commit_message(data)
    commit_out = output_dir / "commit-message.txt"
    with open(commit_out, 'w') as f:
        f.write(commit_msg)
    print(f"   ✅ {commit_out.name}")

    # 4. tag-message.txt
    tag_msg = generate_tag_message(data)
    tag_out = output_dir / "tag-message.txt"
    with open(tag_out, 'w') as f:
        f.write(tag_msg)
    print(f"   ✅ {tag_out.name}")

    # 5. gitlab-release.md
    gitlab_md = generate_gitlab_release(data)
    gitlab_out = output_dir / "gitlab-release.md"
    with open(gitlab_out, 'w') as f:
        f.write(gitlab_md)
    print(f"   ✅ {gitlab_out.name}")

    print()
    print("=" * 60)
    print("✨ All files generated successfully!")
    print("=" * 60)
    print()

    # Show next steps
    print("📋 Next steps:")
    print()
    print(f"   1. Review generated files:")
    print(f"      ls -lh {output_dir}")
    print()
    print(f"   2. Copy to SDK repo:")
    print(f"      cp {output_dir}/CHANGELOG.md {SDK_REPO}/")
    print(f"      cp {output_dir}/README.md {SDK_REPO}/")
    print()
    print(f"   3. Commit changes:")
    print(f"      cd {SDK_REPO}")
    print(f"      git add CHANGELOG.md README.md sdk-generator/openapi.yaml")
    print(f"      git commit -F {output_dir}/commit-message.txt")
    print()
    print(f"   4. Create tag:")
    print(f"      git tag -a {data['version']} -F {output_dir}/tag-message.txt")
    print()
    print(f"   5. Push tag:")
    print(f"      git push origin {data['version']}")
    print()
    print(f"   6. Create GitLab release:")
    print(f"      Use content from: {output_dir}/gitlab-release.md")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
