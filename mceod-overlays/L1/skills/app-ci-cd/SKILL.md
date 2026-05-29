---
name: app-ci-cd
description: >
  Diseñar y validar pipelines CI/CD (GitHub Actions): lint, build, test, validación
  estructural, escaneo de dependencias y branch protection. Activa al crear/arreglar
  workflows, "CI", "GitHub Actions", "pipeline", "checks", "branch protection".
allowed-tools: Read, Grep, Glob, Bash
---

# CI/CD (GitHub Actions)

Pipelines reproducibles que actúan de puerta antes de integrar a `main`.

## Estructura mínima de workflow

- Disparadores: `push` y `pull_request` a `main`; `concurrency` con cancel-in-progress.
- `permissions: contents: read` por defecto; elevar solo lo necesario.
- Jobs por stack: lint → build → test → validación estructural.
- `set -o pipefail` en cada `run` multilínea.

## Gates por tipo de repo

- **Webapp/MCP**: `pnpm install --frozen-lockfile`, `pnpm build`, `pnpm test`.
- **Rust**: `cargo build`, `cargo test`, `cargo clippy -- -D warnings`.
- **Infra (compose)**: `docker compose config --quiet` y prohibir `:latest`
  (`grep -nE 'image:\s*\S+:latest'` ⇒ fallar).
- **Registro/datos**: `python tools/validate.py`.
- **Homologación**: `python repositorios/validar_repositorio.py <repo> --strict`.

## Verificación local antes de pushear

```bash
set -o pipefail
gh run list --limit 5
# reproducir el gate localmente según stack
```

## Salida

`ci.yml` válido (o diagnóstico del fallo) y confirmación de que el gate corre en verde.
