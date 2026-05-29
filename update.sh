#!/usr/bin/env bash
# update.sh · Actualizador del sistema de plantillas
#
# Uso:
#   ./update.sh              # Detecta y pregunta antes de actualizar
#   ./update.sh --force      # Actualiza sin preguntar
#   ./update.sh --check      # Solo verifica si hay nueva versión

set -euo pipefail

PLANTILLAS_DIR="${PLANTILLAS_DIR:-$HOME/.claude/plantillas}"
REPO_URL="https://github.com/alexendros/plantillas.git"
RELEASE_API="https://api.github.com/repos/alexendros/plantillas/releases/latest"

FORCE=0
CHECK=0

log()   { printf '[update] %s\n' "$*"; }
ok()    { printf '[update] ✅ %s\n' "$*"; }
warn()  { printf '[update] ⚠️  %s\n' "$*"; }
error() { printf '[update] ❌ %s\n' "$*" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)  FORCE=1; shift ;;
    --check)  CHECK=1; shift ;;
    -h|--help)
      echo "Uso: update.sh [--force] [--check]"
      exit 0
      ;;
    *) error "Argumento desconocido: $1" ;;
  esac
done

# ─── Detectar versión actual ───────────────────────────────────────────────
CURRENT_VERSION="unknown"
if [[ -f "$PLANTILLAS_DIR/CHANGELOG.md" ]]; then
  CURRENT_VERSION=$(grep -oP '^## \[\K[^\]]+' "$PLANTILLAS_DIR/CHANGELOG.md" | head -1)
fi
log "Versión actual: $CURRENT_VERSION"

# ─── Detectar versión remota ───────────────────────────────────────────────
LATEST_VERSION=""
if command -v curl >/dev/null 2>&1; then
  LATEST_VERSION=$(curl -fsSL "$RELEASE_API" 2>/dev/null | grep -oP '"tag_name": "\K[^"]+' || echo "")
fi

if [[ -z "$LATEST_VERSION" ]]; then
  warn "No se pudo detectar la última versión remota."
  LATEST_VERSION="unknown"
fi

log "Última versión: $LATEST_VERSION"

if [[ "$CHECK" -eq 1 ]]; then
  if [[ "$CURRENT_VERSION" == "$LATEST_VERSION" ]]; then
    ok "Estás en la última versión."
  else
    warn "Hay una nueva versión disponible: $LATEST_VERSION"
  fi
  exit 0
fi

if [[ "$CURRENT_VERSION" == "$LATEST_VERSION" && "$FORCE" -eq 0 ]]; then
  ok "Ya tienes la última versión. No es necesario actualizar."
  exit 0
fi

# ─── Confirmar ─────────────────────────────────────────────────────────────
if [[ "$FORCE" -eq 0 ]]; then
  warn "Se actualizará de $CURRENT_VERSION → $LATEST_VERSION"
  read -rp "¿Continuar? [y/N] " respuesta
  [[ "$respuesta" =~ ^[Yy]$ ]] || { log "Actualización cancelada."; exit 0; }
fi

# ─── Backup ────────────────────────────────────────────────────────────────
BACKUP_DIR="${PLANTILLAS_DIR}.backup.$(date +%s)"
log "Creando backup en: $BACKUP_DIR"
cp -r "$PLANTILLAS_DIR" "$BACKUP_DIR"

# ─── Actualizar ────────────────────────────────────────────────────────────
log "Descargando nueva versión…"
_TMPROOT=$(mktemp -d)
trap 'rm -rf "$_TMPROOT"' EXIT

git clone --depth 1 --branch "$LATEST_VERSION" "$REPO_URL" "$_TMPROOT/repo" 2>/dev/null || \
  git clone --depth 1 "$REPO_URL" "$_TMPROOT/repo"

rm -rf "$PLANTILLAS_DIR"
mkdir -p "$(dirname "$PLANTILLAS_DIR")"
mv "$_TMPROOT/repo" "$PLANTILLAS_DIR"

ok "Actualización completada: $CURRENT_VERSION → $LATEST_VERSION"
log "Backup disponible en: $BACKUP_DIR"
