#!/usr/bin/env bash
# auditoria-canon-repo.sh · audita el cumplimiento del canon en uno o todos los repos.
#
# Uso:
#   auditoria-canon-repo.sh --repo <slug> [--path <ruta>]    # uno
#   auditoria-canon-repo.sh --all [--report]                  # todos vía gh
#
# Salida:
#   - Sin --report: tabla compacta a stdout.
#   - Con --report: archivo Markdown en
#     ~/.claude/cuadernos/meta__AlexendrosCodeCore_*/artefactos/canon-cumplimiento-YYYY-MM-DD.md.

set -euo pipefail

PLANTILLAS_DIR="${PLANTILLAS_DIR:-$HOME/.claude/herramientas/plantillas/repos}"
REPOS_YAML="${REPOS_YAML:-$PLANTILLAS_DIR/repos.yaml}"

ALL=0
REPORT=0
REPO_SLUG=""
REPO_PATH=""

usage() { sed -n '2,11p' "$0"; exit 0; }
log() { printf '%s\n' "$*" >&2; }
error() { printf '[error] %s\n' "$*" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)    REPO_SLUG="$2"; shift 2 ;;
    --path)    REPO_PATH="$2"; shift 2 ;;
    --all)     ALL=1; shift ;;
    --report)  REPORT=1; shift ;;
    -h|--help) usage ;;
    *) error "Argumento desconocido: $1" ;;
  esac
done

# --- yaml helper (compartido con aplica-canon-repo.sh) ---------------------
if command -v yq >/dev/null 2>&1; then YQ="yq"; else YQ=""; fi
yaml_get() {
  if [[ -n "$YQ" ]]; then yq -r "$1" "$2"
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
    if cur is None: print('null'); sys.exit(0)
print(cur if not isinstance(cur, (dict, list)) else yaml.safe_dump(cur).strip())
PY
  fi
}

# --- esperado por perfil ---------------------------------------------------
expected_for_profile() {
  local profile="$1" visibility="$2"
  local files=(
    "CHANGELOG.md" "CONTRIBUTING.md" "CODE_OF_CONDUCT.md" "SECURITY.md"
    "AUTHORS.md" "SUPPORT.md" "MAINTAINERS.md" "RELEASE.md" "ROADMAP.md"
    ".github/PULL_REQUEST_TEMPLATE.md" ".github/CODEOWNERS"
    ".editorconfig" ".gitattributes"
    "README.md" ".gitignore"
    ".github/dependabot.yml" ".github/workflows/ci.yml"
    "docs/adr/0001-template.md" "docs/README.md"
  )
  if [[ "$visibility" == "public" ]]; then
    files+=(
      ".github/FUNDING.yml"
      ".github/ISSUE_TEMPLATE/bug.yml"
      ".github/ISSUE_TEMPLATE/feature.yml"
      ".github/ISSUE_TEMPLATE/question.yml"
      ".github/ISSUE_TEMPLATE/security.yml"
      ".github/ISSUE_TEMPLATE/config.yml"
    )
  fi
  case "$profile" in
    web-nextjs) files+=( "ARCHITECTURE.md" "DESIGN.md" "STYLEGUIDE.md" )
                [[ "$visibility" == "public" ]] && files+=( "public/.well-known/security.txt" )
                ;;
    mcp-server) files+=( "ARCHITECTURE.md" ) ;;
    library-design-system) files+=( "ARCHITECTURE.md" ) ;;
  esac
  printf '%s\n' "${files[@]}"
}

# --- audit local (revisa REPO_PATH) ----------------------------------------
audit_local() {
  local slug="$1" path="$2"
  local profile visibility
  profile="$(yaml_get ".repos.${slug}.profile" "$REPOS_YAML")"
  visibility="$(yaml_get ".repos.${slug}.visibility" "$REPOS_YAML")"
  local total=0 ok=0 missing=()
  while IFS= read -r f; do
    total=$((total + 1))
    if [[ -e "$path/$f" ]]; then ok=$((ok + 1))
    else missing+=("$f"); fi
  done < <(expected_for_profile "$profile" "$visibility")
  # licencia
  total=$((total + 1))
  case "$(yaml_get ".repos.${slug}.license" "$REPOS_YAML")" in
    PROPRIETARY) [[ -e "$path/COPYRIGHT.md" ]] && ok=$((ok + 1)) || missing+=("COPYRIGHT.md") ;;
    *) [[ -e "$path/LICENSE" ]] && ok=$((ok + 1)) || missing+=("LICENSE") ;;
  esac
  local pct=$(( ok * 100 / total ))
  printf '%-40s  %3d/%-3d  %3d%%  %s\n' "$slug" "$ok" "$total" "$pct" \
    "$([ ${#missing[@]} -gt 0 ] && echo "FALTA: ${missing[*]}" || echo "OK")"
}

# --- audit remoto (vía gh api contents) ------------------------------------
audit_remote() {
  local slug="$1"
  local owner profile visibility
  owner="$(yaml_get ".repos.${slug}.owner" "$REPOS_YAML")"
  profile="$(yaml_get ".repos.${slug}.profile" "$REPOS_YAML")"
  visibility="$(yaml_get ".repos.${slug}.visibility" "$REPOS_YAML")"
  [[ "$profile" == "null" ]] && return
  local total=0 ok=0 missing=()
  while IFS= read -r f; do
    total=$((total + 1))
    if gh api "repos/${owner}/${slug}/contents/${f}" --silent >/dev/null 2>&1; then
      ok=$((ok + 1))
    else missing+=("$f"); fi
  done < <(expected_for_profile "$profile" "$visibility")
  total=$((total + 1))
  case "$(yaml_get ".repos.${slug}.license" "$REPOS_YAML")" in
    PROPRIETARY)
      gh api "repos/${owner}/${slug}/contents/COPYRIGHT.md" --silent >/dev/null 2>&1 \
        && ok=$((ok + 1)) || missing+=("COPYRIGHT.md") ;;
    *)
      gh api "repos/${owner}/${slug}/contents/LICENSE" --silent >/dev/null 2>&1 \
        && ok=$((ok + 1)) || missing+=("LICENSE") ;;
  esac
  local pct=$(( ok * 100 / total ))
  printf '%-40s  %3d/%-3d  %3d%%  %s\n' "$slug" "$ok" "$total" "$pct" \
    "$([ ${#missing[@]} -gt 0 ] && echo "FALTA: ${missing[*]}" || echo "OK")"
}

# --- main -------------------------------------------------------------------
header() { printf '%-40s  %-7s  %-4s  %s\n' "REPO" "OK/TOT" "PCT" "ESTADO"; printf '%s\n' "$(printf '%.0s-' {1..120})"; }

if [[ $ALL -eq 1 ]]; then
  out=$(mktemp)
  {
    header
    if [[ -n "$YQ" ]]; then
      while IFS= read -r slug; do
        [[ "$slug" == "null" ]] && continue
        archived="$(yaml_get ".repos.${slug}.archived" "$REPOS_YAML")"
        [[ "$archived" == "true" ]] && continue
        audit_remote "$slug"
      done < <(yq -r '.repos | keys[]' "$REPOS_YAML")
    else
      while IFS= read -r slug; do
        audit_remote "$slug"
      done < <(python3 - "$REPOS_YAML" <<'PY'
import yaml, sys
data = yaml.safe_load(open(sys.argv[1]))
for slug, meta in (data.get('repos') or {}).items():
    if (meta or {}).get('archived'):
        continue
    print(slug)
PY
)
    fi
  } | tee "$out"

  if [[ $REPORT -eq 1 ]]; then
    cuaderno_dir=$(ls -d "$HOME/.claude/cuadernos/meta__AlexendrosCodeCore"* 2>/dev/null | head -1)
    [[ -z "$cuaderno_dir" ]] && cuaderno_dir="$HOME/.claude/cuadernos/claude__CoreAlexendrosCodex"
    mkdir -p "$cuaderno_dir/artefactos"
    out_md="$cuaderno_dir/artefactos/canon-cumplimiento-$(date +%F).md"
    {
      printf '# Cumplimiento canon de repos · %s\n\n' "$(date +%F)"
      printf '```\n'
      cat "$out"
      printf '```\n'
    } > "$out_md"
    log "Informe en: $out_md"
  fi
else
  [[ -z "$REPO_SLUG" ]] && error "Falta --repo <slug> o --all"
  header
  if [[ -n "$REPO_PATH" ]]; then audit_local "$REPO_SLUG" "$REPO_PATH"
  else audit_remote "$REPO_SLUG"; fi
fi
