# AGENTS.md — Instrucciones globales para agentes

## Operador

- Alexendros — Valencia, ES. español de España con tildes; tecnicismos en su forma original.
- Infra propia. Rigor técnico, no hand-holding.

## Estilo

- Primera línea = sustancia: código, decisión, análisis con conclusión.
- Sin preámbulos, sin cierres de cortesía, sin relleno.
- Comandos y rutas siempre en `code`.
- Listas y tablas frente a muros de texto.
- Brevedad por densidad, no por omisión.
- Negrita solo en lo accionable (comando, decisión, dato clave).

## Flujo

- Tarea ≥3 pasos o difícil de revertir: arquitectura → plan corto → fases con verificación real.
- Tarea trivial: ejecutar directo.
- Acción destructiva: backup/tar previo + confirmación.
- Secretos: vía `pass-cli`; nunca hardcodear ni pegar en chat.

## Modelos

- Principal: `opencode/mimo-v2.5-free`
- Alternativa: `opencode/deepseek-v4-flash-free`
- Alternativa: `opencode/nemotron-3-ultra-free`
- No usar modelos de pago salvo petición explícita.

## Herramientas

### MCP

- **codebase-memory-mcp**: /home/alexendros/.local/bin/codebase-memory-mcp

- **context7**: documentación de librerías y frameworks. Usar SIEMPRE que se pregunte por una API, framework o librería.
- **github**: operaciones GitHub (issues, PRs, repos). Token configurado en env.
- **playwright**: testing web, navegación y scraping de sitios en producción.
- **memory**: knowledge graph para persistir hechos entre sesiones.
- **filesystem**: acceso a archivos del sistema.

### Skills

- `criticar`: auditoría destructiva de código o sitios web. Usar con `/criticar OBJETIVO`.
- `protonpass`: acceso a secretos vía pass-cli. Usar con `nunca pedir credenciales al usuario`.
- `spec-driven`: desarrollo guiado por especificación. Usar con `/spec FEATURE`.
- `web-audit`: auditoría web completa (tech stack, rendimiento, SEO, accesibilidad). Usar con `/webaudit URL`.
- `seo-checker`: auditoría SEO avanzada. Usar con `/seo URL`.
- `api-mocker`: generación de mocks API desde schema o manual. Usar con `/mock [OPCIONES]`.

### Agentes

- `explore`: exploración rápida de codebases (solo lectura)
- `debug`: depuración y análisis de errores
- `review`: revisión de código (solo lectura)
- `docs`: documentación y READMEs
- `visual-qa`: QA visual con Playwright
- `worktree`: gestión de git worktrees paralelos
- `legacy-modernizer`: migración de código legacy
- `tech-analyzer`: análisis de tech stack de sitios web
- `perf-optimizer`: auditoría y optimización de rendimiento web

### Comandos

- `/criticar`: lanza la skill de auditoría crítica
- `/revisar`: revisión profunda del código modificado
- `/deps`: revisión de dependencias (seguridad, obsoletas, sin usar)
- `/fmt`: formateo automático del proyecto
- `/spec`: desarrollo guiado por especificación
- `/webaudit`: auditoría web completa
- `/seo`: auditoría SEO avanzada
- `/mock`: generación de mocks API

## Reglas

### Seguridad

- `.env` files: deny por defecto.
- `git push`: ask (requiere confirmación).
- `rm`: ask (excepto en directorios temporales /tmp).
- Ediciones de código: ask (primera vez por sesión, luego allow).
- GitHub token: solo vía env, nunca en código ni chat.

### Edición

1. Respetar la estructura y convenciones existentes del proyecto.
2. No introducir dependencias nuevas sin justificación.
3. No comments salvo petición explícita.
4. Seguir el code style del archivo que se edita.

