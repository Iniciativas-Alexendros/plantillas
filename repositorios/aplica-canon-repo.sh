#!/usr/bin/env bash
# aplica-canon-repo.sh · aplica plantillas canon a un repo local.
#
# Uso:
#   aplica-canon-repo.sh --repo <slug> [--path <ruta>] [--dry-run] [--force <archivo>] [--profile <perfil>]
#
# Reglas:
#   - Idempotente. NO sobrescribe archivos existentes salvo --force <archivo>.
#   - Respeta cabecera `<!-- canon-managed: false -->` y archivo `.canon-skip`.
#   - Lee la fuente de verdad en repos.yaml.
#   - Sustituye placeholders {{REPO_NAME}}, {{REPO_OWNER}}, {{LICENSE_SPDX}},
#     {{YEAR}}, {{DESCRIPTION}}, {{HOMEPAGE}}, {{CONTACT_EMAIL}},
#     {{SECURITY_EMAIL}}, {{PGP_FINGERPRINT}}, {{COPYRIGHT_HOLDER}}, {{NEXT_YEAR}}.

set -euo pipefail

PLANTILLAS_DIR="${PLANTILLAS_DIR:-$HOME/.claude/herramientas/plantillas/repos}"
REPOS_YAML="${REPOS_YAML:-$PLANTILLAS_DIR/repos.yaml}"

DRY_RUN=0
FORCE_FILE=""
REPO_SLUG=""
REPO_PATH=""
PROFILE_OVERRIDE=""

usage() {
  sed -n '2,11p' "$0"
  exit 0
}

log()   { printf '[canon] %s\n' "$*" >&2; }
warn()  { printf '[canon][warn] %s\n' "$*" >&2; }
error() { printf '[canon][error] %s\n' "$*" >&2; exit 1; }

# --- yq detection -----------------------------------------------------------
if command -v yq >/dev/null 2>&1; then
  YQ="yq"
elif command -v python3 >/dev/null 2>&1; then
  YQ=""  # se usará helper python
else
  error "Necesario yq o python3 disponibles para parsear repos.yaml"
fi

yaml_get() {
  # $1 = expresión yq · $2 = archivo
  if [[ -n "$YQ" ]]; then
    yq -r "$1" "$2"
  else
    python3 - "$2" "$1" <<'PY'
import sys, yaml, re
path, expr = sys.argv[1], sys.argv[2]
data = yaml.safe_load(open(path))
expr = expr.strip().lstrip('.')
parts = re.findall(r'[^.\[\]]+|\[[^\]]+\]', expr)
cur = data
for p in parts:
    if p.startswith('['):
        idx = p[1:-1].strip('"\'')
        cur = cur[idx] if isinstance(cur, dict) else cur[int(idx)]
    else:
        cur = cur.get(p) if isinstance(cur, dict) else None
    if cur is None:
        print('null'); sys.exit(0)
print(cur if not isinstance(cur, (dict, list)) else yaml.safe_dump(cur).strip())
PY
  fi
}

# --- args -------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)    REPO_SLUG="$2"; shift 2 ;;
    --path)    REPO_PATH="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --force)   FORCE_FILE="$2"; shift 2 ;;
    --profile) PROFILE_OVERRIDE="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) error "Argumento desconocido: $1" ;;
  esac
done

[[ -z "$REPO_SLUG" ]] && error "Falta --repo <slug>"
[[ -f "$REPOS_YAML" ]] || error "No se encuentra $REPOS_YAML"

# --- resolución de metadatos -----------------------------------------------
PROFILE="${PROFILE_OVERRIDE:-$(yaml_get ".repos.${REPO_SLUG}.profile" "$REPOS_YAML")}"
LICENSE_SPDX="$(yaml_get ".repos.${REPO_SLUG}.license" "$REPOS_YAML")"
VISIBILITY="$(yaml_get ".repos.${REPO_SLUG}.visibility" "$REPOS_YAML")"
DESCRIPTION="$(yaml_get ".repos.${REPO_SLUG}.description" "$REPOS_YAML")"
HOMEPAGE="$(yaml_get ".repos.${REPO_SLUG}.homepage" "$REPOS_YAML")"
OWNER="$(yaml_get ".repos.${REPO_SLUG}.owner" "$REPOS_YAML")"
ARCHIVED="$(yaml_get ".repos.${REPO_SLUG}.archived" "$REPOS_YAML")"

CONTACT_EMAIL="$(yaml_get '.defaults.contact_email' "$REPOS_YAML")"
SECURITY_EMAIL="$(yaml_get '.defaults.security_email' "$REPOS_YAML")"
PGP_FINGERPRINT="$(yaml_get '.defaults.pgp_fingerprint' "$REPOS_YAML")"
COPYRIGHT_HOLDER="$(yaml_get '.defaults.copyright_holder' "$REPOS_YAML")"
YEAR="$(yaml_get '.defaults.year' "$REPOS_YAML")"
NEXT_YEAR="$(yaml_get '.defaults.next_year' "$REPOS_YAML")"

[[ "$PROFILE" == "null" || -z "$PROFILE" ]] && error "Perfil no resuelto para $REPO_SLUG"
[[ "$ARCHIVED" == "true" && "${ALLOW_ARCHIVED:-0}" != "1" ]] && error "Repo $REPO_SLUG archivado · usa ALLOW_ARCHIVED=1 para forzar"

[[ -z "$REPO_PATH" ]] && REPO_PATH="$(pwd)"
[[ -d "$REPO_PATH" ]] || error "Ruta no existe: $REPO_PATH"

log "Repo: $REPO_SLUG · perfil: $PROFILE · licencia: $LICENSE_SPDX · path: $REPO_PATH · dry-run=$DRY_RUN"

# --- helper: render template -----------------------------------------------
render() {
  local src="$1" dst="$2"
  local tmp; tmp="$(mktemp)"
  sed \
    -e "s|{{REPO_NAME}}|${REPO_SLUG}|g" \
    -e "s|{{REPO_OWNER}}|${OWNER}|g" \
    -e "s|{{LICENSE_SPDX}}|${LICENSE_SPDX}|g" \
    -e "s|{{YEAR}}|${YEAR}|g" \
    -e "s|{{NEXT_YEAR}}|${NEXT_YEAR}|g" \
    -e "s|{{DESCRIPTION}}|${DESCRIPTION}|g" \
    -e "s|{{HOMEPAGE}}|${HOMEPAGE}|g" \
    -e "s|{{CONTACT_EMAIL}}|${CONTACT_EMAIL}|g" \
    -e "s|{{SECURITY_EMAIL}}|${SECURITY_EMAIL}|g" \
    -e "s|{{PGP_FINGERPRINT}}|${PGP_FINGERPRINT}|g" \
    -e "s|{{COPYRIGHT_HOLDER}}|${COPYRIGHT_HOLDER}|g" \
    "$src" > "$tmp"
  if [[ $DRY_RUN -eq 1 ]]; then
    log "DRY-RUN · escribiría $dst (origen: $src)"
    diff -u "$dst" "$tmp" 2>/dev/null || true
    rm -f "$tmp"
  else
    mkdir -p "$(dirname "$dst")"
    mv "$tmp" "$dst"
    log "  + $dst"
  fi
}

# --- helper: apply if missing/forced ---------------------------------------
apply_if_missing() {
  local relpath="$1" src="$2"
  local dst="$REPO_PATH/$relpath"

  if [[ ! -f "$src" ]]; then
    warn "Plantilla origen no existe: $src"
    return
  fi

  # canon-managed: false en archivo destino
  if [[ -f "$dst" ]] && grep -q "canon-managed: false" "$dst" 2>/dev/null; then
    log "  · SKIP (canon-managed: false): $relpath"
    return
  fi

  # .canon-skip
  if [[ -f "$REPO_PATH/.canon-skip" ]] && grep -qx "$relpath" "$REPO_PATH/.canon-skip" 2>/dev/null; then
    log "  · SKIP (.canon-skip): $relpath"
    return
  fi

  # ¿forzar este archivo?
  if [[ "$FORCE_FILE" == "$relpath" ]]; then
    render "$src" "$dst"
    return
  fi

  # ¿existe ya?
  if [[ -f "$dst" ]]; then
    log "  · existe (NO sobrescribe): $relpath"
    return
  fi

  render "$src" "$dst"
}

# --- helper: archivo binario común (LICENSE, .editorconfig, .gitattributes) ---
apply_static() {
  local relpath="$1" src="$2"
  local dst="$REPO_PATH/$relpath"
  if [[ ! -f "$src" ]]; then
    warn "Plantilla origen no existe: $src"
    return
  fi
  if [[ -f "$dst" && "$FORCE_FILE" != "$relpath" ]]; then
    log "  · existe (NO sobrescribe): $relpath"
    return
  fi
  if [[ $DRY_RUN -eq 1 ]]; then
    log "DRY-RUN · escribiría $dst desde $src"
  else
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
    log "  + $dst"
  fi
}

# ============================================================================
# Aplicación
# ============================================================================

log "→ Aplicando archivos comunes…"

apply_if_missing "CHANGELOG.md"             "$PLANTILLAS_DIR/comun/CHANGELOG.md.tmpl"
apply_if_missing "CONTRIBUTING.md"          "$PLANTILLAS_DIR/comun/CONTRIBUTING.md.tmpl"
apply_if_missing "CODE_OF_CONDUCT.md"       "$PLANTILLAS_DIR/comun/CODE_OF_CONDUCT.md.tmpl"
apply_if_missing "SECURITY.md"              "$PLANTILLAS_DIR/comun/SECURITY.md.tmpl"
apply_if_missing "AUTHORS.md"               "$PLANTILLAS_DIR/comun/AUTHORS.md.tmpl"
apply_if_missing "SUPPORT.md"               "$PLANTILLAS_DIR/comun/SUPPORT.md.tmpl"
apply_if_missing "MAINTAINERS.md"           "$PLANTILLAS_DIR/comun/MAINTAINERS.md.tmpl"
apply_if_missing "RELEASE.md"               "$PLANTILLAS_DIR/comun/RELEASE.md.tmpl"
apply_if_missing "ROADMAP.md"               "$PLANTILLAS_DIR/comun/ROADMAP.md.tmpl"
apply_if_missing ".github/PULL_REQUEST_TEMPLATE.md" "$PLANTILLAS_DIR/comun/PULL_REQUEST_TEMPLATE.md.tmpl"
apply_if_missing ".github/CODEOWNERS"       "$PLANTILLAS_DIR/comun/CODEOWNERS.tmpl"
apply_static    ".editorconfig"             "$PLANTILLAS_DIR/comun/.editorconfig"
apply_static    ".gitattributes"            "$PLANTILLAS_DIR/comun/.gitattributes"

if [[ "$VISIBILITY" == "public" ]]; then
  apply_if_missing ".github/FUNDING.yml"                  "$PLANTILLAS_DIR/comun/FUNDING.yml.tmpl"
  apply_if_missing ".github/ISSUE_TEMPLATE/bug.yml"       "$PLANTILLAS_DIR/comun/issue-templates/bug.yml.tmpl"
  apply_if_missing ".github/ISSUE_TEMPLATE/feature.yml"   "$PLANTILLAS_DIR/comun/issue-templates/feature.yml.tmpl"
  apply_if_missing ".github/ISSUE_TEMPLATE/question.yml"  "$PLANTILLAS_DIR/comun/issue-templates/question.yml.tmpl"
  apply_if_missing ".github/ISSUE_TEMPLATE/security.yml"  "$PLANTILLAS_DIR/comun/issue-templates/security.yml.tmpl"
  apply_if_missing ".github/ISSUE_TEMPLATE/config.yml"    "$PLANTILLAS_DIR/comun/issue-templates/config.yml.tmpl"
fi

apply_if_missing "docs/adr/0001-template.md" "$PLANTILLAS_DIR/comun/adr/0001-template.md.tmpl"
apply_if_missing "docs/README.md"            "$PLANTILLAS_DIR/comun/docs-index.md.tmpl"

log "→ Aplicando licencia ($LICENSE_SPDX)…"

case "$LICENSE_SPDX" in
  MIT|Apache-2.0|AGPL-3.0|CC-BY-4.0)
    LICENSE_SRC="$PLANTILLAS_DIR/licencias/${LICENSE_SPDX}.txt"
    LICENSE_TMP="$(mktemp)"
    sed \
      -e "s|{{YEAR}}|${YEAR}|g" \
      -e "s|{{COPYRIGHT_HOLDER}}|${COPYRIGHT_HOLDER}|g" \
      "$LICENSE_SRC" > "$LICENSE_TMP"
    if [[ -f "$REPO_PATH/LICENSE" && "$FORCE_FILE" != "LICENSE" ]]; then
      log "  · LICENSE existe (NO sobrescribe)"
    elif [[ $DRY_RUN -eq 1 ]]; then
      log "DRY-RUN · escribiría LICENSE"
    else
      mv "$LICENSE_TMP" "$REPO_PATH/LICENSE"
      log "  + LICENSE"
    fi
    rm -f "$LICENSE_TMP"
    ;;
  PROPRIETARY)
    COPYRIGHT_TMP="$(mktemp)"
    sed \
      -e "s|{{YEAR}}|${YEAR}|g" \
      -e "s|{{COPYRIGHT_HOLDER}}|${COPYRIGHT_HOLDER}|g" \
      -e "s|{{CONTACT_EMAIL}}|${CONTACT_EMAIL}|g" \
      "$PLANTILLAS_DIR/licencias/PROPRIETARY.txt" > "$COPYRIGHT_TMP"
    if [[ -f "$REPO_PATH/COPYRIGHT.md" && "$FORCE_FILE" != "COPYRIGHT.md" ]]; then
      log "  · COPYRIGHT.md existe (NO sobrescribe)"
    elif [[ $DRY_RUN -eq 1 ]]; then
      log "DRY-RUN · escribiría COPYRIGHT.md"
    else
      mv "$COPYRIGHT_TMP" "$REPO_PATH/COPYRIGHT.md"
      log "  + COPYRIGHT.md"
    fi
    rm -f "$COPYRIGHT_TMP"
    ;;
  *)
    warn "Licencia desconocida: $LICENSE_SPDX"
    ;;
esac

log "→ Aplicando perfil ($PROFILE)…"

PROFILE_DIR="$PLANTILLAS_DIR/$PROFILE"
[[ -d "$PROFILE_DIR" ]] || error "Perfil sin plantillas: $PROFILE_DIR"

[[ -f "$PROFILE_DIR/README.md.tmpl" ]]      && apply_if_missing "README.md"       "$PROFILE_DIR/README.md.tmpl"
[[ -f "$PROFILE_DIR/ARCHITECTURE.md.tmpl" ]] && apply_if_missing "ARCHITECTURE.md" "$PROFILE_DIR/ARCHITECTURE.md.tmpl"
[[ -f "$PROFILE_DIR/DESIGN.md.tmpl" ]]      && apply_if_missing "DESIGN.md"       "$PROFILE_DIR/DESIGN.md.tmpl"
[[ -f "$PROFILE_DIR/STYLEGUIDE.md.tmpl" ]]  && apply_if_missing "STYLEGUIDE.md"   "$PROFILE_DIR/STYLEGUIDE.md.tmpl"
[[ -f "$PROFILE_DIR/ci.yml.tmpl" ]]         && apply_if_missing ".github/workflows/ci.yml" "$PROFILE_DIR/ci.yml.tmpl"
[[ -f "$PROFILE_DIR/dependabot.yml.tmpl" ]] && apply_if_missing ".github/dependabot.yml" "$PROFILE_DIR/dependabot.yml.tmpl"
[[ -f "$PROFILE_DIR/.gitignore.tmpl" ]]     && apply_if_missing ".gitignore"      "$PROFILE_DIR/.gitignore.tmpl"
[[ -f "$PROFILE_DIR/security.txt.tmpl" && "$VISIBILITY" == "public" ]] && \
  apply_if_missing "public/.well-known/security.txt" "$PROFILE_DIR/security.txt.tmpl"

log "Listo."
