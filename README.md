# OpenAPI Diff Tool

Sistema automatizado para comparar cambios en OpenAPI y generar releases automáticamente para el SDK.

---

## 🚀 Quick Start

```bash
# Flujo completo desde cero
make release-full
```

Esto ejecuta:
1. Trae OpenAPI de ambos branches (main vs feature)
2. Normaliza y compara cambios
3. Genera git diff filtrado
4. Calcula el siguiente tag
5. Genera todos los archivos de release

---

## 📚 Comandos Disponibles

### Ver todos los comandos
```bash
make help
```

### Flujos completos

| Comando | Descripción |
|---------|-------------|
| `make release-full` | **Flujo completo**: diff + calcular tag + generar archivos de release |
| `make diff-full` | Flujo de diff: traer YAMLs + comparar + git diff |

### Comandos de Diff

| Comando | Descripción |
|---------|-------------|
| `make diff-prepare` | Traer YAMLs de ambos branches y normalizar |
| `make diff-compare` | Ejecutar compare.py (cambios estructurales) |
| `make diff-compare-breaking` | Solo breaking changes |
| `make diff-gitdiff` | Generar git diff filtrado línea a línea |
| `make show-diff` | Mostrar último git diff en terminal |

### Comandos de Release

| Comando | Descripción |
|---------|-------------|
| `make release-info` | Mostrar información del próximo release |
| `make release-prepare` | Calcular tag y generar archivos de release |

### Utilidades

| Comando | Descripción |
|---------|-------------|
| `make info` | Mostrar información de archivos y branches |
| `make clean` | Limpiar directorios docs/ y gitdiff/ |

---

## 📊 ¿Qué hace este proyecto?

### 1. Comparar OpenAPI

Compara dos archivos OpenAPI YAML (main vs feature branch) y detecta:
- **Paths**: Endpoints añadidos/eliminados/modificados
- **Schemas**: Modelos de datos añadidos/eliminados/modificados
- **Responses**: Respuestas HTTP añadidas/eliminadas/modificadas
- **Version Bump**: Sugiere si el cambio es MAJOR, MINOR o PATCH (semver)

### 2. Normalización Automática

Elimina falsos positivos normalizando:
- **UUIDs**: `550e8400-e29b-41d4-a716-446655440000` → `UUID`
- **Timestamps**: `2024-01-26T08:00:00Z` → `TIMESTAMP`
- **Server IDs**: Nombres aleatorios de servidores → `SERVERNAME`
- **Campos descriptivos**: `description`, `summary`, `title`, `example`

### 3. Generar Release Automáticamente

Basándose en los cambios detectados:
1. Calcula el siguiente tag (ej: 1.2.1 → 1.3.0)
2. Genera archivos listos para usar:
   - `CHANGELOG.md` actualizado
   - `README.md` actualizado
   - `commit-message.txt`
   - `tag-message.txt`
   - `gitlab-release.md`

---

## 📖 Flujo de Trabajo Completo

### Paso 1: Ejecutar el flujo completo

```bash
cd /home/mauricio-vargas/projects/personal/diff-files
make release-full
```

**Output:**
```
═══════════════════════════════════════════════
   Flujo Completo: Diff + Release
═══════════════════════════════════════════════

✓ YAMLs copiados y normalizados
✓ Comparación ejecutada
✓ Git diff generado

🏷️  Next Tag Calculator
════════════════════════════════════════════════
📍 Current SDK tag: 1.2.1
🟡 Bump type: MINOR
✨ Next tag: 1.3.0

📝 Release Files Generator
════════════════════════════════════════════════
✅ CHANGELOG.md
✅ README.md
✅ commit-message.txt
✅ tag-message.txt
✅ gitlab-release.md
```

### Paso 2: Revisar archivos generados

```bash
ls -lh releases/v1.3.0/generated/
```

Archivos generados:
- `CHANGELOG.md` → Copiar a SDK repo
- `README.md` → Copiar a SDK repo
- `commit-message.txt` → Usar con `git commit -F`
- `tag-message.txt` → Usar con `git tag -a -F`
- `gitlab-release.md` → Copiar a GitLab Release

### Paso 3: Aplicar cambios al SDK

```bash
# Copiar archivos al SDK
cp releases/v1.3.0/generated/CHANGELOG.md ~/projects/jotelulu/php-bundle-client-hal-dns/
cp releases/v1.3.0/generated/README.md ~/projects/jotelulu/php-bundle-client-hal-dns/

# Ir al SDK repo
cd ~/projects/jotelulu/php-bundle-client-hal-dns

# Commit
git add CHANGELOG.md README.md sdk-generator/openapi.yaml
git commit -F ~/projects/personal/diff-files/releases/v1.3.0/generated/commit-message.txt

# Crear tag
git tag -a 1.3.0 -F ~/projects/personal/diff-files/releases/v1.3.0/generated/tag-message.txt

# Push
git push origin 1.3.0
```

### Paso 4: Crear GitLab Release

1. Ve a GitLab: https://gitlab.jotelulu.com/jotelulu/php-bundle-client-hal-dns/-/releases/new
2. Selecciona el tag: `1.3.0`
3. Copia el contenido de `releases/v1.3.0/generated/gitlab-release.md`
4. Publica el release

---

## 🎯 Lógica de Version Bump

El sistema analiza los cambios y sugiere el tipo de versión según [Semantic Versioning](https://semver.org/):

### Version format: `MAJOR.MINOR.PATCH`

```
Ejemplo: 2.5.3
         │ │ │
         │ │ └─ PATCH: Bug fixes, cambios internos
         │ └─── MINOR: Nuevas features (compatible)
         └───── MAJOR: Breaking changes (incompatible)
```

### Tabla de decisión

| Tipo | Cambio | Se detecta cuando... | Ejemplos |
|------|--------|---------------------|----------|
| 🔴 **MAJOR** | `2.5.3` → `3.0.0` | Breaking changes | - Path eliminado<br>- Schema eliminado<br>- Response eliminado<br>- Tipo de dato cambiado |
| 🟡 **MINOR** | `2.5.3` → `2.6.0` | Nuevas features (compatible) | - Path añadido<br>- Schema añadido<br>- Response añadido |
| ✅ **PATCH** | `2.5.3` → `2.5.4` | Bug fixes / cambios menores | - Modificaciones sin breaking<br>- Descripciones actualizadas |

---

## 📂 Estructura del Proyecto

```
diff-files/
├── Makefile                    # Comandos automatizados
├── README.md                   # Este archivo
├── PROYECTO-CONTEXTO.md        # Contexto del ecosistema completo
│
├── compare.py                  # Comparación estructural de OpenAPI
├── normalize-openapi.py        # Normalización de valores aleatorios
├── filter-gitdiff.py           # Filtrado de git diff
├── show-diff.py                # Mostrar diff en terminal
├── get-next-tag.py            # Calcular siguiente tag
├── generate-release-files.py   # Generar archivos de release
├── utils.py                    # Utilidades
│
├── docs/                       # OpenAPI files (generados)
│   ├── openapi_old.yaml
│   ├── openapi.yaml
│   └── YYYY-MM-DD-branch.md
│
├── gitdiff/                    # Git diff filtrados (generados)
│   └── YYYY-MM-DD-branch-gitdiff.md
│
├── releases/                   # Releases documentados
│   └── v1.3.0/
│       ├── README.md
│       ├── RELEASE-NOTES.md
│       ├── 2026-01-27-feature-PROD-3958-openapi-endpoint-examples.md
│       ├── 2026-01-27-feature-PROD-3958-openapi-endpoint-examples-gitdiff.md
│       └── generated/         # Archivos generados automáticamente
│           ├── CHANGELOG.md
│           ├── README.md
│           ├── commit-message.txt
│           ├── tag-message.txt
│           └── gitlab-release.md
│
└── examples/                   # Ejemplos para testing
```

---

## 🔧 Configuración

### Paths en Makefile

Los paths están configurados en el `Makefile`:

```makefile
HALDNS_PATH=/home/mauricio-vargas/projects/jotelulu/php-hal-dns
HALDNS_WITHOUT=/home/mauricio-vargas/projects/jotelulu/without/php-hal-dns
SDK_PATH=/home/mauricio-vargas/projects/jotelulu/php-bundle-client-hal-dns
```

### Branches detectados automáticamente

El Makefile detecta automáticamente:
- Branch actual de `php-hal-dns` (feature branch)
- Branch de `without/php-hal-dns` (main)

---

## 📝 Casos de Uso

### Caso 1: Desarrollo de nueva feature

```bash
# En php-hal-dns, trabajas en feature/PROD-1234
cd ~/projects/jotelulu/php-hal-dns
git checkout feature/PROD-1234

# Generas OpenAPI desde el código
docker exec php-hal-dns-php-1 php bin/console nelmio:apidoc:dump --format=yaml > docs/OpenApi/openapi.yaml

# Ejecutas el flujo completo
cd ~/projects/personal/diff-files
make release-full

# Revisas los cambios
# Si son MINOR/PATCH → aplicas al SDK
# Si son MAJOR → revisas con el equipo primero
```

### Caso 2: Solo verificar breaking changes

```bash
make diff-prepare
make diff-compare-breaking
```

Si no muestra nada → es seguro continuar.

### Caso 3: Ver cambios detallados línea a línea

```bash
make diff-full
make show-diff
```

---

## 🚨 Qué hacer según el resultado

### 🔴 MAJOR - Breaking Changes

**Resultado:** `Suggested version bump: **MAJOR**`

**Acción requerida:**
1. ⚠️ **NO regenerar SDK automáticamente**
2. 📋 Revisar TODOS los cambios en el reporte
3. 📣 Planificar comunicación con clientes
4. 📝 Documentar migration guide
5. 🏷️ Crear tag: `vX.0.0` (incrementa MAJOR)

### 🟡 MINOR - New Features

**Resultado:** `Suggested version bump: **MINOR**`

**Acción recomendada:**
1. ✅ Safe to regenerate SDK
2. 📝 Documentar nuevas features
3. 🏷️ Crear tag: `vX.Y.0` (incrementa MINOR)
4. 📦 Publicar SDK

### ✅ PATCH - Bug Fixes

**Resultado:** `Suggested version bump: **PATCH**`

**Acción recomendada:**
1. ✅ Safe to regenerate SDK
2. 🏷️ Crear tag: `vX.Y.Z` (incrementa PATCH)
3. 📦 Publicar SDK

---

## 🔍 Troubleshooting

### Error: "openapi.yaml not found"

Asegúrate de que los archivos existen:
```bash
ls ~/projects/jotelulu/php-hal-dns/docs/OpenApi/openapi.yaml
ls ~/projects/jotelulu/without/php-hal-dns/docs/OpenApi/openapi.yaml
```

Si falta el de without (main):
```bash
cd ~/projects/jotelulu/without/php-hal-dns
git checkout main
docker exec php-hal-dns-php-1 php bin/console nelmio:apidoc:dump --format=yaml > docs/OpenApi/openapi.yaml
```

### Error: "Could not determine bump type"

El archivo `RELEASE-NOTES.md` debe existir en `releases/vX.Y.Z/` con el formato correcto.

Verifica que contenga:
```markdown
🟡 **Type:** MINOR (New features, backward compatible)
```

### No se generan archivos de release

Ejecuta el flujo completo paso a paso:
```bash
make diff-full      # Primero genera los reportes
make release-info   # Verifica que se calcula el tag
make release-prepare # Genera los archivos
```

---

## 📚 Referencias

- **Semantic Versioning**: https://semver.org/
- **OpenAPI Spec**: https://swagger.io/specification/
- **Contexto del proyecto**: Ver `PROYECTO-CONTEXTO.md`

---

## 📦 Instalación

```bash
cd /home/mauricio-vargas/projects/personal/diff-files

# Instalar dependencias Python
pip install -r requirements.txt
```

**Dependencias:**
- `PyYAML>=6.0` - Parser de archivos YAML
- `rich>=13.0` - Salida con colores en terminal

---

## ✨ Resumen

Este proyecto automatiza el proceso completo de:

1. ✅ Comparar cambios entre branches de OpenAPI
2. ✅ Detectar breaking changes automáticamente
3. ✅ Calcular el siguiente tag semántico
4. ✅ Generar todos los archivos necesarios para el release
5. ✅ Mantener historial de releases documentado

**Comando único para todo:**
```bash
make release-full
```

---

**Creado por:** Mauricio Vargas
**Uso:** Jotelulu - SDK HAL DNS
**Última actualización:** 2026-01-28
