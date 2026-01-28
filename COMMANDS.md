# ⚙️ Comandos Disponibles - OpenAPI Diff System

Referencia rápida de todos los comandos disponibles en el sistema.

> **Nota:** Todos los comandos se ejecutan desde `~/projects/main`

---

## 🚀 Comandos Principales

### `make openapi-save-main`
**Descripción:** Genera OpenAPI desde la rama `main` y lo guarda como referencia.

**Cuándo usarlo:**
- Primera vez que configuras el sistema
- Cuando `main` tiene cambios importantes y quieres actualizar la referencia

**Qué hace:**
1. Limpia cache de Symfony
2. Genera OpenAPI desde código actual
3. Normaliza UUIDs, timestamps, serverNames
4. Guarda en `without/php-hal-dns/openapi-main.yaml`

**Ejemplo:**
```bash
# Primero asegúrate de estar en main
cd ~/projects/jotelulu/php-hal-dns
git checkout main
git pull

# Luego genera la referencia
cd ~/projects/main
make openapi-save-main
```

**Output:**
```
Generating OpenAPI from current code...
Normalizing (fixing UUIDs, timestamps)...
✓ Main OpenAPI saved: openapi-main.yaml (2835 lines)
  - 128 UUIDs normalized
  - 110 timestamps normalized
  - 16 serverNames/IDs normalized
```

---

### `make openapi-generate`
**Descripción:** Genera archivos OpenAPI OLD (main) y NEW (rama actual) normalizados.

**Cuándo usarlo:**
- Cuando solo quieres generar los archivos sin compararlos
- Para debug o verificación manual

**Qué hace:**
1. Limpia directorios docs/ y gitdiff/
2. Copia OLD desde `openapi-main.yaml` y normaliza
3. Genera NEW desde contenedor actual y normaliza
4. Crea archivo info.md con metadata

**Ejemplo:**
```bash
cd ~/projects/main
make openapi-generate
```

**Output:**
```
Cleaning docs and gitdiff directories...
✓ Docs and gitdiff directories ready

Copying OLD OpenAPI (main from without)...
✓ OLD copied: openapi_old.yaml (2835 lines)

Generating NEW OpenAPI (feature/PROD-3958)...
✓ NEW generated: openapi.yaml (2895 lines)
```

---

### `make openapi-diff`
**Descripción:** Compara OLD vs NEW usando Python tool (cambios estructurales).

**Cuándo usarlo:**
- Cuando ya tienes los archivos generados y solo quieres ver el diff
- Para re-ejecutar la comparación sin regenerar

**Qué hace:**
1. Ejecuta `compare.py` sobre los archivos
2. Detecta paths/schemas/responses añadidos/eliminados/modificados
3. Sugiere version bump (MAJOR/MINOR/PATCH)
4. Guarda resultados en info.md

**Ejemplo:**
```bash
cd ~/projects/main
make openapi-diff
```

**Output:**
```
Comparing: main vs feature/PROD-3958

## Paths
### 🟢 Added
### 🔴 Removed
### 🟡 Modified
* /api/zones/import

## 🟡 Suggested version bump: MINOR
```

---

### `make openapi-gitdiff`
**Descripción:** Genera diff línea por línea usando git diff.

**Cuándo usarlo:**
- Cuando quieres ver cambios detallados línea por línea
- Para inspeccionar cambios en ejemplos, descripciones, etc.

**Qué hace:**
1. Ejecuta `git diff --no-index` entre OLD y NEW
2. Filtra ruido (UUIDs, timestamps normalizados)
3. Guarda en markdown con formato diff
4. Cuenta líneas añadidas/eliminadas

**Ejemplo:**
```bash
cd ~/projects/main
make openapi-gitdiff
```

**Output:**
```
Generating git diff report...
Filtering noise (UUIDs, timestamps, serverNames)...
✓ Git diff saved: 2026-01-27-feature-PROD-3958-gitdiff.md
  Lines in diff: 180
```

---

### `make openapi-gitdiff-show`
**Descripción:** Muestra el último reporte de git diff en terminal con colores.

**Cuándo usarlo:**
- Para revisar cambios detallados sin abrir el archivo
- Después de ejecutar `openapi-gitdiff`

**Qué hace:**
1. Encuentra el último archivo gitdiff generado
2. Lo muestra con formato coloreado en terminal

**Ejemplo:**
```bash
cd ~/projects/main
make openapi-gitdiff-show
```

---

### `make openapi-update-full` ⭐ RECOMENDADO
**Descripción:** Ejecuta el flujo completo: generar → comparar → gitdiff.

**Cuándo usarlo:**
- **SIEMPRE** que quieras comparar una rama feature con main
- Es el comando más usado del sistema

**Qué hace:**
1. `openapi-generate` - Genera OLD y NEW
2. `openapi-diff` - Compara con Python tool
3. `openapi-gitdiff` - Genera git diff detallado
4. Muestra resumen con próximos pasos

**Ejemplo:**
```bash
# Estando en tu rama feature
cd ~/projects/jotelulu/php-hal-dns
git checkout feature/mi-feature

# Ejecutar comparación completa
cd ~/projects/main
make openapi-update-full
```

**Output final:**
```
✓ Full workflow completed!

Files generated:
  Docs: docs/
    - openapi_old.yaml (main)
    - openapi.yaml (feature/mi-feature)
    - 2026-01-27-feature-mi-feature.md

  Git Diff: gitdiff/
    - 2026-01-27-feature-mi-feature-gitdiff.md

Next steps based on version bump:
  🔴 MAJOR - Breaking changes
  🟡 MINOR - New features
  ✅ PATCH - Bug fixes
```

---

## 📦 Comandos de SDK

### `make openapi-copy`
**Descripción:** Copia el OpenAPI NEW al generador de SDK.

**Cuándo usarlo:**
- Después de aprobar los cambios del diff
- Antes de regenerar el SDK

**Qué hace:**
1. Verifica que openapi.yaml existe
2. Hace backup del OpenAPI anterior en SDK
3. Copia el nuevo al generador

**Ejemplo:**
```bash
cd ~/projects/main
make openapi-copy
```

---

### `make sdk-generate`
**Descripción:** Regenera el SDK usando el OpenAPI copiado.

**Cuándo usarlo:**
- Después de copiar el OpenAPI nuevo
- Para generar el cliente PHP actualizado

**Qué hace:**
1. Ejecuta el generador de SDK en contenedor
2. Genera código PHP del cliente
3. Actualiza archivos del SDK

**Ejemplo:**
```bash
cd ~/projects/main
make sdk-generate
```

---

### `make openapi-update`
**Descripción:** Flujo completo + copia + regenera SDK.

**⚠️ NO RECOMENDADO:** Mejor ejecutar pasos manualmente.

**Por qué:**
- No da oportunidad de revisar cambios
- Puede regenerar SDK con breaking changes sin supervisión

**Uso (solo si estás seguro):**
```bash
cd ~/projects/main
make openapi-update
```

---

## 🐚 Comandos de Docker

### `make in-sdk`
**Descripción:** Entra al bash del contenedor SDK.

**Ejemplo:**
```bash
cd ~/projects/main
make in-sdk
```

---

## 📊 Resumen por Escenario

### Escenario 1: Primera vez configurando
```bash
# Setup inicial
cd ~/projects/main
make openapi-save-main

# Listo, ya puedes comparar branches
```

---

### Escenario 2: Trabajando en una feature
```bash
# 1. Desarrollar en feature branch
cd ~/projects/jotelulu/php-hal-dns
git checkout -b feature/nueva-funcionalidad
# ... hacer cambios ...

# 2. Comparar con main
cd ~/projects/main
make openapi-update-full

# 3. Revisar resultados
make openapi-gitdiff-show

# 4. Si es MINOR o PATCH, regenerar SDK
make openapi-copy
make sdk-generate
```

---

### Escenario 3: Actualizar referencia de main
```bash
# Main tiene cambios, actualizar referencia
cd ~/projects/jotelulu/php-hal-dns
git checkout main
git pull

cd ~/projects/main
make openapi-save-main
```

---

### Escenario 4: Solo quiero ver diferencias rápido
```bash
cd ~/projects/main
make openapi-update-full | grep -A 20 "Suggested version bump"
```

---

### Escenario 5: Re-comparar sin regenerar
```bash
# Si los archivos ya están generados
cd ~/projects/main
make openapi-diff
make openapi-gitdiff
make openapi-gitdiff-show
```

---

## 🎯 Comando según tu objetivo

| Objetivo | Comando |
|----------|---------|
| 🔧 Setup inicial | `make openapi-save-main` |
| 🔍 Comparar feature vs main | `make openapi-update-full` |
| 👀 Ver diff detallado | `make openapi-gitdiff-show` |
| 📦 Regenerar SDK | `make openapi-copy && make sdk-generate` |
| 🔄 Actualizar main reference | `make openapi-save-main` |
| 🐛 Debug/verificación | `make openapi-generate` |

---

## 📚 Ver también

- **README.md** - Documentación completa del sistema
- **SETUP.md** - Guía de configuración inicial
- **releases/** - Historial de versiones
- **devops/mk/openapi.mk** - Código fuente de los comandos
