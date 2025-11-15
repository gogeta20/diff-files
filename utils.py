import yaml
import re

# ------------------------------------------------------------------------------
# LOAD YAML
# ------------------------------------------------------------------------------

def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ------------------------------------------------------------------------------
# BASIC KEY DIFF
# ------------------------------------------------------------------------------

def dict_diff_keys(a: dict, b: dict):
    a_keys = set(a.keys())
    b_keys = set(b.keys())
    added = b_keys - a_keys
    removed = a_keys - b_keys
    common = a_keys & b_keys
    return sorted(added), sorted(removed), sorted(common)


# ------------------------------------------------------------------------------
# SANITIZATION HELPERS
# ------------------------------------------------------------------------------

UUID_REGEX = re.compile(
    r"[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}"
)

TIMESTAMP_REGEX = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
)

FIELDS_TO_IGNORE = {
    "description",
    "summary",
    "title",
    "example",
    "examples",
    "operationId",
    "format",
    "serverName",
    "correlationId",
}


def sanitize_value(value):
    if isinstance(value, str):
        value = UUID_REGEX.sub("UUID", value)
        value = TIMESTAMP_REGEX.sub("TIMESTAMP", value)

    if value in [None, "", {}, []]:
        return "EMPTY"

    return value


# ------------------------------------------------------------------------------
# SANITIZE OPENAPI STRUCTURE
# ------------------------------------------------------------------------------

def sanitize_openapi(data):
    if isinstance(data, dict):
        out = {}
        for k, v in data.items():
            if k in FIELDS_TO_IGNORE:
                continue
            out[k] = sanitize_openapi(v)
        return out

    if isinstance(data, list):
        return [sanitize_openapi(v) for v in data]

    return sanitize_value(data)


# ------------------------------------------------------------------------------
# NORMALIZE SCHEMA STRUCTURE (oneOf/anyOf)
# ------------------------------------------------------------------------------

def normalize_schema_structure(data):
    """Normalize schema composition keywords to avoid noisy diffs."""
    if isinstance(data, dict):
        normalized = {}

        if "oneOf" in data:
            normalized["oneOf"] = sorted(
                sanitize_openapi(data["oneOf"]),
                key=lambda x: str(x)
            )

        if "anyOf" in data:
            normalized["anyOf"] = sorted(
                sanitize_openapi(data["anyOf"]),
                key=lambda x: str(x)
            )

        for k, v in data.items():
            if k not in ["oneOf", "anyOf"]:
                normalized[k] = normalize_schema_structure(v)

        return normalized

    if isinstance(data, list):
        return [normalize_schema_structure(i) for i in data]

    return data


# ------------------------------------------------------------------------------
# DEEP DIFF
# ------------------------------------------------------------------------------

def deep_diff(old, new, path=""):
    changes = []

    # Dict recursion
    if isinstance(old, dict) and isinstance(new, dict):
        old_keys = set(old.keys())
        new_keys = set(new.keys())

        for k in new_keys - old_keys:
            changes.append(("added", f"{path}/{k}", None, new[k]))

        for k in old_keys - new_keys:
            changes.append(("removed", f"{path}/{k}", old[k], None))

        for k in old_keys & new_keys:
            changes.extend(
                deep_diff(old[k], new[k], f"{path}/{k}")
            )

        return changes

    # List recursion
    if isinstance(old, list) and isinstance(new, list):
        max_len = max(len(old), len(new))
        for i in range(max_len):
            if i >= len(old):
                changes.append(("added", f"{path}[{i}]", None, new[i]))
            elif i >= len(new):
                changes.append(("removed", f"{path}[{i}]", old[i], None))
            else:
                changes.extend(
                    deep_diff(old[i], new[i], f"{path}[{i}]")
                )
        return changes

    # Direct value diff
    if old != new:
        changes.append(("modified", path, old, new))

    return changes


# ------------------------------------------------------------------------------
# FORMAT SCHEMA DIFF (NO DUPLICATES)
# ------------------------------------------------------------------------------

def compare_schema_details(old_schema, new_schema, schema_name):
    diffs = deep_diff(old_schema, new_schema, path=f"/components/schemas/{schema_name}")

    formatted = []
    seen = set()

    for change_type, path, old, new in diffs:
        key = (change_type, path)
        if key in seen:
            continue
        seen.add(key)

        if change_type == "added":
            formatted.append(f"[green]+ Added[/green] {path}: {new}")
        elif change_type == "removed":
            formatted.append(f"[red]- Removed[/red] {path}: {old}")
        else:
            formatted.append(f"[yellow]~ Modified[/yellow] {path}: {old} → {new}")

    return formatted
