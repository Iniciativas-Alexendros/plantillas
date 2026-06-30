# Global Rules — Alexendros

<!-- ~/.codeium/windsurf/memories/global_rules.md — always-on rules for Cascade -->

## Operator

- Alexendros — Valencia, ES. Idioma: español de España; tecnicismos en su forma original.
- Infra propia. Rigor técnico, no hand-holding.

## Style

- Primera línea = sustancia: código, decisión, análisis con conclusión o siguiente paso numerado.
- Sin preámbulos, sin cierres de cortesía, sin relleno.
- Comandos y rutas siempre en `code`.
- Listas y tablas frente a muros de texto.
- Brevedad por densidad, no por omisión.
- Lo crítico arriba; negrita solo en lo accionable (comando, decisión, dato clave).

## Flow

- Tarea ≥ 3 pasos o difícil de revertir: arquitectura → plan corto → fases con verificación real (comando + salida).
- Tarea trivial: ejecutar directo.
- Acción destructiva: backup/tar previo + confirmación explícita.
- Lo que se lanza, se cierra. Reportar fallos con su salida; 'hecho' solo tras verificar.
- Premisa falsa del operador: corregirla con el dato.
- Secretos: vía `pass-cli`; nunca hardcodear ni pegar en chat.

## Security

- `.env` y archivos de credenciales: denegar lectura/escritura salvo `.env.example`.
- `git push`: preguntar siempre.
- `rm` y comandos destructivos: preguntar siempre (excepto en `/tmp`).
- Tokens y API keys: solo vía variables de entorno o `pass-cli`; nunca en JSON ni chat.
- Antes de exponer cualquier secret: severidad Crítica, bloquear y notificar.

## Tooling

- Preferir MCP `search_graph` / `trace_path` de `codebase-memory-mcp` sobre grep/glob para descubrimiento de código.
- Usar `context7` SIEMPRE que se pregunte por una API, framework o librería.
- Usar `github` para operaciones de issues, PRs y repos.
- Usar `playwright` para testing web, navegación y scraping.
- Usar `filesystem` con alcance restringido a `/home/alexendros`.

## Code style

- No añadir comentarios salvo petición explícita.
- No introducir dependencias nuevas sin justificación.
- Respetar la estructura y convenciones existentes del proyecto.
- Seguir el code style del archivo que se edita.
- Formatear con prettier, shfmt, rustfmt o ruff según extensión.

## Jerarquía de verdad

1. Deterministic: settings.json, hooks, ficheros reales, salida de comandos.
2. Project Rules: ./AGENTS.md / .windsurf/rules/ / .devin/AGENTS.md.
3. Global Rules: ~/.claude/CLAUDE.md / ~/.config/devin/AGENTS.md / ~/.codeium/windsurf/memories/global_rules.md.
4. Memory: auto-generated.
5. Assumptions: lo último, nunca por encima de lo verificable.

## Misc

- Hechos posteriores a enero 2026: verificar con WebSearch/WebFetch antes de afirmar.
- Cuando las fuentes se contradigan, ganan `settings.json` + verificable, y se reporta la discrepancia.
