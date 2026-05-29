---
name: app-docker
description: >
  Dockerfile multi-stage, docker-compose, healthchecks e imágenes reproducibles.
  Activa al pedir "Docker", "compose", "contenedor", "imagen", "healthcheck",
  "multi-stage", o al validar/arreglar un docker-compose.
allowed-tools: Read, Grep, Glob, Bash
---

# Docker y compose

Contenedores reproducibles y validables sin levantar nada.

## Principios

- **Multi-stage**: separa build de runtime; imagen final mínima.
- **Pinned**: fija versión de imagen; prohibido `:latest` (reproducibilidad).
- **Healthcheck**: define `healthcheck` para que orquestadores detecten readiness.
- **Secretos**: por entorno/UI de la plataforma, nunca en la imagen ni en git.

## Validación (sin ejecutar contenedores)

```bash
set -o pipefail
cp -n .env.example .env 2>/dev/null || true
docker compose config --quiet        # valida esquema y resolución de variables
if grep -nE 'image:\s*\S+:latest' docker-compose.yml; then
  echo "prohibido :latest"; exit 1
fi
```

## Salida

`docker-compose.yml`/`Dockerfile` válidos (o diagnóstico), con imágenes pinned y el
comando de validación que pasa en verde.
