#!/usr/bin/env python3
"""
Filter noise from git diff - removes lines where ONLY examples change.
This is a FALLBACK filter in case normalization missed something.
"""

import sys
import re
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: ./filter-gitdiff.py <gitdiff-file>")
        sys.exit(1)

    input_file = sys.argv[1]

    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Patterns to normalize for comparison
    UUID_PATTERN = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
    TIMESTAMP_PATTERN = re.compile(r'20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')
    # Match ANY 13-char alphanumeric in example context
    SERVERNAME_PATTERN = re.compile(r'example:\s*[\'"]?[a-z0-9]{13}[\'"]?')
    CORRELATION_ID_PATTERN = re.compile(r'(correlationId[^:]*:\s*[^:]*example:\s*)[\'"][^\'",}]+[\'"]')

    def normalize_line(line):
        """Replace variable examples with placeholders for comparison"""
        normalized = UUID_PATTERN.sub('UUID_PLACEHOLDER', line)
        normalized = TIMESTAMP_PATTERN.sub('TIMESTAMP_PLACEHOLDER', normalized)
        # Normalize serverNames: example: abc123 → example: SERVERNAME
        normalized = SERVERNAME_PATTERN.sub('example: SERVERNAME_PLACEHOLDER', normalized)
        normalized = CORRELATION_ID_PATTERN.sub(r'\1"CORRELATION_PLACEHOLDER"', normalized)
        return normalized

    def has_meaningful_change(line1, line2):
        """Check if two lines have changes beyond just examples"""
        # Normalize both lines
        norm1 = normalize_line(line1)
        norm2 = normalize_line(line2)

        # If normalized versions are different, there's a meaningful change
        return norm1 != norm2

    filtered_lines = []
    i = 0
    in_diff_block = False
    removed_count = 0

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
                # Get content without +/- prefix
                curr_content = curr_line[1:]
                next_content = next_line[1:]

                # Check if there's meaningful change
                if not has_meaningful_change(curr_content, next_content):
                    # Skip both lines (noise)
                    removed_count += 2
                    i += 2
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
    print(f"  Removed: {removed_count} noise lines")

if __name__ == '__main__':
    main()
