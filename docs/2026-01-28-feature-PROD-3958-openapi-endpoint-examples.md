# 📊 OpenAPI Comparison Report

📅 **Date:** 2026-01-28 06:58:07

## 🔀 Branches Compared

- 🔵 **OLD (base):** `main` from `without/php-hal-dns`
- 🟢 **NEW (current):** `feature/PROD-3958-openapi-endpoint-examples` from `php-hal-dns`

## 📄 Files

- `openapi_old.yaml` - 2835 lines
- `openapi.yaml` - 2895 lines

## ⚙️ Commands

```bash
# Compare changes
cd /home/mauricio-vargas/projects/personal/diff-files
python3 compare.py docs/openapi_old.yaml docs/openapi.yaml

# Only breaking changes
python3 compare.py docs/openapi_old.yaml docs/openapi.yaml --breaking
```

## Python Diff Tool Results

```
# OpenAPI Diff Tool

Comparing:
- docs/openapi_old.yaml
- docs/openapi.yaml



## Paths

### 🟢 Added

### 🔴 Removed

### 🟡 Modified
* /api/zones/import

## Schemas

### 🟢 Added

### 🔴 Removed

### 🟡 Modified

## Responses

/api/zones/import [POST]
    + Added response 404


## 🟡 Suggested version bump: **MINOR**
```
