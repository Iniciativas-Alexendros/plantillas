#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# module-map.sh — Mapa centralizado de módulos del sistema de plantillas
#
# Elimina la duplicación de lógica módulo→singular→paths en workflows.
#
# Uso:
#   source .github/scripts/module-map.sh
#   SCRIPT=$(module_validator "agentes")   # → agentes/validar_agente.py
#   EJEMPLO=$(module_ejemplo "agentes")    # → agentes/ejemplo_agente
#   PLANTILLA=$(module_plantilla "agentes")# → agentes/plantilla_agente
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

# Lista canónica de módulos (usados por workflows que hacen source de este script)
# shellcheck disable=SC2034
MODULOS_CANONICOS=(agentes skills commands hooks mcp plugins dot-claude repositorios modulo proyecto)

# Módulos cuya raíz ES la plantilla (sin plantilla_*/ejemplo_*)
# shellcheck disable=SC2034
MODULOS_ESPECIALES=(modulo proyecto)

module_singular() {
  case "$1" in
    agentes)      echo "agente" ;;
    skills)       echo "skill" ;;
    commands)     echo "command" ;;
    hooks)        echo "hook" ;;
    mcp)          echo "mcp" ;;
    plugins)      echo "plugin" ;;
    dot-claude)   echo "dot_claude" ;;
    repositorios) echo "repositorio" ;;
    modulo)       echo "modulo" ;;
    proyecto)     echo "proyecto" ;;
    *)            echo "$1" ;;
  esac
}

module_validator() {
  local mod="$1"
  local singular
  singular=$(module_singular "$mod")
  echo "${mod}/validar_${singular}.py"
}

module_ejemplo() {
  local mod="$1"
  local singular
  singular=$(module_singular "$mod")
  if module_is_special "$mod"; then
    echo "$mod"
  else
    echo "${mod}/ejemplo_${singular}"
  fi
}

module_plantilla() {
  local mod="$1"
  local singular
  singular=$(module_singular "$mod")
  if module_is_special "$mod"; then
    echo "$mod"
  else
    echo "${mod}/plantilla_${singular}"
  fi
}

module_is_special() {
  local mod="$1"
  for special in "${MODULOS_ESPECIALES[@]}"; do
    if [ "$mod" = "$special" ]; then
      return 0
    fi
  done
  return 1
}
