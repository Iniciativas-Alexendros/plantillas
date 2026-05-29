---
name: dev-estrategia-tests
description: >
  Diseñar estrategia y plan de tests y configurar herramientas (Vitest, Playwright,
  pytest, cargo test). Activa al pedir test plan, cobertura, qué/cómo testear,
  pirámide de tests, E2E, smoke test, pre-commit, o configurar el runner.
allowed-tools: Read, Grep, Glob, Bash
---

# Estrategia de tests

Define qué testear y cómo, proporcional al riesgo del cambio.

## Pirámide

- **Unit**: lógica pura, casos límite. Rápidos y numerosos.
- **Integración**: módulos/IO/DB con dobles donde haga falta.
- **E2E/smoke**: recorridos críticos del usuario o arranque del servicio.

## Por stack

- **TS/Next**: Vitest (unit/integración) + Playwright (E2E). `pnpm test`.
- **Rust**: `cargo test`; `cargo clippy` como gate de lint.
- **Python**: `pytest`; `ruff` para lint.

## Criterio

1. Todo cambio de comportamiento lleva test pareado.
2. Define cobertura mínima por repo y un smoke que verifique "arranca y responde".
3. Integra el gate en CI (ver `app-ci-cd`) y, si procede, en pre-commit.

## Salida

Plan de tests: qué casos, en qué nivel, con qué runner, y el comando de CI que los
ejecuta en verde.
