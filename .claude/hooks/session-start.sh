#!/bin/bash
# SessionStart hook · instala dependencias para que los tests y linters
# del sistema de plantillas funcionen en Claude Code on the web.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"

echo "[session-start] Instalando dependencias del sistema..."
if command -v apt-get >/dev/null 2>&1; then
  if ! command -v shellcheck >/dev/null 2>&1; then
    sudo apt-get update -qq
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends shellcheck
  fi
fi

echo "[session-start] Instalando dependencias Python..."
PIP="$(command -v pip3 || command -v pip)"
"$PIP" install --quiet --upgrade --user \
  -r requirements.txt \
  ruff \
  yamllint \
  pytest \
  pre-commit

if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  # shellcheck disable=SC2016
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$CLAUDE_ENV_FILE"
fi

echo "[session-start] OK"
