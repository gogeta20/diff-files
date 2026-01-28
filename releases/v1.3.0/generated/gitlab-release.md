## 🚀 What's New in 1.3.0

### ✅ Added
- Response 404 to `/api/zones/import` endpoint
  - Error: Cluster {cluster} not found
  - ErrorCode: `ClusterNotFoundException::ERROR_CODE`
  - Backward compatible: existing clients continue working

### ♻️ Changed
- N/A

---

📦 Install this version via:

```bash
composer require jotelulu/php-bundle-client-hal-dns:^1.3
```

🔧 Requirements: PHP 8.1+ and Symfony 6.3+

📘 See `README.md` and `CHANGELOG.md` for full details.
