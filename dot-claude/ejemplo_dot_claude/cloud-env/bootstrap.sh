#!/usr/bin/env bash
# =====================================================================
# XEK-ENV v3.2 · Bootstrap horizontal para Claude Code on the web
# Sucesor de OMNI-ENV v3.0-FINAL · Autor: Alexendros
# Pega este script en el campo "Script de configuración" del diálogo
# "Actualizar entorno en la nube" (https://claude.ai/code).
#
# Garantías:
#   · idempotente (cache diaria $XEK_STATE/bootstrap-YYYY-MM-DD.stamp)
#   · tolerante a apt offline (no falla si no hay red apt)
#   · NO escribe secretos
#   · primera ejecución 60–120s (download de mise/node), siguientes <5s
#
# Tiers (toggleables vía env vars del propio diálogo):
#   CORE      fd, bat, eza, delta, zoxide, sops, zstd, rsync, sqlite3, httpie
#   RUNTIMES  mise + node@$NODE_VERSION (default 24) + python@$PYTHON_VERSION
#   PY        ipython + polars/pandas/numpy/httpx/pydantic/rich/typer/...
#   SHELL     zsh + starship + atuin + zinit + plugins + rcfiles
#   AI        huggingface_hub + llm + duckdb
#   OFFICE    ffmpeg + imagemagick + webp
#   NET       mtr/iperf3/nmap/tcpdump/mosh/autossh/tmux/rclone/restic/...
#   DOCKER    docker-compose-plugin + lazydocker + dive + ctop + hadolint + trivy
#   LEGAL     pandoc + poppler-utils + qpdf + tesseract-ocr-spa
#   WEB       corepack/pnpm/yarn shims (Node 24 ya viene de RUNTIMES)
# =====================================================================
set -Eeuo pipefail
trap 'echo "[XEK] bootstrap interrumpido en línea $LINENO" >&2' ERR

# ---------- 0. Logging y dirs ----------
mkdir -p "$XEK_CACHE" "$XEK_STATE" "$XEK_SECRETS_DIR" "$XEK_REPOS_HOME" \
         "$HOME/.config/starship" "$HOME/.local/bin" \
         "$HOME/.ipython/profile_default" "$HOME/.config/mise"
exec > >(tee -a "$XEK_LOG") 2>&1
START=$(date +%s)
echo "──────────── XEK-ENV v3.2 · $(date -Is) ────────────"

# ---------- 1. Locale + TZ ----------
sudo -n ln -sf "/usr/share/zoneinfo/$TZ" /etc/localtime 2>/dev/null || true
if ! locale -a 2>/dev/null | grep -qi 'es_ES.utf8'; then
  echo "es_ES.UTF-8 UTF-8" | sudo -n tee -a /etc/locale.gen >/dev/null 2>&1 || true
  sudo -n locale-gen >/dev/null 2>&1 || true
fi

# ---------- 2. PATH ----------
export PATH="$HOME/.local/share/mise/shims:$HOME/.local/bin:$HOME/.cargo/bin:$HOME/.bun/bin:/opt/node22/bin:/usr/local/go/bin:$PATH"

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
              httpie sqlite3 sops jpegoptim direnv jq yq bc
  [ -x /usr/bin/fdfind ] && ln -sf /usr/bin/fdfind  "$HOME/.local/bin/fd"
  [ -x /usr/bin/batcat ] && ln -sf /usr/bin/batcat  "$HOME/.local/bin/bat"
  # bun upgrade in-place (rapido, ya viene en la imagen)
  [ "${BUN_AUTO_UPGRADE:-1}" = 1 ] && command -v bun >/dev/null && bun upgrade --stable >/dev/null 2>&1 || true
fi

# ---------- 5. Tier RUNTIMES (mise + node + python) ----------
if [ "${XEK_TIER_RUNTIMES:-1}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] tier RUNTIMES (mise + node@${NODE_VERSION:-24} + python@${PYTHON_VERSION:-3.13})"
  if ! command -v mise >/dev/null; then
    curl -fsSL https://mise.run | sh >/dev/null 2>&1 || true
  fi
  if command -v mise >/dev/null; then
    mise use --global --quiet "node@${NODE_VERSION:-24}" 2>/dev/null || true
    [ -n "${PYTHON_VERSION:-}" ] && mise use --global --quiet "python@${PYTHON_VERSION}" 2>/dev/null || true
    # Asegura shims activos en este shell del bootstrap
    eval "$(mise activate bash --shims 2>/dev/null)" 2>/dev/null || true
  fi
fi

# ---------- 6. Tier SHELL (zsh + starship + atuin + plugins) ----------
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

# ---------- 7. Tier PY (ipython + librerías potentes) ----------
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

# ---------- 8. Tier AI ----------
if [ "${XEK_TIER_AI:-1}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] tier AI (huggingface_hub + llm + duckdb)"
  uv tool install --quiet huggingface_hub llm duckdb 2>/dev/null || true
fi

# ---------- 9. Tier OFFICE ----------
if [ "${XEK_TIER_OFFICE:-1}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] tier OFFICE (ffmpeg + imagemagick + webp)"
  install_apt ffmpeg imagemagick webp
fi

# ---------- 10. Tier NET (diagnóstico/optimización red local + VPS) ----------
if [ "${XEK_TIER_NET:-1}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] tier NET (mtr + iperf3 + nmap + tcpdump + mosh + tmux + ...)"
  install_apt mtr-tiny iperf3 nmap tcpdump traceroute whois socat ngrep \
              mosh autossh sshpass \
              nethogs iftop bmon \
              tmux screen \
              rclone restic netcat-openbsd \
              wireguard-tools
  # gping (graphical ping) via cargo si está rust
  if command -v cargo >/dev/null && [ ! -x "$HOME/.cargo/bin/gping" ]; then
    cargo install --quiet gping 2>/dev/null || true
  fi
  # bandwhich (per-process bandwidth) idem
  if command -v cargo >/dev/null && [ ! -x "$HOME/.cargo/bin/bandwhich" ]; then
    cargo install --quiet bandwhich 2>/dev/null || true
  fi
  # croc (file transfer) binario único
  if [ ! -x "$HOME/.local/bin/croc" ]; then
    CV=$(curl -fsSL https://api.github.com/repos/schollz/croc/releases/latest 2>/dev/null | jq -r '.tag_name // empty')
    if [ -n "$CV" ]; then
      curl -fsSL "https://github.com/schollz/croc/releases/download/${CV}/croc_${CV#v}_Linux-64bit.tar.gz" | \
        tar -xz -C "$HOME/.local/bin" croc 2>/dev/null || true
    fi
  fi
fi

# ---------- 11. Tier DOCKER (compose + lazydocker + dive + ctop + hadolint + trivy) ----------
if [ "${XEK_TIER_DOCKER:-1}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] tier DOCKER (compose + lazydocker + dive + ctop + hadolint + trivy)"
  install_apt docker-compose-plugin docker-buildx-plugin buildah skopeo
  # lazydocker
  if [ ! -x "$HOME/.local/bin/lazydocker" ]; then
    LV=$(curl -fsSL https://api.github.com/repos/jesseduffield/lazydocker/releases/latest 2>/dev/null | jq -r '.tag_name // empty')
    if [ -n "$LV" ]; then
      curl -fsSL "https://github.com/jesseduffield/lazydocker/releases/download/${LV}/lazydocker_${LV#v}_Linux_x86_64.tar.gz" | \
        tar -xz -C "$HOME/.local/bin" lazydocker 2>/dev/null || true
    fi
  fi
  # dive
  if [ ! -x "$HOME/.local/bin/dive" ]; then
    DV=$(curl -fsSL https://api.github.com/repos/wagoodman/dive/releases/latest 2>/dev/null | jq -r '.tag_name // empty')
    if [ -n "$DV" ]; then
      curl -fsSL "https://github.com/wagoodman/dive/releases/download/${DV}/dive_${DV#v}_linux_amd64.tar.gz" | \
        tar -xz -C "$HOME/.local/bin" dive 2>/dev/null || true
    fi
  fi
  # ctop
  [ ! -x "$HOME/.local/bin/ctop" ] && \
    curl -fsSL "https://github.com/bcicen/ctop/releases/download/v0.7.7/ctop-0.7.7-linux-amd64" \
      -o "$HOME/.local/bin/ctop" 2>/dev/null && chmod +x "$HOME/.local/bin/ctop" 2>/dev/null || true
  # hadolint (URL latest estable)
  [ ! -x "$HOME/.local/bin/hadolint" ] && \
    curl -fsSL "https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64" \
      -o "$HOME/.local/bin/hadolint" 2>/dev/null && chmod +x "$HOME/.local/bin/hadolint" 2>/dev/null || true
  # trivy (apt repo, una sola vez)
  if ! command -v trivy >/dev/null && [ ! -f /usr/share/keyrings/trivy.gpg ]; then
    curl -fsSL https://aquasecurity.github.io/trivy-repo/deb/public.key | \
      sudo -n gpg --dearmor -o /usr/share/keyrings/trivy.gpg 2>/dev/null || true
    echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main" | \
      sudo -n tee /etc/apt/sources.list.d/trivy.list >/dev/null 2>&1 || true
    install_apt trivy
  fi
fi

# ---------- 12. Tier LEGAL ----------
if [ "${XEK_TIER_LEGAL:-0}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] tier LEGAL (pandoc + pdf + ocr-spa)"
  install_apt pandoc poppler-utils qpdf tesseract-ocr tesseract-ocr-spa
fi

# ---------- 13. uv tool global (pipx-style) ----------
if [ "$SKIP" = 0 ]; then
  echo "[XEK] uv tool · pre-commit, yamllint, csvkit, commitizen"
  uv tool install --quiet pre-commit yamllint csvkit commitizen 2>/dev/null || true
fi

# ---------- 14. Tier WEB (corepack/pnpm/yarn) ----------
if [ "${XEK_TIER_WEB:-1}" = 1 ] && [ "$SKIP" = 0 ]; then
  echo "[XEK] tier WEB (corepack + pnpm + yarn)"
  corepack enable >/dev/null 2>&1 || true
  corepack prepare pnpm@latest --activate >/dev/null 2>&1 || true
  corepack prepare yarn@stable --activate >/dev/null 2>&1 || true
fi

# ---------- 15. Pre-stage ~/.claude/ ----------
if [ -d "$XEK_PLANTILLAS/dot-claude/ejemplo_dot_claude" ] && [ ! -e "$HOME/.claude/mcp.json" ]; then
  mkdir -p "$HOME/.claude"
  # Excluye cloud-env/ y rc/ del staging (no son contenido de ~/.claude)
  rsync -a --quiet \
    --exclude='cloud-env/' --exclude='rc/' \
    "$XEK_PLANTILLAS/dot-claude/ejemplo_dot_claude/" "$HOME/.claude/" 2>/dev/null || \
    cp -nR "$XEK_PLANTILLAS/dot-claude/ejemplo_dot_claude/." "$HOME/.claude/"
  echo "[XEK] ~/.claude/ pre-staged desde dot-claude/ejemplo_dot_claude/"
fi

# ---------- 16. Git defaults ----------
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global push.autoSetupRemote true
git config --global rerere.enabled true
git config --global core.pager 'cat'
git config --global user.name "$AUTHOR"

# ---------- 17. Doors (puertas cifradas) ----------
chmod 700 "$XEK_SECRETS_DIR" 2>/dev/null || true
[ ! -f "$SOPS_AGE_KEY_FILE" ] && echo "[XEK] info · sin clave age (sops deshabilitado)"

# ---------- 18. Banner ----------
echo "$(date -Is)" > "$STAMP"
END=$(date +%s)
NODE_NOW=$(command -v node >/dev/null && node --version 2>/dev/null || echo "n/a")
cat <<BANNER
╔════════════════════════════════════════════════════════╗
║ XEK-ENV v3.2 listo en $((END-START))s
║ host:        $(hostname)  ·  user: $(whoami)
║ plantillas:  $XEK_PLANTILLAS
║ repos:       $XEK_REPOS_HOME
║ lang:        $XEK_LANG · TZ=$TZ
║ node:        $NODE_NOW (target=v$NODE_VERSION)
║ tiers on:    core=$XEK_TIER_CORE runtimes=$XEK_TIER_RUNTIMES py=$XEK_TIER_PY shell=$XEK_TIER_SHELL
║              ai=$XEK_TIER_AI office=$XEK_TIER_OFFICE net=$XEK_TIER_NET docker=$XEK_TIER_DOCKER
║              legal=$XEK_TIER_LEGAL web=$XEK_TIER_WEB
║ log:         $XEK_LOG
╚════════════════════════════════════════════════════════╝
BANNER
