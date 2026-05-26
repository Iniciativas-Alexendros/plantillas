#!/usr/bin/env bash
# =====================================================================
# XEK-ENV v3.1 · Bootstrap horizontal para Claude Code on the web
# Sucesor de OMNI-ENV v3.0-FINAL · Autor: Alexendros
# Pega este script en el campo "Script de configuración" del diálogo
# "Actualizar entorno en la nube" (https://claude.ai/code).
#
# Garantías:
#   · idempotente (cache diaria $XEK_STATE/bootstrap-YYYY-MM-DD.stamp)
#   · tolerante a apt offline (no falla si no hay red apt)
#   · <30s en frío, <5s con caché
#   · NO escribe secretos
#
# Tiers (toggleables vía env vars del propio diálogo):
#   CORE    fd, bat, eza, delta, zoxide, sops, zstd, rsync, sqlite3, httpie
#   PY      ipython + polars/pandas/numpy/httpx/pydantic/rich/typer/...
#   SHELL   zsh + starship + atuin + zinit + plugins + rcfiles
#   AI      huggingface_hub + llm + duckdb
#   OFFICE  ffmpeg + imagemagick + webp
#   LEGAL   pandoc + poppler-utils + qpdf + tesseract-ocr-spa
#   WEB     corepack/pnpm (Node 22 ya viene en la imagen)
# =====================================================================
set -Eeuo pipefail
trap 'echo "[XEK] bootstrap interrumpido en línea $LINENO" >&2' ERR

# ---------- 0. Logging y dirs ----------
mkdir -p "$XEK_CACHE" "$XEK_STATE" "$XEK_SECRETS_DIR" "$XEK_REPOS_HOME" \
         "$HOME/.config/starship" "$HOME/.local/bin" \
         "$HOME/.ipython/profile_default"
exec > >(tee -a "$XEK_LOG") 2>&1
START=$(date +%s)
echo "──────────── XEK-ENV v3.1 · $(date -Is) ────────────"

# ---------- 1. Locale + TZ ----------
sudo -n ln -sf "/usr/share/zoneinfo/$TZ" /etc/localtime 2>/dev/null || true
if ! locale -a 2>/dev/null | grep -qi 'es_ES.utf8'; then
  echo "es_ES.UTF-8 UTF-8" | sudo -n tee -a /etc/locale.gen >/dev/null 2>&1 || true
  sudo -n locale-gen >/dev/null 2>&1 || true
fi

# ---------- 2. PATH ----------
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$HOME/.bun/bin:/opt/node22/bin:/usr/local/go/bin:$PATH"

# ---------- 3. Cache diaria ----------
STAMP="$XEK_STATE/bootstrap-$(date +%Y-%m-%d).stamp"
if [ -f "$STAMP" ]; then echo "[XEK] cache diaria activa · skip installs"; SKIP=1; else SKIP=0; fi

install_apt() {
  DEBIAN_FRONTEND=noninteractive sudo -n apt-get update -qq 2>/dev/null || true
  sudo -n apt-get install -y -qq --no-install-recommends "$@" 2>&1 | tail -2 || true
}

# ---------- 4. Tier CORE ----------
if [ "${XEK_TIER_CORE:-1}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] capa CORE"
  install_apt fd-find bat eza zoxide git-delta \
              zstd rsync openssh-client dnsutils \
              httpie sqlite3 sops jpegoptim direnv
  [ -x /usr/bin/fdfind ] && ln -sf /usr/bin/fdfind  "$HOME/.local/bin/fd"
  [ -x /usr/bin/batcat ] && ln -sf /usr/bin/batcat  "$HOME/.local/bin/bat"
fi

# ---------- 5. Tier SHELL (zsh + starship + atuin + plugins) ----------
if [ "${XEK_TIER_SHELL:-1}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] tier SHELL (zsh + starship + atuin + zinit)"
  install_apt zsh
  command -v starship >/dev/null || \
    curl -fsSL https://starship.rs/install.sh | sh -s -- -y -b "$HOME/.local/bin" >/dev/null 2>&1 || true
  command -v atuin >/dev/null || \
    curl -fsSL https://setup.atuin.sh | sh >/dev/null 2>&1 || true
  ZI="$HOME/.local/share/zinit/zinit.git"
  [ ! -d "$ZI" ] && git clone --depth 1 https://github.com/zdharma-continuum/zinit.git "$ZI" >/dev/null 2>&1 || true
  # rcfiles desde plantillas (sólo si faltan)
  [ ! -f "$HOME/.bashrc.d/xek.sh" ] && mkdir -p "$HOME/.bashrc.d" && \
    cp -n "$XEK_PLANTILLAS/dot-claude/ejemplo_dot_claude/rc/xek-bash.sh" "$HOME/.bashrc.d/xek.sh" 2>/dev/null || true
  grep -q 'bashrc.d/xek.sh' "$HOME/.bashrc" 2>/dev/null || \
    echo '[ -f "$HOME/.bashrc.d/xek.sh" ] && source "$HOME/.bashrc.d/xek.sh"' >> "$HOME/.bashrc"
  [ ! -f "$HOME/.zshrc" ] && \
    cp -n "$XEK_PLANTILLAS/dot-claude/ejemplo_dot_claude/rc/xek-zsh.zsh" "$HOME/.zshrc" 2>/dev/null || true
  [ ! -f "$HOME/.config/starship.toml" ] && \
    cp -n "$XEK_PLANTILLAS/dot-claude/ejemplo_dot_claude/rc/starship.toml" "$HOME/.config/starship.toml" 2>/dev/null || true
fi

# ---------- 6. Tier PY (ipython + librerías potentes) ----------
if [ "${XEK_TIER_PY:-1}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] tier PY (ipython + polars/pandas/numpy/httpx/pydantic/...)"
  uv tool install --quiet ipython \
    --with polars --with pandas --with numpy \
    --with httpx --with requests \
    --with pydantic --with typer --with rich \
    --with pyyaml --with python-dotenv \
    --with beautifulsoup4 --with sqlmodel \
    --with tabulate --with msgspec 2>/dev/null || true
  uv tool install --quiet jupyterlab 2>/dev/null || true
  IPY="$HOME/.ipython/profile_default/ipython_config.py"
  [ ! -f "$IPY" ] && \
    cp -n "$XEK_PLANTILLAS/dot-claude/ejemplo_dot_claude/rc/ipython_config.py" "$IPY" 2>/dev/null || true
fi

# ---------- 7. Tier AI ----------
if [ "${XEK_TIER_AI:-1}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] tier AI (huggingface_hub + llm + duckdb)"
  uv tool install --quiet huggingface_hub llm duckdb 2>/dev/null || true
fi

# ---------- 8. Tier OFFICE ----------
if [ "${XEK_TIER_OFFICE:-1}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] tier OFFICE (ffmpeg + imagemagick + webp)"
  install_apt ffmpeg imagemagick webp
fi

# ---------- 9. Tier LEGAL ----------
if [ "${XEK_TIER_LEGAL:-0}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] tier LEGAL (pandoc + pdf + ocr-spa)"
  install_apt pandoc poppler-utils qpdf tesseract-ocr tesseract-ocr-spa
fi

# ---------- 10. uv tool global (pipx-style) ----------
if [ "$SKIP" = 0 ]; then
  echo "[XEK] uv tool · pre-commit, yamllint, csvkit, commitizen"
  uv tool install --quiet pre-commit yamllint csvkit commitizen 2>/dev/null || true
fi

# ---------- 11. Tier WEB (corepack/pnpm) ----------
[ "${XEK_TIER_WEB:-1}" = 1 ] && corepack enable >/dev/null 2>&1 || true

# ---------- 12. Pre-stage ~/.claude/ ----------
if [ -d "$XEK_PLANTILLAS/dot-claude/ejemplo_dot_claude" ] && [ ! -e "$HOME/.claude/mcp.json" ]; then
  mkdir -p "$HOME/.claude"
  cp -nR "$XEK_PLANTILLAS/dot-claude/ejemplo_dot_claude/." "$HOME/.claude/"
  echo "[XEK] ~/.claude/ pre-staged desde dot-claude/ejemplo_dot_claude/"
fi

# ---------- 13. Git defaults ----------
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global push.autoSetupRemote true
git config --global rerere.enabled true
git config --global core.pager 'cat'
git config --global user.name "$AUTHOR"

# ---------- 14. Doors (puertas cifradas) ----------
chmod 700 "$XEK_SECRETS_DIR" 2>/dev/null || true
[ ! -f "$SOPS_AGE_KEY_FILE" ] && echo "[XEK] info · sin clave age (sops deshabilitado)"

# ---------- 15. Banner ----------
echo "$(date -Is)" > "$STAMP"
END=$(date +%s)
cat <<BANNER
╔════════════════════════════════════════════════════╗
║ XEK-ENV v3.1 listo en $((END-START))s
║ host:        $(hostname)  ·  user: $(whoami)
║ plantillas:  $XEK_PLANTILLAS
║ repos:       $XEK_REPOS_HOME
║ lang:        $XEK_LANG · TZ=$TZ
║ tiers on:    core=$XEK_TIER_CORE py=$XEK_TIER_PY shell=$XEK_TIER_SHELL ai=$XEK_TIER_AI office=$XEK_TIER_OFFICE legal=$XEK_TIER_LEGAL web=$XEK_TIER_WEB
║ log:         $XEK_LOG
╚════════════════════════════════════════════════════╝
BANNER
