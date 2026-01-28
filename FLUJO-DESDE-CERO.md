# Flujo Completo desde Cero

Guía paso a paso para ejecutar el proceso completo de generación de release desde cero.

**Fecha creación:** 2026-01-28
**Autor:** Claude + Mauricio Vargas

---

## 📋 Pre-requisitos

1. Haber hecho cambios en `php-hal-dns` (feature branch)
2. Tener el branch `main` en `without/php-hal-dns` para comparar
3. Haber generado el OpenAPI desde el código actualizado

---

## 🚀 Comandos Exactos desde Cero

### Paso 1: Generar OpenAPI en php-hal-dns

```bash
cd ~/projects/jotelulu/php-hal-dns

# Asegúrate de estar en el branch correcto
git branch --show-current
# Output: feature/PROD-3958-openapi-endpoint-examples

# Generar OpenAPI desde el código
docker exec php-hal-dns-php-1 php bin/console nelmio:apidoc:dump --format=yaml > docs/OpenApi/openapi.yaml

# Verificar que se generó correctamente
ls -lh docs/OpenApi/openapi.yaml
```

---

### Paso 2: Ejecutar flujo completo automatizado

```bash
cd ~/projects/personal/diff-files

# COMANDO ÚNICO - Ejecuta todo el flujo
make release-full
```

**Este comando ejecuta automáticamente:**
1. ✅ Trae `openapi.yaml` de `without/php-hal-dns` (main)
2. ✅ Trae `openapi.yaml` de `php-hal-dns` (feature)
3. ✅ Normaliza ambos archivos (elimina UUIDs, timestamps, etc.)
4. ✅ Compara estructuralmente con `compare.py`
5. ✅ Genera git diff filtrado línea a línea
6. ✅ Calcula el siguiente tag (ej: 1.2.1 → 1.3.0)
7. ✅ Genera 5 archivos listos para usar

**Output esperado:**
```
═══════════════════════════════════════════════
   Flujo Completo: Diff + Release
═══════════════════════════════════════════════

Branches:
  OLD (main):    main
  NEW (feature): feature/PROD-3958-openapi-endpoint-examples

✓ YAMLs copiados y normalizados
✓ Comparación ejecutada

Suggested version bump: **MINOR**

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

✓ Proceso completo finalizado!
```

---

### Paso 3: Revisar archivos generados

```bash
# Ver archivos generados
ls -lh releases/v1.3.0/generated/

# Output:
# CHANGELOG.md
# README.md
# commit-message.txt
# tag-message.txt
# gitlab-release.md

# Ver el CHANGELOG generado
cat releases/v1.3.0/generated/CHANGELOG.md | head -20

# Ver el mensaje de commit
cat releases/v1.3.0/generated/commit-message.txt

# Ver el mensaje del tag
cat releases/v1.3.0/generated/tag-message.txt

# Ver el texto para GitLab Release
cat releases/v1.3.0/generated/gitlab-release.md
```

---

### Paso 4: Copiar archivos al SDK

```bash
# Copiar CHANGELOG y README al SDK
cp releases/v1.3.0/generated/CHANGELOG.md ~/projects/jotelulu/php-bundle-client-hal-dns/
cp releases/v1.3.0/generated/README.md ~/projects/jotelulu/php-bundle-client-hal-dns/

# Verificar que se copiaron correctamente
ls -lh ~/projects/jotelulu/php-bundle-client-hal-dns/{CHANGELOG.md,README.md}
```

---

### Paso 5: Crear commit en SDK

```bash
cd ~/projects/jotelulu/php-bundle-client-hal-dns

# Verificar branch actual
git branch --show-current
# Debe ser: feature/tag-1.3 o similar

# Ver cambios
git status
git diff CHANGELOG.md README.md

# Agregar archivos al stage
git add CHANGELOG.md README.md sdk-generator/openapi.yaml

# Crear commit usando el mensaje generado
git commit -F ~/projects/personal/diff-files/releases/v1.3.0/generated/commit-message.txt

# Verificar el commit
git log -1
```

**Commit creado:**
```
PROD-3958: Prepare 1.3.0 release

This release adds a new 404 response to `/api/zones/import` endpoint for handling cluster not found errors

Updated README.md and CHANGELOG.md

made: mau
```

---

### Paso 6: Crear tag

```bash
cd ~/projects/jotelulu/php-bundle-client-hal-dns

# Crear tag anotado usando el mensaje generado
git tag -a 1.3.0 -F ~/projects/personal/diff-files/releases/v1.3.0/generated/tag-message.txt

# Verificar el tag
git tag -l -n5 1.3.0

# Ver el tag completo
git show 1.3.0
```

**Tag creado:**
```
tag 1.3.0
Tagger: Mauricio Vargas

Release 1.3.0

This release adds a new 404 response to `/api/zones/import` endpoint for handling cluster not found errors.
- Backward compatible (MINOR release)
```

---

### Paso 7: Push del tag (CUIDADO)

```bash
cd ~/projects/jotelulu/php-bundle-client-hal-dns

# IMPORTANTE: Verificar todo antes de pushear
git log -1
git tag -l -n5 1.3.0

# Push del tag
git push origin 1.3.0
```

---

### Paso 8: Crear GitLab Release

1. **Ir a GitLab:**
   ```
   https://gitlab.jotelulu.com/jotelulu/php-bundle-client-hal-dns/-/releases/new
   ```

2. **Seleccionar tag:** `1.3.0`

3. **Copiar contenido del archivo:**
   ```bash
   cat ~/projects/personal/diff-files/releases/v1.3.0/generated/gitlab-release.md
   ```

4. **Pegar en GitLab Release:**
   ```markdown
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
   ```

5. **Publicar Release**

---

### Paso 9: Actualizar Panel (cuando sea necesario)

```bash
cd ~/projects/servers/dev-environments/panel.php

# Editar composer.json
nano composer.json

# Cambiar:
# "jotelulu/php-bundle-client-hal-dns": "^1.2"
# Por:
# "jotelulu/php-bundle-client-hal-dns": "^1.3"

# Actualizar dependencias
composer update jotelulu/php-bundle-client-hal-dns

# Verificar que se instaló la versión correcta
composer show jotelulu/php-bundle-client-hal-dns
```

---

## 🎯 Resumen del Flujo

```bash
# 1. Generar OpenAPI en php-hal-dns
cd ~/projects/jotelulu/php-hal-dns
docker exec php-hal-dns-php-1 php bin/console nelmio:apidoc:dump --format=yaml > docs/OpenApi/openapi.yaml

# 2. Ejecutar flujo automatizado (COMANDO ÚNICO)
cd ~/projects/personal/diff-files
make release-full

# 3. Revisar archivos generados
ls -lh releases/v1.3.0/generated/

# 4. Copiar al SDK
cp releases/v1.3.0/generated/CHANGELOG.md ~/projects/jotelulu/php-bundle-client-hal-dns/
cp releases/v1.3.0/generated/README.md ~/projects/jotelulu/php-bundle-client-hal-dns/

# 5. Crear commit
cd ~/projects/jotelulu/php-bundle-client-hal-dns
git add CHANGELOG.md README.md sdk-generator/openapi.yaml
git commit -F ~/projects/personal/diff-files/releases/v1.3.0/generated/commit-message.txt

# 6. Crear tag
git tag -a 1.3.0 -F ~/projects/personal/diff-files/releases/v1.3.0/generated/tag-message.txt

# 7. Push tag
git push origin 1.3.0

# 8. Crear GitLab Release (manual en web)

# 9. Actualizar Panel (cuando sea necesario)
```

---

## 🔧 Comandos Útiles

### Ver información del próximo release

```bash
cd ~/projects/personal/diff-files
make release-info
```

### Solo verificar breaking changes

```bash
cd ~/projects/personal/diff-files
make diff-prepare
make diff-compare-breaking
```

### Ver último git diff en terminal

```bash
cd ~/projects/personal/diff-files
make show-diff
```

### Limpiar archivos temporales

```bash
cd ~/projects/personal/diff-files
make clean
```

---

## ⚠️ Notas Importantes

1. **NO hacer commits ni push hasta revisar TODO**
2. **Verificar siempre el tipo de bump** (MAJOR/MINOR/PATCH)
3. **Si es MAJOR**, revisar con el equipo antes de proceder
4. **Los archivos generados son una base** - revisar antes de usar
5. **El flujo es idempotente** - puedes ejecutar `make release-full` múltiples veces

---

## 🚨 Troubleshooting

### Error: "openapi.yaml not found"

```bash
# Verificar que existen los archivos
ls ~/projects/jotelulu/php-hal-dns/docs/OpenApi/openapi.yaml
ls ~/projects/jotelulu/without/php-hal-dns/docs/OpenApi/openapi.yaml

# Si falta el de without (main), generarlo
cd ~/projects/jotelulu/without/php-hal-dns
git checkout main
docker exec php-hal-dns-php-1 php bin/console nelmio:apidoc:dump --format=yaml > docs/OpenApi/openapi.yaml
```

### Error: "Could not calculate next tag"

```bash
# Verificar que hay un tag en el SDK
cd ~/projects/jotelulu/php-bundle-client-hal-dns
git tag --sort=-v:refname | head -5
```

### Los archivos generados no son correctos

```bash
# Ejecutar paso a paso para debugear
cd ~/projects/personal/diff-files

make diff-prepare   # Trae y normaliza YAMLs
make diff-compare   # Compara cambios
make release-info   # Muestra info del release
make release-prepare # Genera archivos
```

---

**Fin del documento**
