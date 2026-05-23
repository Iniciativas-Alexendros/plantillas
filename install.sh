#!/usr/bin/env bash
# install.sh · Instalador del sistema de plantillas modulares para Claude Code
#
# Uso:
#   curl -fsSL https://raw.githubusercontent.com/alexendros/plantillas/main/install.sh | bash
#   ./install.sh --prefix ~/.claude/plantillas
#   ./install.sh --prefix ./plantillas --version v1.0.0
#
# Características:
#   - Idempotente: puede ejecutarse varias veces sin duplicar.
#   - Verifica dependencias (git, python3).
#   - Descarga release o clona repo según disponibilidad.
#   - Crea symlink en ~/.local/bin/claude-init si se pide.

set -euo pipefail

SCRIPT_URL="https://raw.githubusercontent.com/alexendros/plantillas/main/install.sh"
REPO_URL="https://github.com/alexendros/plantillas.git"
RELEASE_API="https://api.github.com/repos/alexendros/plantillas/releases/latest"

PREFIX="${HOME}/.claude/plantillas"
VERSION=""
DRY_RUN=0
CREATE_SYMLINK=0
FORCE=0

# ─── Colores ───────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()   { printf "${BLUE}[install]${NC} %s\n" "$*"; }
ok()    { printf "${GREEN}[install]${NC} %s\n" "$*"; }
warn()  { printf "${YELLOW}[install]${NC} %s\n" "$*"; }
error() { printf "${RED}[install]${NC} %s\n" "$*" >&2; exit 1; }

# ─── Args ──────────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --prefix)      PREFIX="$2"; shift 2 ;;
    --version)     VERSION="$2"; shift 2 ;;
    --dry-run)     DRY_RUN=1; shift ;;
    --symlink)     CREATE_SYMLINK=1; shift ;;
    --force)       FORCE=1; shift ;;
    -h|--help)
      cat << 'HELP'
Uso: install.sh [OPCIONES]

Opciones:
  --prefix <dir>     Directorio de instalación (default: ~/.claude/plantillas)
  --version <tag>    Versión específica a instalar (ej: v1.0.0)
  --dry-run          Muestra qué haría sin ejecutar
  --symlink          Crea symlink ~/.local/bin/claude-init
  --force            Sobrescribe instalación existente
  -h, --help         Muestra esta ayuda
HELP
      exit 0
      ;;
    *) error "Argumento desconocido: $1" ;;
  esac
done

# ─── Dependencias ──────────────────────────────────────────────────────────
log "Verificando dependencias…"

command -v git >/dev/null 2>&1 || error "git no está instalado. Instálalo e inténtalo de nuevo."
command -v python3 >/dev/null 2>&1 || warn "python3 no encontrado. Los validadores no funcionarán."

# ─── Preparar destino ──────────────────────────────────────────────────────
if [[ -d "$PREFIX" && "$FORCE" -eq 0 ]]; then
  warn "El directorio ya existe: $PREFIX"
  read -rp "¿Sobrescribir? [y/N] " respuesta
  [[ "$respuesta" =~ ^[Yy]$ ]] || { log "Instalación cancelada."; exit 0; }
fi

if [[ "$DRY_RUN" -eq 1 ]]; then
  log "DRY-RUN · Simulando instalación en: $PREFIX"
fi

# ─── Instalación ───────────────────────────────────────────────────────────
if [[ "$DRY_RUN" -eq 1 ]]; then
  log "DRY-RUN · Descargaría plantillas en: $PREFIX"
else
  # Crear directorio temporal
  TMPDIR=$(mktemp -d)
  trap 'rm -rf "$TMPDIR"' EXIT

  if [[ -n "$VERSION" ]]; then
    log "Descargando release $VERSION…"
    curl -fsSL "${REPO_URL%.git}/archive/refs/tags/${VERSION}.tar.gz" | tar -xz -C "$TMPDIR" --strip-components=1
  else
    log "Clonando repositorio…"
    git clone --depth 1 "$REPO_URL" "$TMPDIR/repo"
    TMPDIR="$TMPDIR/repo"
  fi

  # Limpiar destino si existe y copiar
  [[ -d "$PREFIX" ]] && rm -rf "$PREFIX"
  mkdir -p "$(dirname "$PREFIX")"
  mv "$TMPDIR" "$PREFIX"

  ok "Plantillas instaladas en: $PREFIX"
fi

# ─── Symlink ───────────────────────────────────────────────────────────────
if [[ "$CREATE_SYMLINK" -eq 1 ]]; then
  BIN_DIR="${HOME}/.local/bin"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    log "DRY-RUN · Crearía symlink: ${BIN_DIR}/claude-init → ${PREFIX}/claude-init"
  else
    mkdir -p "$BIN_DIR"
    ln -sf "${PREFIX}/claude-init" "${BIN_DIR}/claude-init"
    ok "Symlink creado: ${BIN_DIR}/claude-init"
    if [[ ":$PATH:" != *":${BIN_DIR}:"* ]]; then
      warn "Añade ${BIN_DIR} a tu PATH:"
      echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
  fi
fi

# ─── Post-instalación ──────────────────────────────────────────────────────
if [[ "$DRY_RUN" -eq 0 ]]; then
  ok "Instalación completada."
  echo
  echo "Próximos pasos:"
  echo "  1. Explora el índice:   cat ${PREFIX}/INDEX.md"
  echo "  2. Valida un ejemplo:   python ${PREFIX}/agentes/validar_agente.py ${PREFIX}/agentes/ejemplo_agente.md --strict"
  echo "  3. Inicializa un módulo: ${PREFIX}/claude-init"
  echo
  echo "Para actualizar en el futuro:"
  echo "  ${PREFIX}/update.sh"
fi
