# 📦 Release v1.3.0

**Tag:** v1.3.0
**Date:** 2026-01-27
**Type:** 🟡 MINOR
**Previous:** v1.2.1

---

## 📄 Archivos

- **RELEASE-NOTES.md** - Notas de release completas con detalles técnicos
- **2026-01-27-feature-PROD-3958-openapi-endpoint-examples.md** - Reporte Python tool
- **2026-01-27-feature-PROD-3958-openapi-endpoint-examples-gitdiff.md** - Git diff detallado

---

## 🎯 Resumen Ejecutivo

**Cambio principal:** Añadida respuesta 404 al endpoint `/api/zones/import` para manejar casos de cluster no encontrado.

**Impacto:** Backward compatible - Los clientes existentes seguirán funcionando. Los nuevos clientes pueden manejar el error 404 apropiadamente.

**Acción requerida:** Opcional - Actualizar clientes para manejar nueva respuesta 404.

---

## ✅ Checklist de Release

- [ ] Revisar RELEASE-NOTES.md
- [ ] Verificar cambios en git diff
- [ ] Ejecutar `make openapi-copy`
- [ ] Ejecutar `make sdk-generate`
- [ ] Crear tag en SDK: `git tag v1.3.0`
- [ ] Push tag: `git push origin v1.3.0`
- [ ] Publicar en packagist (si aplica)
- [ ] Notificar consumidores del API (opcional)

---

## 📚 Documentación

Ver documentación del sistema completo en: `../../README.md`
