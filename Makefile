# OpenAPI Diff & Release Generator
# Automatiza el flujo completo: traer YAMLs → comparar → generar release files

# Colors
RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[1;33m
CYAN=\033[0;36m
MAGENTA=\033[0;35m
NC=\033[0m # No Color

# Paths
HALDNS_PATH=/home/mauricio-vargas/projects/jotelulu/php-hal-dns
HALDNS_WITHOUT=/home/mauricio-vargas/projects/jotelulu/without/php-hal-dns
SDK_PATH=/home/mauricio-vargas/projects/jotelulu/php-bundle-client-hal-dns
DIFF_PROJECT=$(shell pwd)

# Directories
DOCS_DIR=$(DIFF_PROJECT)/docs
GITDIFF_DIR=$(DIFF_PROJECT)/gitdiff
RELEASES_DIR=$(DIFF_PROJECT)/releases

# Get current branch names
CURRENT_BRANCH := $(shell cd $(HALDNS_PATH) && git branch --show-current)
MAIN_BRANCH := $(shell cd $(HALDNS_WITHOUT) && git branch --show-current)
CURRENT_BRANCH_SAFE := $(shell cd $(HALDNS_PATH) && git branch --show-current | sed 's/\//-/g')

# OpenAPI files
OPENAPI_OLD=$(DOCS_DIR)/openapi_old.yaml
OPENAPI_NEW=$(DOCS_DIR)/openapi.yaml
OPENAPI_INFO=$(DOCS_DIR)/$(shell date +%Y-%m-%d)-$(CURRENT_BRANCH_SAFE).md
GITDIFF_FILE=$(GITDIFF_DIR)/$(shell date +%Y-%m-%d)-$(CURRENT_BRANCH_SAFE)-gitdiff.md

.PHONY: help
help:
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo "$(MAGENTA)   OpenAPI Diff & Release Generator$(NC)"
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(CYAN)📊 Diff Commands:$(NC)"
	@echo "  $(YELLOW)make diff-prepare$(NC)       - Traer YAMLs y preparar comparación"
	@echo "  $(YELLOW)make diff-compare$(NC)       - Ejecutar compare.py (cambios estructurales)"
	@echo "  $(YELLOW)make diff-gitdiff$(NC)       - Generar git diff filtrado línea a línea"
	@echo "  $(YELLOW)make diff-full$(NC)          - Flujo completo: prepare + compare + gitdiff"
	@echo ""
	@echo "$(CYAN)🏷️  Release Commands:$(NC)"
	@echo "  $(YELLOW)make release-init$(NC)       - Crear estructura de release (carpetas vX.Y.Z)"
	@echo "  $(YELLOW)make release-notes$(NC)      - Generar RELEASE-NOTES.md desde diff results"
	@echo "  $(YELLOW)make release-prepare$(NC)    - Calcular tag y generar archivos de release"
	@echo "  $(YELLOW)make release-info$(NC)       - Mostrar info del próximo release"
	@echo "  $(YELLOW)make release-apply$(NC)      - Copiar archivos generados al SDK repo"
	@echo "  $(YELLOW)make release-full$(NC)       - Flujo completo: diff + init + notes + prepare"
	@echo ""
	@echo "$(CYAN)🔧 Utility Commands:$(NC)"
	@echo "  $(YELLOW)make clean$(NC)              - Limpiar docs/ y gitdiff/"
	@echo "  $(YELLOW)make info$(NC)               - Mostrar información de archivos y branches"
	@echo "  $(YELLOW)make show-diff$(NC)          - Mostrar último gitdiff en terminal"
	@echo ""

######### DIFF PREPARATION #########

.PHONY: diff-prepare
diff-prepare:
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo "$(MAGENTA)   Preparando OpenAPI Diff$(NC)"
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(CYAN)Branches:$(NC)"
	@echo "  OLD (main):    $(YELLOW)$(MAIN_BRANCH)$(NC)"
	@echo "  NEW (feature): $(YELLOW)$(CURRENT_BRANCH)$(NC)"
	@echo ""
	@# Clean and create directories
	@echo "$(YELLOW)Limpiando directorios...$(NC)"
	@mkdir -p $(DOCS_DIR) $(GITDIFF_DIR)
	@rm -f $(DOCS_DIR)/*.yaml $(DOCS_DIR)/*.md
	@rm -f $(GITDIFF_DIR)/*.md $(GITDIFF_DIR)/*.md.backup $(GITDIFF_DIR)/*.yaml
	@echo "$(GREEN)✓ Directorios listos$(NC)"
	@echo ""
	@# Copy OLD from without (main branch)
	@echo "$(CYAN)Copiando OLD OpenAPI ($(MAIN_BRANCH))...$(NC)"
	@if [ ! -f "$(HALDNS_WITHOUT)/docs/OpenApi/openapi.yaml" ]; then \
		echo "$(RED)Error: openapi.yaml not found in without/php-hal-dns$(NC)"; \
		exit 1; \
	fi
	@cp $(HALDNS_WITHOUT)/docs/OpenApi/openapi.yaml $(OPENAPI_OLD)
	@echo "$(YELLOW)Normalizando OLD (UUIDs, timestamps, IDs)...$(NC)"
	@python3 normalize-openapi.py $(OPENAPI_OLD)
	@echo "$(GREEN)✓ OLD copiado: $$(wc -l < $(OPENAPI_OLD)) líneas$(NC)"
	@echo ""
	@# Copy NEW from current branch
	@echo "$(CYAN)Copiando NEW OpenAPI ($(CURRENT_BRANCH))...$(NC)"
	@if [ ! -f "$(HALDNS_PATH)/docs/OpenApi/openapi.yaml" ]; then \
		echo "$(RED)Error: openapi.yaml not found in php-hal-dns$(NC)"; \
		exit 1; \
	fi
	@cp $(HALDNS_PATH)/docs/OpenApi/openapi.yaml $(OPENAPI_NEW)
	@echo "$(YELLOW)Normalizando NEW (UUIDs, timestamps, IDs)...$(NC)"
	@python3 normalize-openapi.py $(OPENAPI_NEW)
	@echo "$(GREEN)✓ NEW copiado: $$(wc -l < $(OPENAPI_NEW)) líneas$(NC)"
	@echo ""
	@# Generate info file
	@echo "$(CYAN)Creando archivo de información...$(NC)"
	@echo "# 📊 OpenAPI Comparison Report" > $(OPENAPI_INFO)
	@echo "" >> $(OPENAPI_INFO)
	@echo "📅 **Date:** $$(date '+%Y-%m-%d %H:%M:%S')" >> $(OPENAPI_INFO)
	@echo "" >> $(OPENAPI_INFO)
	@echo "## 🔀 Branches Compared" >> $(OPENAPI_INFO)
	@echo "" >> $(OPENAPI_INFO)
	@echo "- 🔵 **OLD (base):** \`$(MAIN_BRANCH)\` from \`without/php-hal-dns\`" >> $(OPENAPI_INFO)
	@echo "- 🟢 **NEW (current):** \`$(CURRENT_BRANCH)\` from \`php-hal-dns\`" >> $(OPENAPI_INFO)
	@echo "" >> $(OPENAPI_INFO)
	@echo "## 📄 Files" >> $(OPENAPI_INFO)
	@echo "" >> $(OPENAPI_INFO)
	@echo "- \`openapi_old.yaml\` - $$(wc -l < $(OPENAPI_OLD)) lines" >> $(OPENAPI_INFO)
	@echo "- \`openapi.yaml\` - $$(wc -l < $(OPENAPI_NEW)) lines" >> $(OPENAPI_INFO)
	@echo "" >> $(OPENAPI_INFO)
	@echo "## ⚙️ Commands" >> $(OPENAPI_INFO)
	@echo "" >> $(OPENAPI_INFO)
	@echo "\`\`\`bash" >> $(OPENAPI_INFO)
	@echo "# Compare changes" >> $(OPENAPI_INFO)
	@echo "cd $(DIFF_PROJECT)" >> $(OPENAPI_INFO)
	@echo "python3 compare.py docs/openapi_old.yaml docs/openapi.yaml" >> $(OPENAPI_INFO)
	@echo "" >> $(OPENAPI_INFO)
	@echo "# Only breaking changes" >> $(OPENAPI_INFO)
	@echo "python3 compare.py docs/openapi_old.yaml docs/openapi.yaml --breaking" >> $(OPENAPI_INFO)
	@echo "\`\`\`" >> $(OPENAPI_INFO)
	@echo "$(GREEN)✓ Info file: $(OPENAPI_INFO)$(NC)"
	@echo ""
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)✓ Preparación completada!$(NC)"
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"

######### DIFF COMPARISON #########

.PHONY: diff-compare
diff-compare:
	@if [ ! -f "$(OPENAPI_OLD)" ] || [ ! -f "$(OPENAPI_NEW)" ]; then \
		echo "$(RED)Error: Archivos OpenAPI no encontrados. Ejecuta 'make diff-prepare' primero.$(NC)"; \
		exit 1; \
	fi
	@echo "$(CYAN)Comparando: $(YELLOW)$(MAIN_BRANCH)$(CYAN) vs $(YELLOW)$(CURRENT_BRANCH)$(NC)"
	@echo ""
	@python3 compare.py docs/openapi_old.yaml docs/openapi.yaml
	@echo ""
	@echo "$(YELLOW)Guardando resultados en info file...$(NC)"
	@echo "" >> $(OPENAPI_INFO)
	@echo "## Python Diff Tool Results" >> $(OPENAPI_INFO)
	@echo "" >> $(OPENAPI_INFO)
	@echo "\`\`\`" >> $(OPENAPI_INFO)
	@python3 compare.py docs/openapi_old.yaml docs/openapi.yaml >> $(OPENAPI_INFO)
	@echo "\`\`\`" >> $(OPENAPI_INFO)
	@echo "$(GREEN)✓ Resultados guardados en: $(OPENAPI_INFO)$(NC)"

.PHONY: diff-compare-breaking
diff-compare-breaking:
	@if [ ! -f "$(OPENAPI_OLD)" ] || [ ! -f "$(OPENAPI_NEW)" ]; then \
		echo "$(RED)Error: Archivos OpenAPI no encontrados. Ejecuta 'make diff-prepare' primero.$(NC)"; \
		exit 1; \
	fi
	@echo "$(CYAN)Verificando breaking changes: $(YELLOW)$(MAIN_BRANCH)$(CYAN) vs $(YELLOW)$(CURRENT_BRANCH)$(NC)"
	@echo ""
	@python3 compare.py docs/openapi_old.yaml docs/openapi.yaml --breaking

######### GIT DIFF #########

.PHONY: diff-gitdiff
diff-gitdiff:
	@if [ ! -f "$(OPENAPI_OLD)" ] || [ ! -f "$(OPENAPI_NEW)" ]; then \
		echo "$(RED)Error: Archivos OpenAPI no encontrados. Ejecuta 'make diff-prepare' primero.$(NC)"; \
		exit 1; \
	fi
	@echo "$(CYAN)Generando git diff filtrado...$(NC)"
	@mkdir -p $(GITDIFF_DIR)
	@echo "# 📊 Git Diff - OpenAPI Comparison" > $(GITDIFF_FILE)
	@echo "" >> $(GITDIFF_FILE)
	@echo "📅 **Date:** $$(date '+%Y-%m-%d %H:%M:%S')" >> $(GITDIFF_FILE)
	@echo "🔀 **Branches:** \`$(MAIN_BRANCH)\` vs \`$(CURRENT_BRANCH)\`" >> $(GITDIFF_FILE)
	@echo "" >> $(GITDIFF_FILE)
	@echo "## 📝 Summary" >> $(GITDIFF_FILE)
	@echo "" >> $(GITDIFF_FILE)
	@echo "- 📄 **OLD:** \`openapi_old.yaml\` ($$(wc -l < $(OPENAPI_OLD)) lines) - $(MAIN_BRANCH)" >> $(GITDIFF_FILE)
	@echo "- 📄 **NEW:** \`openapi.yaml\` ($$(wc -l < $(OPENAPI_NEW)) lines) - $(CURRENT_BRANCH)" >> $(GITDIFF_FILE)
	@ADDED=$$(git diff --no-index $(OPENAPI_OLD) $(OPENAPI_NEW) 2>/dev/null | grep -c "^+" || echo "0"); \
	REMOVED=$$(git diff --no-index $(OPENAPI_OLD) $(OPENAPI_NEW) 2>/dev/null | grep -c "^-" || echo "0"); \
	echo "- 📈 **Changes:** 🟢 $$ADDED lines added, 🔴 $$REMOVED lines removed" >> $(GITDIFF_FILE)
	@echo "" >> $(GITDIFF_FILE)
	@echo "## 🔍 Git Diff Output" >> $(GITDIFF_FILE)
	@echo "" >> $(GITDIFF_FILE)
	@echo "\`\`\`diff" >> $(GITDIFF_FILE)
	@git diff --no-index $(OPENAPI_OLD) $(OPENAPI_NEW) 2>/dev/null | tail -n +6 >> $(GITDIFF_FILE) || echo "No differences found" >> $(GITDIFF_FILE)
	@echo "\`\`\`" >> $(GITDIFF_FILE)
	@echo "$(YELLOW)Filtrando ruido (UUIDs, timestamps, IDs)...$(NC)"
	@python3 filter-gitdiff.py $(GITDIFF_FILE)
	@echo "$(GREEN)✓ Git diff guardado: $(GITDIFF_FILE)$(NC)"
	@echo "$(CYAN)  Líneas en diff: $$(wc -l < $(GITDIFF_FILE))$(NC)"

.PHONY: show-diff
show-diff:
	@LAST_DIFF=$$(ls -t $(GITDIFF_DIR)/*.md 2>/dev/null | head -1); \
	if [ -z "$$LAST_DIFF" ]; then \
		echo "$(RED)No se encontraron reportes. Ejecuta 'make diff-gitdiff' primero.$(NC)"; \
		exit 1; \
	fi; \
	echo "$(CYAN)Mostrando último git diff:$(NC) $$(basename $$LAST_DIFF)"; \
	echo ""; \
	python3 show-diff.py $$LAST_DIFF

######### FULL DIFF WORKFLOW #########

.PHONY: diff-full
diff-full:
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo "$(MAGENTA)   Flujo Completo de Diff$(NC)"
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo ""
	@$(MAKE) diff-prepare
	@echo ""
	@echo "$(CYAN)═══════════════════════════════════════════════$(NC)"
	@echo "$(CYAN)   Comparando Cambios$(NC)"
	@echo "$(CYAN)═══════════════════════════════════════════════$(NC)"
	@echo ""
	@$(MAKE) diff-compare
	@echo ""
	@echo "$(CYAN)═══════════════════════════════════════════════$(NC)"
	@echo "$(CYAN)   Generando Git Diff$(NC)"
	@echo "$(CYAN)═══════════════════════════════════════════════$(NC)"
	@echo ""
	@$(MAKE) diff-gitdiff
	@echo ""
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)✓ Diff completo generado!$(NC)"
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(YELLOW)Archivos generados:$(NC)"
	@echo "  📁 $(DOCS_DIR)/"
	@echo "     - openapi_old.yaml"
	@echo "     - openapi.yaml"
	@echo "     - $$(basename $(OPENAPI_INFO))"
	@echo "  📁 $(GITDIFF_DIR)/"
	@echo "     - $$(basename $(GITDIFF_FILE))"
	@echo ""
	@echo "$(YELLOW)Siguiente paso:$(NC)"
	@echo "  make release-full    $(CYAN)# Crear release completo$(NC)"
	@echo ""

######### RELEASE GENERATION #########

.PHONY: release-init
release-init:
	@echo "$(CYAN)Inicializando estructura de release...$(NC)"
	@NEXT_TAG=$$(python3 get-next-tag.py 2>/dev/null | grep "✨ Next tag:" | awk '{print $$4}'); \
	if [ -z "$$NEXT_TAG" ]; then \
		echo "$(RED)Error: No se pudo calcular el siguiente tag$(NC)"; \
		echo "$(YELLOW)Ejecuta 'make diff-full' primero para generar los reportes$(NC)"; \
		exit 1; \
	fi; \
	RELEASE_DIR=$(RELEASES_DIR)/v$$NEXT_TAG; \
	mkdir -p $$RELEASE_DIR; \
	echo "$(GREEN)✓ Estructura creada: $$RELEASE_DIR$(NC)"

.PHONY: release-notes
release-notes:
	@echo "$(CYAN)Generando RELEASE-NOTES.md...$(NC)"
	@NEXT_TAG=$$(python3 get-next-tag.py 2>/dev/null | grep "✨ Next tag:" | awk '{print $$4}'); \
	if [ -z "$$NEXT_TAG" ]; then \
		echo "$(RED)Error: No se pudo calcular el siguiente tag$(NC)"; \
		exit 1; \
	fi; \
	RELEASE_DIR=$(RELEASES_DIR)/v$$NEXT_TAG; \
	mkdir -p $$RELEASE_DIR; \
	if [ -f "$(OPENAPI_INFO)" ]; then \
		cp $(OPENAPI_INFO) $$RELEASE_DIR/$$(basename $(OPENAPI_INFO)); \
		echo "$(GREEN)✓ Copiado: $$(basename $(OPENAPI_INFO))$(NC)"; \
	fi; \
	if [ -f "$(GITDIFF_FILE)" ]; then \
		cp $(GITDIFF_FILE) $$RELEASE_DIR/$$(basename $(GITDIFF_FILE)); \
		echo "$(GREEN)✓ Copiado: $$(basename $(GITDIFF_FILE))$(NC)"; \
	fi; \
	echo "$(YELLOW)Nota: RELEASE-NOTES.md debe crearse manualmente con el contenido de los reportes$(NC)"

.PHONY: release-prepare
release-prepare:
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo "$(MAGENTA)   Preparando Release$(NC)"
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo ""
	@python3 get-next-tag.py
	@echo ""
	@echo "$(CYAN)Generando archivos de release...$(NC)"
	@python3 generate-release-files.py
	@echo ""
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)✓ Release preparado!$(NC)"
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"

.PHONY: release-info
release-info:
	@python3 get-next-tag.py

.PHONY: release-apply
release-apply:
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo "$(MAGENTA)   Aplicando Release al SDK$(NC)"
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo ""
	@# Get next tag
	@NEXT_TAG=$$(python3 get-next-tag.py 2>/dev/null | grep "✨ Next tag:" | awk '{print $$4}'); \
	if [ -z "$$NEXT_TAG" ]; then \
		echo "$(RED)Error: No se pudo calcular el siguiente tag$(NC)"; \
		echo "$(YELLOW)Ejecuta 'make release-full' primero$(NC)"; \
		exit 1; \
	fi; \
	RELEASE_DIR=$(RELEASES_DIR)/v$$NEXT_TAG/generated; \
	echo "$(CYAN)Tag detectado: $(YELLOW)$$NEXT_TAG$(NC)"; \
	echo "$(CYAN)Release dir: $(YELLOW)$$RELEASE_DIR$(NC)"; \
	echo ""; \
	if [ ! -d "$$RELEASE_DIR" ]; then \
		echo "$(RED)Error: Release directory not found: $$RELEASE_DIR$(NC)"; \
		echo "$(YELLOW)Ejecuta 'make release-prepare' primero$(NC)"; \
		exit 1; \
	fi; \
	echo "$(CYAN)Verificando archivos...$(NC)"; \
	MISSING=0; \
	if [ ! -f "$$RELEASE_DIR/CHANGELOG.md" ]; then \
		echo "$(RED)  ✗ CHANGELOG.md no encontrado$(NC)"; \
		MISSING=1; \
	else \
		echo "$(GREEN)  ✓ CHANGELOG.md$(NC)"; \
	fi; \
	if [ ! -f "$$RELEASE_DIR/README.md" ]; then \
		echo "$(RED)  ✗ README.md no encontrado$(NC)"; \
		MISSING=1; \
	else \
		echo "$(GREEN)  ✓ README.md$(NC)"; \
	fi; \
	if [ ! -f "$$RELEASE_DIR/commit-message.txt" ]; then \
		echo "$(YELLOW)  ⚠ commit-message.txt no encontrado$(NC)"; \
	else \
		echo "$(GREEN)  ✓ commit-message.txt$(NC)"; \
	fi; \
	if [ ! -f "$$RELEASE_DIR/tag-message.txt" ]; then \
		echo "$(YELLOW)  ⚠ tag-message.txt no encontrado$(NC)"; \
	else \
		echo "$(GREEN)  ✓ tag-message.txt$(NC)"; \
	fi; \
	echo ""; \
	if [ $$MISSING -eq 1 ]; then \
		echo "$(RED)Error: Faltan archivos requeridos$(NC)"; \
		exit 1; \
	fi; \
	echo "$(CYAN)Verificando SDK repo...$(NC)"; \
	if [ ! -d "$(SDK_PATH)" ]; then \
		echo "$(RED)Error: SDK repo no encontrado: $(SDK_PATH)$(NC)"; \
		exit 1; \
	fi; \
	SDK_BRANCH=$$(cd $(SDK_PATH) && git branch --show-current); \
	echo "$(GREEN)  ✓ SDK repo encontrado$(NC)"; \
	echo "$(CYAN)  Branch actual: $(YELLOW)$$SDK_BRANCH$(NC)"; \
	echo ""; \
	echo "$(YELLOW)Copiando archivos al SDK...$(NC)"; \
	cp $$RELEASE_DIR/CHANGELOG.md $(SDK_PATH)/; \
	echo "$(GREEN)  ✓ CHANGELOG.md → $(SDK_PATH)/CHANGELOG.md$(NC)"; \
	cp $$RELEASE_DIR/README.md $(SDK_PATH)/; \
	echo "$(GREEN)  ✓ README.md → $(SDK_PATH)/README.md$(NC)"; \
	if [ -f "$(OPENAPI_NEW)" ]; then \
		cp $(OPENAPI_NEW) $(SDK_PATH)/sdk-generator/openapi.yaml; \
		echo "$(GREEN)  ✓ openapi.yaml → $(SDK_PATH)/sdk-generator/openapi.yaml$(NC)"; \
	else \
		echo "$(YELLOW)  ⚠ openapi.yaml no encontrado, no copiado$(NC)"; \
	fi; \
	echo ""; \
	echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"; \
	echo "$(GREEN)✓ Archivos copiados al SDK!$(NC)"; \
	echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"; \
	echo ""; \
	echo "$(YELLOW)Siguientes pasos:$(NC)"; \
	echo ""; \
	echo "  $(CYAN)1. Ver cambios:$(NC)"; \
	echo "     cd $(SDK_PATH)"; \
	echo "     git status"; \
	echo "     git diff CHANGELOG.md README.md"; \
	echo ""; \
	echo "  $(CYAN)2. Crear commit:$(NC)"; \
	echo "     git add CHANGELOG.md README.md sdk-generator/openapi.yaml"; \
	echo "     git commit -F $$RELEASE_DIR/commit-message.txt"; \
	echo ""; \
	echo "  $(CYAN)3. Crear tag:$(NC)"; \
	echo "     git tag -a $$NEXT_TAG -F $$RELEASE_DIR/tag-message.txt"; \
	echo ""; \
	echo "  $(CYAN)4. Push tag:$(NC)"; \
	echo "     git push origin $$NEXT_TAG"; \
	echo ""; \
	echo "  $(CYAN)5. GitLab Release:$(NC)"; \
	echo "     cat $$RELEASE_DIR/gitlab-release.md"; \
	echo ""

.PHONY: release-full
release-full:
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo "$(MAGENTA)   Flujo Completo: Diff + Release$(NC)"
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo ""
	@$(MAKE) diff-full
	@echo ""
	@$(MAKE) release-prepare
	@echo ""
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)✓ Proceso completo finalizado!$(NC)"
	@echo "$(MAGENTA)═══════════════════════════════════════════════$(NC)"

######### UTILITIES #########

.PHONY: clean
clean:
	@echo "$(YELLOW)Limpiando directorios...$(NC)"
	@rm -rf $(DOCS_DIR)/* $(GITDIFF_DIR)/*
	@echo "$(GREEN)✓ Limpieza completada$(NC)"

.PHONY: info
info:
	@echo "$(CYAN)Información del Proyecto$(NC)"
	@echo ""
	@echo "$(YELLOW)Branches:$(NC)"
	@echo "  Main (without): $(MAIN_BRANCH)"
	@echo "  Current:        $(CURRENT_BRANCH)"
	@echo ""
	@echo "$(YELLOW)Directorios:$(NC)"
	@echo "  Docs:     $(DOCS_DIR)"
	@echo "  Git Diff: $(GITDIFF_DIR)"
	@echo "  Releases: $(RELEASES_DIR)"
	@echo ""
	@echo "$(YELLOW)Archivos OpenAPI:$(NC)"
	@if [ -f "$(OPENAPI_OLD)" ]; then \
		echo "  ✓ OLD: $$(wc -l < $(OPENAPI_OLD)) líneas"; \
	else \
		echo "  ✗ OLD: no encontrado"; \
	fi
	@if [ -f "$(OPENAPI_NEW)" ]; then \
		echo "  ✓ NEW: $$(wc -l < $(OPENAPI_NEW)) líneas"; \
	else \
		echo "  ✗ NEW: no encontrado"; \
	fi
	@echo ""
	@echo "$(YELLOW)Releases:$(NC)"
	@if [ -d "$(RELEASES_DIR)" ]; then \
		RELEASE_COUNT=$$(ls -1 $(RELEASES_DIR) 2>/dev/null | wc -l); \
		echo "  Total: $$RELEASE_COUNT"; \
		if [ $$RELEASE_COUNT -gt 0 ]; then \
			ls -1 $(RELEASES_DIR) | sed 's/^/    - /'; \
		fi; \
	else \
		echo "  No releases found"; \
	fi
