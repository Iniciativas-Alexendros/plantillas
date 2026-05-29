---
name: app-despliegue
description: >
  Despliegue a Vercel (serverless), Coolify/Dokploy (self-hosted VPS) o estático.
  Activa al pedir deploy, dominio/DNS, "producción", "staging", "Vercel", "Coolify",
  "502", "build failed en deploy", o configurar el entorno de despliegue.
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# Despliegue

Gestiona el ciclo de publicación según la plataforma del repo.

## Rutas

- **Vercel (serverless)**: build remoto; verifica `pnpm build` local primero;
  variables en el panel, nunca en git; dominios/alias tras deploy.
- **Coolify/Dokploy (self-hosted)**: `docker compose` gestionado por la plataforma;
  imagen pinned (sin `:latest`); secretos en la UI de la plataforma.
- **Estático**: `pnpm build && export`; publicar artefacto.

## Preflight (antes de desplegar)

1. Build/test verde local (ver `app-ci-cd`).
2. Variables/secretos presentes en la plataforma (no en repo).
3. Plan de rollback definido (versión anterior recuperable).

## Infra del operador

Para VPS/DNS usa el MCP `hostinger` (lectura para diagnóstico; cambios solo con
confirmación). El go-live de secretos reales (claves LIVE) es acto del operador.

## Salida

Estado del despliegue, URL/dominio, y verificación post-deploy (servicio responde).
