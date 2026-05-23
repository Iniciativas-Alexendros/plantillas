---
name: github-commands
description: >
  Comandos rápidos para operaciones frecuentes de GitHub:
  crear PR, listar issues, revisar estado de CI.
allowed-tools:
  - Bash
  - Read
---

# GitHub Commands

## Cuándo usar

- El usuario pide "crea un PR", "qué issues hay abiertos", "estado de CI".

## Reglas

- Preferir `gh` CLI si está autenticado.
- Si no hay `gh`, usar `curl` con `GITHUB_TOKEN`.

## Comandos comunes

```bash
# Crear PR
gh pr create --title "feat: descripción" --body "Cuerpo del PR"

# Listar issues abiertos
gh issue list --state open --limit 20

# Estado de CI del PR actual
gh pr checks
```
