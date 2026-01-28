# 🔧 Setup Inicial - OpenAPI Diff System

Guía de configuración inicial del sistema de comparación de OpenAPI.

---

## 📋 Prerequisitos

- Docker y Docker Compose funcionando
- Python 3 con PyYAML instalado
- Make
- Git
- Contenedores de `php-hal-dns` corriendo

---

## 🚀 Setup Inicial (Primera Vez)

### 1. Generar OpenAPI de referencia desde `main`

Antes de comparar cualquier rama feature, necesitas generar un OpenAPI base desde `main`.

```bash
# 1. Ir a main branch
cd ~/projects/jotelulu/php-hal-dns
git checkout main
git pull origin main

# 2. Asegurar que contenedores estén corriendo
docker compose ps
# Si no están corriendo:
docker compose up -d --wait

# 3. Generar y guardar OpenAPI de main como referencia
cd ~/projects/main
make openapi-save-main
```

Este comando genera `openapi-main.yaml` y lo guarda en:
```
~/projects/jotelulu/without/php-hal-dns/openapi-main.yaml
```

**Notas importantes:**
- ✅ Este archivo se genera **normalizado** (UUIDs, timestamps, serverNames fijos)
- ✅ Solo necesitas hacerlo **una vez** o cuando actualices `main`
- ✅ Se usa como **OLD** en todas las comparaciones

---

## 🔄 Actualizar OpenAPI de referencia

Cuando `main` tiene cambios significativos y quieres actualizar la referencia:

```bash
# 1. Actualizar main
cd ~/projects/jotelulu/php-hal-dns
git checkout main
git pull origin main

# 2. Limpiar cache de Symfony
docker exec php-hal-dns-php-1 php bin/console cache:clear

# 3. Regenerar referencia
cd ~/projects/main
make openapi-save-main
```

---

## 📂 Estructura de Directorios

```
~/projects/
├── jotelulu/
│   ├── php-hal-dns/              # Proyecto principal (feature branches)
│   ├── without/
│   │   └── php-hal-dns/
│   │       └── openapi-main.yaml  # ⭐ OpenAPI de referencia (main)
│   └── php-bundle-client-hal-dns/ # SDK generado
│
├── personal/
│   └── diff-files/                # Sistema de comparación
│       ├── docs/                  # Reportes Python tool
│       ├── gitdiff/               # Reportes git diff
│       ├── releases/              # Documentación de releases
│       ├── compare.py             # Python diff tool
│       ├── normalize-openapi.py   # Normalizador
│       ├── filter-gitdiff.py      # Filtro de ruido
│       └── README.md              # Documentación principal
│
└── main/
    └── devops/mk/openapi.mk      # Comandos make
```

---

## ✅ Verificar Setup

```bash
# Verificar que existe el archivo de referencia
ls -lh ~/projects/jotelulu/without/php-hal-dns/openapi-main.yaml

# Debe mostrar algo como:
# -rw-rw-r-- 1 user user 177K ene 27 10:00 openapi-main.yaml

# Verificar líneas y normalización
wc -l ~/projects/jotelulu/without/php-hal-dns/openapi-main.yaml
# Debe mostrar ~2800-2900 líneas

# Verificar que está normalizado (buscar UUIDs no normalizados)
grep -oE "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}" \
  ~/projects/jotelulu/without/php-hal-dns/openapi-main.yaml | \
  grep -v "00000000-0000-0000-0000-000000000000" | wc -l
# Debe mostrar: 0 (ningún UUID sin normalizar)
```

---

## 🎯 Siguiente Paso

Una vez completado el setup, puedes empezar a comparar branches:

```bash
cd ~/projects/main
make openapi-update-full
```

Ver la documentación completa en: `README.md`

---

## ⚠️ Troubleshooting

### Error: "openapi-main.yaml not found"

**Causa:** No has generado el OpenAPI de referencia.

**Solución:**
```bash
cd ~/projects/main
make openapi-save-main
```

---

### Error: Contenedores no corriendo

**Causa:** Docker compose no está levantado en php-hal-dns.

**Solución:**
```bash
cd ~/projects/jotelulu/php-hal-dns
docker compose up -d --wait
```

---

### Error: Cache de Symfony desactualizado

**Causa:** Symfony no refleja los cambios de código.

**Solución:**
```bash
docker exec php-hal-dns-php-1 php bin/console cache:clear
```

---

### Contenedores en restart loop

**Causa:** Problema con .env o configuración.

**Solución:**
```bash
cd ~/projects/jotelulu/php-hal-dns
docker compose down
docker compose up -d --wait
```

---

## 📚 Referencias

- **README principal:** `README.md` - Todos los comandos disponibles
- **Makefile:** `~/projects/main/devops/mk/openapi.mk` - Lógica de comandos
- **Releases:** `releases/` - Historial de versiones documentadas
