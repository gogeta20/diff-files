#!/bin/bash
# Filter noise from git diff - removes lines where ONLY examples change

INPUT_FILE="$1"

if [ -z "$INPUT_FILE" ]; then
    echo "Usage: $0 <gitdiff-file>"
    exit 1
fi

# Create backup
cp "$INPUT_FILE" "${INPUT_FILE}.backup"

# Simple approach: remove consecutive +/- pairs that only differ in:
# - UUIDs (format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
# - Timestamps (format: 2026-01-27T07:24:55Z)
# - ServerNames (format: random 13-char alphanumeric)

python3 << 'PYTHON_EOF' "$INPUT_FILE"
import sys
import re

input_file = sys.argv[1]

with open(input_file, 'r') as f:
    lines = f.readlines()

# Patterns to normalize
UUID_PATTERN = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
TIMESTAMP_PATTERN = re.compile(r'20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')
SERVERNAME_PATTERN = re.compile(r'example: [a-z0-9]{13},')

def normalize_line(line):
    """Replace examples with placeholders"""
    normalized = UUID_PATTERN.sub('UUID_PLACEHOLDER', line)
    normalized = TIMESTAMP_PATTERN.sub('TIMESTAMP_PLACEHOLDER', normalized)
    normalized = SERVERNAME_PATTERN.sub('example: SERVERNAME_PLACEHOLDER,', normalized)
    return normalized

filtered_lines = []
i = 0
in_diff_block = False

while i < len(lines):
    line = lines[i]

    # Track if we're in diff block
    if line.strip() == '```diff':
        in_diff_block = True
        filtered_lines.append(line)
        i += 1
        continue
    elif line.strip() == '```' and in_diff_block:
        in_diff_block = False
        filtered_lines.append(line)
        i += 1
        continue

    # If not in diff block, keep line as is
    if not in_diff_block:
        filtered_lines.append(line)
        i += 1
        continue

    # In diff block - check for noise
    if i + 1 < len(lines):
        curr_line = lines[i]
        next_line = lines[i + 1]

        # Check if it's a +/- pair
        if curr_line.startswith('-') and next_line.startswith('+'):
            # Normalize both lines
            curr_normalized = normalize_line(curr_line[1:])  # Remove - prefix
            next_normalized = normalize_line(next_line[1:])  # Remove + prefix

            # If normalized versions are identical, skip both lines (noise)
            if curr_normalized == next_normalized:
                i += 2  # Skip both lines
                continue

    # Keep the line
    filtered_lines.append(line)
    i += 1

# Write filtered output
with open(input_file, 'w') as f:
    f.writelines(filtered_lines)

print(f"✓ Filtered gitdiff: {input_file}")
print(f"  Original: {len(lines)} lines")
print(f"  Filtered: {len(filtered_lines)} lines")
print(f"  Removed: {len(lines) - len(filtered_lines)} noise lines")

PYTHON_EOF
