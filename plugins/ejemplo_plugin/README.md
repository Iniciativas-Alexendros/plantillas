# github-integration

> Plugin de integración con GitHub para Claude Code

## Qué incluye

- **Agente `pr-reviewer`**: Revisa PRs automáticamente buscando bugs y smell.
- **Skill `github-commands`**: Comandos slash para GitHub (`/pr`, `/issue`).
- **Hook `pre-push-audit`**: Valida calidad antes de permitir `git push`.
- **MCP Server `github`**: Acceso a API de GitHub vía MCP.

## Instalación

```bash
# Copiar a plugins de Claude
cp -r github-integration ~/.claude/plugins/

# Configurar token
export GITHUB_TOKEN=ghp_xxxxxxxx
```

## Uso

```
/pr review 42           ← Revisa el PR #42
/issue create "Bug: ..." ← Crea un issue
```

## Dependencias

- `GITHUB_TOKEN` con scopes: `repo`, `issues`, `pull_requests`
- MCP server de GitHub instalado globalmente
