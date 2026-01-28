# 📊 Git Diff - OpenAPI Comparison

📅 **Date:** 2026-01-27 10:49:20
🔀 **Branches:** `main` vs `feature/PROD-3958-openapi-endpoint-examples`

## 📝 Summary

- 📄 **OLD:** `openapi_old.yaml` (2835 lines) - main
- 📄 **NEW:** `openapi.yaml` (2895 lines) - feature/PROD-3958-openapi-endpoint-examples
- 📈 **Changes:** 🟢 82 lines added, 🔴 22 lines removed

## 🔍 Git Diff Output

```diff
               examples:
                 '0':
                   summary: 'Name field validation error'
-                  value: { errors: [{ code: SHARED.PAYLOAD.VALIDATION_ERROR, title: 'The name field is required', source: { pointer: /api/zones }, meta: { serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
+                  value: { errors: [{ code: SHARED.PAYLOAD.VALIDATION_ERROR, title: 'The name field is required', source: { pointer: /api/zones }, meta: { violations: [{ name: name, message: 'The name cannot be empty.' }], serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
                 '1':
-                  summary: 'Type field validation error'
-                  value: { errors: [{ code: SHARED.PAYLOAD.VALIDATION_ERROR, title: 'The type field is invalid', source: { pointer: /api/zones }, meta: { serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
+                  summary: 'Invalid zone name'
+                  value: { errors: [{ code: ZONE.NAME_NOT_VALID, title: 'Zone name {name} is not valid.', source: { pointer: /api/zones }, meta: { serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
         '404':
           description: 'Resource not found'
           content:
@@ -1237,6 +1237,15 @@ paths:
                   errors: { type: array, items: { properties: { code: { description: '', type: string, example: ZONE.ALREADY_EXISTS, nullable: false }, title: { description: '', type: string, example: 'Duplicated zone', nullable: false }, source: { properties: { pointer: { description: '', type: string, example: /api/zones/import, nullable: false } }, type: object }, meta: { properties: { serverName: { description: 'Server name identifier', type: string, example: fixed-server-id, nullable: false } }, type: object } }, type: object } }
                   metadata: { properties: { correlationId: { description: 'Correlation ID for request tracking', type: string, example: error-correlation-id, nullable: false }, timestamp: { description: 'Response timestamp', type: string, format: date-time, example: '2026-01-01T00:00:00Z', nullable: false } }, type: object }
                 type: object
+        '404':
+          description: 'Cluster {cluster} not found'
+          content:
+            application/json:
+              schema:
+                properties:
+                  errors: { type: array, items: { properties: { code: { description: '', type: string, example: CLUSTER.NOT_FOUND, nullable: false }, title: { description: '', type: string, example: 'Cluster not found zone', nullable: false }, source: { properties: { pointer: { description: '', type: string, example: /api/zones/import, nullable: false } }, type: object }, meta: { properties: { serverName: { description: 'Server name identifier', type: string, example: fixed-server-id, nullable: false } }, type: object } }, type: object } }
+                  metadata: { properties: { correlationId: { description: 'Correlation ID for request tracking', type: string, example: error-correlation-id, nullable: false }, timestamp: { description: 'Response timestamp', type: string, format: date-time, example: '2026-01-01T00:00:00Z', nullable: false } }, type: object }
+                type: object
         '500':
           description: 'Unhandled error'
           content:
@@ -1673,7 +1682,7 @@ paths:
                   metadata: { properties: { correlationId: { description: 'Correlation ID for request tracking', type: string, example: 00000000-0000-0000-0000-000000000000, nullable: false }, timestamp: { description: 'Response timestamp', type: string, format: date-time, example: '2026-01-01T00:00:00Z', nullable: false } }, type: object }
                 type: object
         '400':
-          description: 'Validation error'
+          description: 'Validation failed'
           content:
             application/json:
               schema:
@@ -1681,24 +1690,51 @@ paths:
                   errors: { type: array, items: { properties: { code: { description: '', type: string, example: SHARED.PAYLOAD.VALIDATION_ERROR, nullable: false }, title: { description: '', type: string, example: 'Validation failed', nullable: false }, source: { properties: { pointer: { description: '', type: string, example: /api/records, nullable: false } }, type: object }, meta: { properties: { violations: { description: 'List of validation violations', type: array, items: { properties: { name: { description: 'Violation message', type: string, example: 'The name field is required.' } }, type: object } }, serverName: { description: 'Server name identifier', type: string, example: fixed-server-id, nullable: false } }, type: object } }, type: object } }
                   metadata: { properties: { correlationId: { description: 'Correlation ID for request tracking', type: string, example: validation-error-id, nullable: false }, timestamp: { description: 'Response timestamp', type: string, format: date-time, example: '2026-01-01T00:00:00Z', nullable: false } }, type: object }
                 type: object
+              examples:
+                '0':
+                  summary: 'Validation error'
+                  value: { errors: [{ code: SHARED.PAYLOAD.VALIDATION_ERROR, title: 'Record validation failed', source: { pointer: /api/records }, meta: { violations: [{ name: name, message: 'The name field is too long.' }, { name: content, message: 'Content cannot be empty.' }], serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
+                '1':
+                  summary: 'Priority not set'
+                  value: { errors: [{ code: RECORD.PRIORITY_NOT_SET, title: 'Priority not set', source: { pointer: /api/records }, meta: { serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
+                '2':
+                  summary: 'Record Type Not Available'
+                  value: { errors: [{ code: RECORD.TYPE_NOT_AVAILABLE, title: "{type} records can't be modified", source: { pointer: /api/records }, meta: { serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
         '404':
-          description: 'Zone not found'
+          description: 'Resource not found'
           content:
             application/json:
               schema:
                 properties:
-                  errors: { type: array, items: { properties: { code: { description: '', type: string, example: ZONE.NOT_FOUND, nullable: false }, title: { description: '', type: string, example: 'Validation failed', nullable: false }, source: { properties: { pointer: { description: '', type: string, example: /api/records, nullable: false } }, type: object }, meta: { properties: { serverName: { description: 'Server name identifier', type: string, example: fixed-server-id, nullable: false } }, type: object } }, type: object } }
-                  metadata: { properties: { correlationId: { description: 'Correlation ID for request tracking', type: string, example: error-correlation-id, nullable: false }, timestamp: { description: 'Response timestamp', type: string, format: date-time, example: '2026-01-01T00:00:00Z', nullable: false } }, type: object }
+                  errors: { type: array, items: { properties: { code: { description: '', type: string, example: '404', nullable: false }, title: { description: '', type: string, example: 'Resource not found', nullable: false }, source: { properties: { pointer: { description: '', type: string, example: /api/records, nullable: false } }, type: object }, meta: { properties: { serverName: { description: 'Server name identifier', type: string, example: fixed-server-id, nullable: false } }, type: object } }, type: object } }
+                  metadata: { properties: { correlationId: { description: 'Correlation ID for request tracking', type: string, example: '', nullable: false }, timestamp: { description: 'Response timestamp', type: string, format: date-time, example: '2026-01-01T00:00:00Z', nullable: false } }, type: object }
                 type: object
+              examples:
+                '0':
+                  summary: 'Zone not found'
+                  value: { errors: [{ code: ZONE.NOT_FOUND, title: 'Zone {type} not found.', source: { pointer: /api/records }, meta: { serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
+                '1':
+                  summary: 'Record Type not found'
+                  value: { errors: [{ code: RECORD_TYPE.NOT_FOUND, title: 'Record Type {type} not found.', source: { pointer: /api/records }, meta: { serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
         '409':
-          description: 'Duplicated record'
+          description: Conflict
           content:
             application/json:
               schema:
                 properties:
-                  errors: { type: array, items: { properties: { code: { description: '', type: string, example: RECORD.ALREADY_EXISTS, nullable: false }, title: { description: '', type: string, example: 'Duplicated record', nullable: false }, source: { properties: { pointer: { description: '', type: string, example: /api/records, nullable: false } }, type: object }, meta: { properties: { serverName: { description: 'Server name identifier', type: string, example: fixed-server-id, nullable: false } }, type: object } }, type: object } }
-                  metadata: { properties: { correlationId: { description: 'Correlation ID for request tracking', type: string, example: error-correlation-id, nullable: false }, timestamp: { description: 'Response timestamp', type: string, format: date-time, example: '2026-01-01T00:00:00Z', nullable: false } }, type: object }
+                  errors: { type: array, items: { properties: { code: { description: '', type: string, example: '409', nullable: false }, title: { description: '', type: string, example: Conflict, nullable: false }, source: { properties: { pointer: { description: '', type: string, example: /api/zones, nullable: false } }, type: object }, meta: { properties: { serverName: { description: 'Server name identifier', type: string, example: fixed-server-id, nullable: false } }, type: object } }, type: object } }
+                  metadata: { properties: { correlationId: { description: 'Correlation ID for request tracking', type: string, example: '', nullable: false }, timestamp: { description: 'Response timestamp', type: string, format: date-time, example: '2026-01-01T00:00:00Z', nullable: false } }, type: object }
                 type: object
+              examples:
+                '0':
+                  summary: 'Duplicated CNAME record'
+                  value: { errors: [{ code: RECORD.CNAME_ALREADY_EXISTS, title: 'Duplicated CNAME record for {zone}', source: { pointer: /api/zones }, meta: { serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
+                '1':
+                  summary: 'Duplicated record'
+                  value: { errors: [{ code: RECORD.ALREADY_EXISTS, title: 'Duplicated {type} record', source: { pointer: /api/zones }, meta: { serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
+                '2':
+                  summary: 'Record out of zone'
+                  value: { errors: [{ code: RECORD.NAME_OUT_OF_ZONE, title: 'Record {name} is out of zone {zone}', source: { pointer: /api/zones }, meta: { serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
         '500':
           description: 'Unhandled error'
           content:
@@ -1855,33 +1891,57 @@ paths:
                   data: { $ref: '#/components/schemas/RecordResponse' }
                   metadata: { properties: { correlationId: { description: 'Correlation ID for request tracking', type: string, example: 00000000-0000-0000-0000-000000000000, nullable: false }, timestamp: { description: 'Response timestamp', type: string, format: date-time, example: '2026-01-01T00:00:00Z', nullable: false } }, type: object }
                 type: object
-        '404':
-          description: 'Record not found'
+        '400':
+          description: 'Validation failed'
           content:
             application/json:
               schema:
                 properties:
-                  errors: { type: array, items: { properties: { code: { description: '', type: string, example: RECORD.NOT_FOUND, nullable: false }, title: { description: '', type: string, example: 'Record not found.', nullable: false }, source: { properties: { pointer: { description: '', type: string, example: /api/records/00000000-0000-0000-0000-000000000000, nullable: false } }, type: object }, meta: { properties: { serverName: { description: 'Server name identifier', type: string, example: fixed-server-id, nullable: false } }, type: object } }, type: object } }
-                  metadata: { properties: { correlationId: { description: 'Correlation ID for request tracking', type: string, example: error-correlation-id, nullable: false }, timestamp: { description: 'Response timestamp', type: string, format: date-time, example: '2026-01-01T00:00:00Z', nullable: false } }, type: object }
+                  errors: { type: array, items: { properties: { code: { description: '', type: string, example: SHARED.PAYLOAD.VALIDATION_ERROR, nullable: false }, title: { description: '', type: string, example: 'Validation failed', nullable: false }, source: { properties: { pointer: { description: '', type: string, example: /api/records, nullable: false } }, type: object }, meta: { properties: { violations: { description: 'List of validation violations', type: array, items: { properties: { name: { description: 'Violation message', type: string, example: 'The name field is required.' } }, type: object } }, serverName: { description: 'Server name identifier', type: string, example: fixed-server-id, nullable: false } }, type: object } }, type: object } }
+                  metadata: { properties: { correlationId: { description: 'Correlation ID for request tracking', type: string, example: validation-error-id, nullable: false }, timestamp: { description: 'Response timestamp', type: string, format: date-time, example: '2026-01-01T00:00:00Z', nullable: false } }, type: object }
                 type: object
-        '400':
-          description: 'Validation error'
+              examples:
+                '0':
+                  summary: 'Validation error'
+                  value: { errors: [{ code: SHARED.PAYLOAD.VALIDATION_ERROR, title: 'Record validation failed', source: { pointer: /api/records }, meta: { violations: [{ name: name, message: 'The name field is too long.' }, { name: content, message: 'Content cannot be empty.' }], serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
+                '1':
+                  summary: 'Priority not set'
+                  value: { errors: [{ code: RECORD.PRIORITY_NOT_SET, title: 'Priority not set', source: { pointer: /api/records }, meta: { serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
+                '2':
+                  summary: 'Record Type Not Available'
+                  value: { errors: [{ code: RECORD.TYPE_NOT_AVAILABLE, title: "{type} records can't be modified", source: { pointer: /api/records }, meta: { serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
+        '404':
+          description: 'Resource not found'
           content:
             application/json:
               schema:
                 properties:
-                  errors: { type: array, items: { properties: { code: { description: '', type: string, example: SHARED.PAYLOAD.VALIDATION_ERROR, nullable: false }, title: { description: '', type: string, example: 'Validation failed', nullable: false }, source: { properties: { pointer: { description: '', type: string, example: /api/records/00000000-0000-0000-0000-000000000000, nullable: false } }, type: object }, meta: { properties: { violations: { description: 'List of validation violations', type: array, items: { properties: { name: { description: 'Violation message', type: string, example: 'Invalid record payload.' } }, type: object } }, serverName: { description: 'Server name identifier', type: string, example: fixed-server-id, nullable: false } }, type: object } }, type: object } }
-                  metadata: { properties: { correlationId: { description: 'Correlation ID for request tracking', type: string, example: validation-error-id, nullable: false }, timestamp: { description: 'Response timestamp', type: string, format: date-time, example: '2026-01-01T00:00:00Z', nullable: false } }, type: object }
+                  errors: { type: array, items: { properties: { code: { description: '', type: string, example: '404', nullable: false }, title: { description: '', type: string, example: 'Resource not found', nullable: false }, source: { properties: { pointer: { description: '', type: string, example: /api/records, nullable: false } }, type: object }, meta: { properties: { serverName: { description: 'Server name identifier', type: string, example: fixed-server-id, nullable: false } }, type: object } }, type: object } }
+                  metadata: { properties: { correlationId: { description: 'Correlation ID for request tracking', type: string, example: '', nullable: false }, timestamp: { description: 'Response timestamp', type: string, format: date-time, example: '2026-01-01T00:00:00Z', nullable: false } }, type: object }
                 type: object
+              examples:
+                '0':
+                  summary: 'Record not found'
+                  value: { errors: [{ code: RECORD.NOT_FOUND, title: 'Record {uuid} not found.', source: { pointer: /api/records }, meta: { serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
         '409':
-          description: 'Duplicated record'
+          description: Conflict
           content:
             application/json:
               schema:
                 properties:
-                  errors: { type: array, items: { properties: { code: { description: '', type: string, example: RECORD.ALREADY_EXISTS, nullable: false }, title: { description: '', type: string, example: 'Duplicated record', nullable: false }, source: { properties: { pointer: { description: '', type: string, example: /api/records, nullable: false } }, type: object }, meta: { properties: { serverName: { description: 'Server name identifier', type: string, example: fixed-server-id, nullable: false } }, type: object } }, type: object } }
-                  metadata: { properties: { correlationId: { description: 'Correlation ID for request tracking', type: string, example: error-correlation-id, nullable: false }, timestamp: { description: 'Response timestamp', type: string, format: date-time, example: '2026-01-01T00:00:00Z', nullable: false } }, type: object }
+                  errors: { type: array, items: { properties: { code: { description: '', type: string, example: '409', nullable: false }, title: { description: '', type: string, example: Conflict, nullable: false }, source: { properties: { pointer: { description: '', type: string, example: /api/zones, nullable: false } }, type: object }, meta: { properties: { serverName: { description: 'Server name identifier', type: string, example: fixed-server-id, nullable: false } }, type: object } }, type: object } }
+                  metadata: { properties: { correlationId: { description: 'Correlation ID for request tracking', type: string, example: '', nullable: false }, timestamp: { description: 'Response timestamp', type: string, format: date-time, example: '2026-01-01T00:00:00Z', nullable: false } }, type: object }
                 type: object
+              examples:
+                '0':
+                  summary: 'Duplicated CNAME record'
+                  value: { errors: [{ code: RECORD.CNAME_ALREADY_EXISTS, title: 'Duplicated CNAME record for {zone}', source: { pointer: /api/zones }, meta: { serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
+                '1':
+                  summary: 'Duplicated record'
+                  value: { errors: [{ code: RECORD.ALREADY_EXISTS, title: 'Duplicated {type} record', source: { pointer: /api/zones }, meta: { serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
+                '2':
+                  summary: 'Record out of zone'
+                  value: { errors: [{ code: RECORD.NAME_OUT_OF_ZONE, title: 'Record {name} is out of zone {zone}', source: { pointer: /api/zones }, meta: { serverName: fixed-server-id } }], metadata: { correlationId: 00000000-0000-0000-0000-000000000000, timestamp: '2026-01-01T00:00:00Z' } }
         '500':
           description: 'Unhandled error'
           content:
```
