# Changelog

## [1.3.0] - 2026-01-27

### Added
- Response 404 to `/api/zones/import` endpoint for cluster not found errors

### Changed
- N/A

### Removed
- N/A


## [1.2.0] - 2025-11-13

### Added
- New endpoint: `GET /api/status/info`
  Provides extended service information.
- Added new response codes and improved error semantics across the API.
- Provider endpoints (introduced in 1.1.x) are now fully integrated:
  - `GET /api/providers`
  - `GET /api/providers/{id}`

### Changed
- Updated multiple endpoints with more precise HTTP status codes (`400`, `404`, `422`, etc.).
- Improved validation error structures and metadata consistency.
- Updated SDK generation with new response models and normalization changes.

### Removed
- (Nothing removed in this release)

## [1.0.0] - 2025-10-21

### Added
- Endpoints:
  - `GET /api/recordTypes/by-name/{typeName}` – Retrieve RecordType by name (A, AAAA, CNAME, TXT…)
  - `GET /api/status/live` – Liveness probe
  - `GET /api/status/ready` – Readiness probe
  - `GET /api/status/startup-probe` – Startup probe
  - `GET /api/status/detailed` – Detailed service status
- Documentation reviewed and aligned with stable 1.x series

### Changed
- Promoted API/SDK to **stable (1.x)**.
- Internal OpenAPI reorganization for clarity and maintainability.

### Removed
- Legacy response schemas cleaned up:
  - `ClustersResponse`, `RecordDefaultsResponse`, `RecordTypesResponse`,
    `RecordsMetadataResponse`, `RecordsResponse`, `ZonesResponse`


## [0.3.0] - 2025-09-18

### Added
- Endpoints:
  - `POST /api/records/import` – Import DNS records in bulk
  - `POST /api/zones/import` – Import zones
  - `GET /api/zones/{id}/status` – Retrieve status information for a zone
- Schemas:
  - `ZoneRecordStatusResponse`
  - `ZoneStatusResponse`

### Changed
- Improved OpenAPI coverage with status and import operations

### Removed
- N/A

---

## [0.2.0] - 2025-09-09

### Added
- Endpoints:
  - `GET /zones`: Retrieve DNS zones collection
  - `GET /zones/{id}`: Retrieve a specific zone by UUID
  - `GET /zones/{id}/records`: Retrieve DNS records for a given zone
  - `GET /zones/{id}/records/{recordId}`: Retrieve a specific record by zone and ID
- Schemas:
  - `Zone`
  - `ZoneCollection`
  - `ZoneRecord`
  - `ZoneRecordDetail`
  - `RecordCollection`
  - `PaginationMeta`
  - `ErrorResponse`
- HAL-style pagination and metadata support
- Standardized error handling with `ErrorResponse` schema
- Docker support for SDK generation with `make generate-sdk`

### Changed
- Improved OpenAPI definitions with better `$ref` usage
- Refactored SDK client structure for clarity and future extension

### Removed
- N/A
