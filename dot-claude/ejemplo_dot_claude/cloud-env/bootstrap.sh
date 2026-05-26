#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════
# XEK-ENV v3.3 · bootstrap horizontal · Claude Code on the web
# Autor: Alexendros · Sucesor de OMNI-ENV v3.0-FINAL · Bun-first
# ══════════════════════════════════════════════════════════════════════
# Pega este script en el campo "Script de configuración" del diálogo
# "Actualizar entorno en la nube" (https://claude.ai/code).
#
# Garantías:
#   · idempotente (cache diaria $XEK_STATE/bootstrap-YYYY-MM-DD.stamp)
#   · apt-get update deduplicado por día (APT_STAMP)
#   · tolerante a red parcial (todos los pasos terminan en `|| true`)
#   · NO escribe secretos
#   · frío 30–60s (general) · 60–120s (todos los tiers) · <5s caliente
#
# Tiers (toggleables vía XEK_TIER_* en env vars del diálogo):
#   CORE      fd, bat, eza, delta, zoxide, sops, zstd, rsync, sqlite3,
#             httpie, direnv, jq, yq, bc + bun upgrade --stable
#   RUNTIMES  mise + node@$NODE_VERSION (default 24) + python@$PYTHON_VERSION
#   PY        ipython + polars/pandas/numpy/httpx/pydantic/rich/typer/...
#   SHELL     zsh + starship + atuin + zinit + plugins + rcfiles
#   AI        huggingface_hub + llm + duckdb
#   OFFICE    ffmpeg + imagemagick + webp
#   NET       mtr + iperf3 + nmap + tcpdump + mosh + tmux + rclone + ...
#   DOCKER    docker-compose-plugin + buildx + buildah + skopeo +
#             lazydocker + dive + ctop + hadolint + trivy
#   LEGAL     pandoc + poppler-utils + qpdf + tesseract-ocr-spa
#   WEB       corepack + pnpm@latest + yarn@stable (Bun ya viene de CORE)
# ══════════════════════════════════════════════════════════════════════
set -Eeuo pipefail
trap 'echo "[XEK] error en línea $LINENO" >&2' ERR

# ─── 0 · Dirs y logging ───────────────────────────────────────────────
mkdir -p "$XEK_CACHE" "$XEK_STATE" "$XEK_SECRETS_DIR" "$XEK_REPOS_HOME" \
         "$HOME/.config/mise" "$HOME/.config/starship" \
         "$HOME/.local/bin"   "$HOME/.ipython/profile_default"
exec > >(tee -a "$XEK_LOG") 2>&1
T0=$(date +%s)
echo "──── XEK-ENV v3.3 · $(date -Is) · env=${XEK_ENV_NAME:-general} ────"

# ─── 1 · Locale + TZ ──────────────────────────────────────────────────
sudo -n ln -sf "/usr/share/zoneinfo/$TZ" /etc/localtime 2>/dev/null || true
if ! locale -a 2>/dev/null | grep -qi 'es_ES.utf8'; then
  echo "es_ES.UTF-8 UTF-8" | sudo -n tee -a /etc/locale.gen >/dev/null 2>&1 || true
  sudo -n locale-gen >/dev/null 2>&1 || true
fi

# ─── 2 · PATH (mise → local → cargo → bun → node22 → sys → go) ────────
export PATH="$HOME/.local/share/mise/shims:$HOME/.local/bin:$HOME/.cargo/bin:$HOME/.bun/bin:/opt/node22/bin:/usr/local/go/bin:$PATH"

# ─── 3 · Cache diaria + helpers apt ───────────────────────────────────
STAMP="$XEK_STATE/bootstrap-$(date +%Y-%m-%d).stamp"
APT_STAMP="$XEK_STATE/apt-updated-$(date +%Y-%m-%d).stamp"
SKIP=0; [ -f "$STAMP" ] && { echo "[XEK] cache diaria · skip installs"; SKIP=1; }

apt_update_once() {
  [ -f "$APT_STAMP" ] && return 0
  DEBIAN_FRONTEND=noninteractive sudo -n apt-get update -qq 2>/dev/null || true
  touch "$APT_STAMP"
}
install_apt() {
  apt_update_once
  sudo -n apt-get install -y -qq --no-install-recommends "$@" 2>&1 | tail -2 || true
}

# ─── 4 · Tier CORE ────────────────────────────────────────────────────
if [ "${XEK_TIER_CORE:-1}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] · CORE"
  install_apt fd-find bat eza zoxide git-delta zstd rsync openssh-client \
              dnsutils httpie sqlite3 sops jpegoptim direnv jq yq bc
  [ -x /usr/bin/fdfind ] && ln -sf /usr/bin/fdfind "$HOME/.local/bin/fd"
  [ -x /usr/bin/batcat ] && ln -sf /usr/bin/batcat "$HOME/.local/bin/bat"
  [ "${BUN_AUTO_UPGRADE:-1}" = 1 ] && command -v bun >/dev/null && \
    bun upgrade --stable >/dev/null 2>&1 || true
fi

# ─── 5 · Tier RUNTIMES (mise · node@$NODE_VERSION · python@$PYTHON_VERSION) ──
if [ "${XEK_TIER_RUNTIMES:-1}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] · RUNTIMES (node@${NODE_VERSION:-24} python@${PYTHON_VERSION:-3.13})"
  command -v mise >/dev/null || \
    curl -fsSL https://mise.run | sh >/dev/null 2>&1 || true
  if command -v mise >/dev/null; then
    mise use --global --quiet "node@${NODE_VERSION:-24}"   2>/dev/null || true
    [ -n "${PYTHON_VERSION:-}" ] && \
      mise use --global --quiet "python@${PYTHON_VERSION}" 2>/dev/null || true
    eval "$(mise activate bash --shims 2>/dev/null)"        2>/dev/null || true
  fi
fi

# ─── 6 · Tier PY (ipython + librerías potentes) ───────────────────────
if [ "${XEK_TIER_PY:-1}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] · PY"
  uv tool install --quiet ipython \
    --with polars         --with pandas     --with numpy \
    --with httpx          --with requests \
    --with pydantic       --with typer      --with rich \
    --with pyyaml         --with python-dotenv \
    --with beautifulsoup4 --with sqlmodel \
    --with tabulate       --with msgspec    2>/dev/null || true
  uv tool install --quiet jupyterlab        2>/dev/null || true
  IPY="$HOME/.ipython/profile_default/ipython_config.py"
  RC="$XEK_PLANTILLAS/dot-claude/ejemplo_dot_claude/rc"
  [ ! -f "$IPY" ] && [ -f "$RC/ipython_config.py" ] && \
    cp -n "$RC/ipython_config.py" "$IPY" 2>/dev/null || true
fi

# ─── 7 · Tier SHELL (zsh + starship + atuin + zinit + rcfiles) ────────
if [ "${XEK_TIER_SHELL:-1}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] · SHELL"
  install_apt zsh
  command -v starship >/dev/null || \
    curl -fsSL https://starship.rs/install.sh | sh -s -- -y -b "$HOME/.local/bin" >/dev/null 2>&1 || true
  command -v atuin >/dev/null || \
    curl -fsSL https://setup.atuin.sh | sh >/dev/null 2>&1 || true
  ZI="$HOME/.local/share/zinit/zinit.git"
  [ ! -d "$ZI" ] && \
    git clone --depth 1 https://github.com/zdharma-continuum/zinit.git "$ZI" >/dev/null 2>&1 || true
  RC="$XEK_PLANTILLAS/dot-claude/ejemplo_dot_claude/rc"
  if [ -d "$RC" ]; then
    mkdir -p "$HOME/.bashrc.d" "$HOME/.config"
    [ ! -f "$HOME/.bashrc.d/xek.sh" ]       && cp -n "$RC/xek-bash.sh"    "$HOME/.bashrc.d/xek.sh"      2>/dev/null || true
    [ ! -f "$HOME/.zshrc" ]                  && cp -n "$RC/xek-zsh.zsh"    "$HOME/.zshrc"                2>/dev/null || true
    [ ! -f "$HOME/.config/starship.toml" ]   && cp -n "$RC/starship.toml"  "$HOME/.config/starship.toml" 2>/dev/null || true
    grep -q 'bashrc.d/xek.sh' "$HOME/.bashrc" 2>/dev/null || \
      echo '[ -f "$HOME/.bashrc.d/xek.sh" ] && source "$HOME/.bashrc.d/xek.sh"' >> "$HOME/.bashrc"
  fi
fi

# ─── 8 · Tier AI (huggingface_hub + llm + duckdb) ─────────────────────
if [ "${XEK_TIER_AI:-0}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] · AI"
  uv tool install --quiet huggingface_hub llm duckdb 2>/dev/null || true
fi

# ─── 9 · Tier OFFICE (ffmpeg + imagemagick + webp) ────────────────────
if [ "${XEK_TIER_OFFICE:-0}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] · OFFICE"
  install_apt ffmpeg imagemagick webp
fi

# ─── 10 · Tier NET (red local + VPS) ──────────────────────────────────
if [ "${XEK_TIER_NET:-0}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] · NET"
  install_apt mtr-tiny iperf3 nmap tcpdump ngrep traceroute whois socat \
              mosh autossh sshpass \
              nethogs iftop bmon \
              tmux screen netcat-openbsd \
              rclone restic wireguard-tools
  if command -v cargo >/dev/null; then
    [ -x "$HOME/.cargo/bin/gping" ]     || cargo install --quiet gping     2>/dev/null || true
    [ -x "$HOME/.cargo/bin/bandwhich" ] || cargo install --quiet bandwhich 2>/dev/null || true
  fi
  if [ ! -x "$HOME/.local/bin/croc" ]; then
    CV=$(curl -fsSL https://api.github.com/repos/schollz/croc/releases/latest 2>/dev/null | jq -r '.tag_name // empty')
    [ -n "$CV" ] && \
      curl -fsSL "https://github.com/schollz/croc/releases/download/${CV}/croc_${CV#v}_Linux-64bit.tar.gz" | \
      tar -xz -C "$HOME/.local/bin" croc 2>/dev/null || true
  fi
fi

# ─── 11 · Tier DOCKER (compose + lazydocker + dive + ctop + hadolint + trivy) ──
if [ "${XEK_TIER_DOCKER:-0}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] · DOCKER"
  install_apt docker-compose-plugin docker-buildx-plugin buildah skopeo
  if [ ! -x "$HOME/.local/bin/lazydocker" ]; then
    LV=$(curl -fsSL https://api.github.com/repos/jesseduffield/lazydocker/releases/latest 2>/dev/null | jq -r '.tag_name // empty')
    [ -n "$LV" ] && \
      curl -fsSL "https://github.com/jesseduffield/lazydocker/releases/download/${LV}/lazydocker_${LV#v}_Linux_x86_64.tar.gz" | \
      tar -xz -C "$HOME/.local/bin" lazydocker 2>/dev/null || true
  fi
  if [ ! -x "$HOME/.local/bin/dive" ]; then
    DV=$(curl -fsSL https://api.github.com/repos/wagoodman/dive/releases/latest 2>/dev/null | jq -r '.tag_name // empty')
    [ -n "$DV" ] && \
      curl -fsSL "https://github.com/wagoodman/dive/releases/download/${DV}/dive_${DV#v}_linux_amd64.tar.gz" | \
      tar -xz -C "$HOME/.local/bin" dive 2>/dev/null || true
  fi
  [ ! -x "$HOME/.local/bin/ctop" ] && \
    curl -fsSL https://github.com/bcicen/ctop/releases/download/v0.7.7/ctop-0.7.7-linux-amd64 \
      -o "$HOME/.local/bin/ctop"     2>/dev/null && chmod +x "$HOME/.local/bin/ctop"     2>/dev/null || true
  [ ! -x "$HOME/.local/bin/hadolint" ] && \
    curl -fsSL https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64 \
      -o "$HOME/.local/bin/hadolint" 2>/dev/null && chmod +x "$HOME/.local/bin/hadolint" 2>/dev/null || true
  if ! command -v trivy >/dev/null && [ ! -f /usr/share/keyrings/trivy.gpg ]; then
    curl -fsSL https://aquasecurity.github.io/trivy-repo/deb/public.key | \
      sudo -n gpg --dearmor -o /usr/share/keyrings/trivy.gpg 2>/dev/null || true
    echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main" | \
      sudo -n tee /etc/apt/sources.list.d/trivy.list >/dev/null 2>&1 || true
    rm -f "$APT_STAMP"
    install_apt trivy
  fi
fi

# ─── 12 · Tier LEGAL (pandoc + pdf + ocr-spa) ─────────────────────────
if [ "${XEK_TIER_LEGAL:-0}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] · LEGAL"
  install_apt pandoc poppler-utils qpdf tesseract-ocr tesseract-ocr-spa
fi

# ─── 13 · Tier WEB (corepack + pnpm + yarn sobre Node 24) ─────────────
if [ "${XEK_TIER_WEB:-1}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] · WEB"
  corepack enable                                  >/dev/null 2>&1 || true
  corepack prepare pnpm@latest  --activate         >/dev/null 2>&1 || true
  corepack prepare yarn@stable  --activate         >/dev/null 2>&1 || true
fi

# ─── 14 · uv tools globales (pre-commit, yamllint, csvkit, commitizen) ────
if [ "$SKIP" = 0 ]; then
  echo "[XEK] · uv tools"
  uv tool install --quiet pre-commit yamllint csvkit commitizen 2>/dev/null || true
fi

# ─── 15 · Pre-stage ~/.claude/ desde plantillas ───────────────────────
if [ -d "$XEK_PLANTILLAS/dot-claude/ejemplo_dot_claude" ] && [ ! -e "$HOME/.claude/mcp.json" ]; then
  mkdir -p "$HOME/.claude"
  if command -v rsync >/dev/null; then
    rsync -a --quiet --exclude='cloud-env/' --exclude='rc/' \
      "$XEK_PLANTILLAS/dot-claude/ejemplo_dot_claude/" "$HOME/.claude/" 2>/dev/null || true
  else
    cp -nR "$XEK_PLANTILLAS/dot-claude/ejemplo_dot_claude/." "$HOME/.claude/" 2>/dev/null || true
  fi
  echo "[XEK] ~/.claude/ pre-staged"
fi

# ─── 16 · Git defaults ────────────────────────────────────────────────
git config --global init.defaultBranch    main
git config --global pull.rebase           false
git config --global push.autoSetupRemote  true
git config --global rerere.enabled        true
git config --global core.pager            'cat'
git config --global user.name             "$AUTHOR"

# ─── 17 · Doors (puertas cifradas) ────────────────────────────────────
# Secretos por:  (a) MCPs ya autenticados en Claude Code
#                (b) age-cifrados en $XEK_SECRETS_DIR (700, gitignored)
#                (c) sops + age en $SOPS_AGE_KEY_FILE
chmod 700 "$XEK_SECRETS_DIR" 2>/dev/null || true
[ ! -f "$SOPS_AGE_KEY_FILE" ] && echo "[XEK] info · sin clave age (sops deshabilitado)"

# ─── 18 · Banner final ────────────────────────────────────────────────
echo "$(date -Is)" > "$STAMP"
T1=$(date +%s)
NODE_V=$(command -v node    >/dev/null && node    --version 2>/dev/null || echo "n/a")
PY_V=$(  command -v python3 >/dev/null && python3 --version 2>/dev/null | awk '{print $2}' || echo "n/a")
BUN_V=$( command -v bun     >/dev/null && bun     --version 2>/dev/null || echo "n/a")
cat <<BANNER
╔══════════════════════════════════════════════════════════════╗
║ XEK-ENV v3.3 listo en $((T1-T0))s · env=${XEK_ENV_NAME:-general}
║ host:    $(hostname)  ·  user: $(whoami)
║ node:    $NODE_V  (target v${NODE_VERSION})
║ python:  $PY_V    (target ${PYTHON_VERSION})
║ bun:     $BUN_V
║ tiers:   core=${XEK_TIER_CORE} runtimes=${XEK_TIER_RUNTIMES} py=${XEK_TIER_PY} shell=${XEK_TIER_SHELL} web=${XEK_TIER_WEB}
║          ai=${XEK_TIER_AI} office=${XEK_TIER_OFFICE} net=${XEK_TIER_NET} docker=${XEK_TIER_DOCKER} legal=${XEK_TIER_LEGAL}
║ log:     $XEK_LOG
╚══════════════════════════════════════════════════════════════╝
BANNER
