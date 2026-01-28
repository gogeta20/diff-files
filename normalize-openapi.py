#!/usr/bin/env python3
"""
Normalize OpenAPI YAML file by replacing random values with fixed ones.
This allows real comparison without noise from auto-generated examples.
"""

import sys
import re

def normalize_openapi_yaml(file_path):
    """
    Normalize OpenAPI YAML by replacing ALL variable examples:
    - UUIDs → fixed UUID
    - Timestamps → fixed timestamp
    - 13-char alphanumeric strings (serverNames) → fixed-server-id
    - correlationIds → fixed-correlation-id
    """

    with open(file_path, 'r') as f:
        content = f.read()

    # Count occurrences for stats (before normalization)
    uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    uuid_count = len(re.findall(uuid_pattern, content))

    timestamp_pattern = r"'20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z'"
    timestamp_count = len(re.findall(timestamp_pattern, content))

    # Count alphanumeric IDs in examples (before normalization)
    servername_pattern = r'example:\s*[a-z0-9]{10,15}(?=[,\s\}])'
    servername_count = len(re.findall(servername_pattern, content))

    # 1. Normalize ALL UUIDs (everywhere: examples, correlationIds, etc.)
    content = re.sub(
        uuid_pattern,
        '00000000-0000-0000-0000-000000000000',
        content
    )

    # 2. Normalize ALL timestamps
    content = re.sub(
        timestamp_pattern,
        "'2026-01-01T00:00:00Z'",
        content
    )

    # 3. Normalize ALL alphanumeric examples (serverNames, serial numbers, etc)
    # This catches: example: abc123xyz4567 (10-15 chars, with comma, space, or brace after)
    # These are typically serverName examples or serial numbers
    content = re.sub(
        r'example:\s*([a-z0-9]{10,15})(?=[,\s\}])',
        'example: fixed-server-id',
        content
    )

    # 4. Normalize serverName values (direct format: serverName: abc123)
    # In case there are some in different format
    content = re.sub(
        r'(serverName:\s*)([a-z0-9]{10,15})(?=[,\s\}])',
        r'\1fixed-server-id',
        content
    )

    # Write normalized content
    with open(file_path, 'w') as f:
        f.write(content)

    return uuid_count, timestamp_count, servername_count

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: ./normalize-openapi.py <openapi.yaml>")
        sys.exit(1)

    file_path = sys.argv[1]
    uuid_count, timestamp_count, servername_count = normalize_openapi_yaml(file_path)

    print(f"✓ Normalized: {file_path}")
    print(f"  - {uuid_count} UUIDs normalized")
    print(f"  - {timestamp_count} timestamps normalized")
    print(f"  - {servername_count} serverNames/IDs normalized")
