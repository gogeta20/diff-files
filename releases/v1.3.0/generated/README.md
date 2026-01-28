# HAL DNS Client Bundle

A Symfony bundle for consuming the DNS HAL API.\
It provides a fully-generated SDK (based on OpenAPI), auto-configured for Symfony, with support for domain and record management.

---

## 📚 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Available Endpoints](#available-endpoints)
- [OpenAPI SDK Generation](#openapi-sdk-generation)
- [Versioning](#versioning)
- [License](#license)

---

## ⚙️ Installation

### 1. Add the GitLab repository to your `composer.json`:

```json
{
  "repositories": [
    {
      "name": "jotelulu/php-bundle-client-hal-dns",
      "type": "gitlab",
      "url": "https://gitlab.jotelulu.com/jotelulu/php-bundle-client-hal-dns.git"
    }
  ]
}
```

### 2. Require the bundle via Composer

```bash
composer require jotelulu/php-bundle-client-hal-dns:^1.3
```

> You can also use `dev-main` for development purposes.

### 3. Enable the bundle

In `config/bundles.php`:

```php
return [
    Jotelulu\Dns\Hal\ClientBundle\HalDnsClientBundle::class => ['all' => true],
];
```

Or let Symfony autoload it via Flex (if applicable).

---

## 🚀 Usage

You can inject the HAL DNS client in your services or controllers:

```php
use Jotelulu\Dns\Hal\ClientBundle\Client\Client;

class MyService
{
    public function __construct(private Client $client) {}

    public function fetchZones(): array
    {
        return $this->client->getAllZones(); // Example method
    }
}
```

---

## 📡 Available Endpoints

The current version (`1.3.0`) supports:

### Zones
- `GET /zones`
- `GET /zones/{id}`
- `GET /zones/{id}/status`
- `POST /api/zones/import`

### Records
- `GET /zones/{id}/records`
- `GET /zones/{id}/records/{recordId}`
- `POST /api/records/import`

### Record Types
- `GET /api/recordTypes/{id}`
- `GET /api/recordTypes/by-name/{typeName}`

### Providers
- `GET /api/providers`
- `GET /api/providers/{id}`

### Status & Health
- `GET /api/status/live`
- `GET /api/status/ready`
- `GET /api/status/startup-probe`
- `GET /api/status/detailed`
- `GET /api/status/info`

> Responses follow HAL standard: data + `_links` + `meta`

---

## 🧪 OpenAPI SDK Generation

To regenerate the client after OpenAPI updates:

### Option A: Locally

```bash
cd sdk-generator && composer install && make generate-client
```

### Option B: With Docker

```bash
make build
make run
make generate-sdk
```

🖐️ You can list available tools with:

```bash
make help
```

---

## 📌 Versioning

We follow [SemVer](https://semver.org/):

- `MAJOR`: Breaking changes
- `MINOR`: New features, backward compatible
- `PATCH`: Fixes

To upgrade, just update your Composer constraint:

```bash
composer require jotelulu/php-bundle-client-hal-dns:^1.3
```

---

## 🪖 License

MIT License – see [LICENSE](LICENSE)

---

## ✍️ Maintained by

**Jotelulu Engineering Team** – [https://www.jotelulu.com](https://www.jotelulu.com)
