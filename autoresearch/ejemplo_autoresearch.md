---
name: prompt-caching-vs-memory-claude-api
description: >
  Investigación sobre las diferencias entre prompt caching y memory en la
  Claude API, cuándo conviene cada mecanismo y cómo afectan al coste y
  a la latencia en aplicaciones Claude Code.
topic: claude-api anthropic prompt-caching memory cost latency
sources:
  - "https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching"
  - "https://docs.anthropic.com/en/docs/build-with-claude/memory"
  - "https://docs.anthropic.com/en/api/messages"
status: published
last_updated: 2026-05-23
confidence: 0.85
---

## Pregunta

¿Cuál es la diferencia entre prompt caching y memory en la Claude API, y
cuándo conviene usar cada uno para optimizar coste y latencia?

## Fuentes

- [Prompt caching — Anthropic docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
  — Documentación oficial de la funcionalidad de caché de prefijos.
- [Memory — Anthropic docs](https://docs.anthropic.com/en/docs/build-with-claude/memory)
  — Guía de los mecanismos de memoria de larga duración en Claude.
- [Messages API reference](https://docs.anthropic.com/en/api/messages)
  — Referencia de la API de mensajes; parámetros de caché y de contexto.

## Hallazgos

- **Prompt caching** opera a nivel de prefijo de contexto: marcas un bloque
  de texto con `cache_control: {type: "ephemeral"}` y Anthropic lo guarda
  en caché en sus servidores durante 5 minutos (configurable). Las llamadas
  siguientes que reutilicen exactamente ese prefijo pagan ~90 % menos en
  tokens de entrada y reducen la latencia de procesamiento.

- **Memory** se refiere a mecanismos de almacenamiento externo al contexto de
  la conversación: archivos, bases de datos, o el sistema de archivos del
  operador. No es una función built-in de la API, sino un patrón arquitectónico
  implementado por la aplicación (por ejemplo, guardar resúmenes en un `.md`
  que se inyecta en cada prompt).

- El prompt caching es **stateless desde la perspectiva del cliente**: no hay
  garantía de que el caché persista entre sesiones distintas o tras 5 minutos
  de inactividad; el precio de cache hit es `input_tokens × 0.10` vs.
  `input_tokens × 1.0` sin caché (Sonnet 3.7 en la fecha de este cuaderno).

- Memory externa **persiste indefinidamente** pero añade la responsabilidad de
  gestión al operador: retrieval, actualización y coherencia son responsabilidad
  de la aplicación.

- Los casos de uso no se solapan completamente: prompt caching es adecuado para
  documentos largos repetidos (system prompts, código base, RAG chunks estáticos);
  memory externa es adecuada para contexto de usuario que evoluciona entre
  sesiones (historial de preferencias, hechos personalizados).

- Claude Code (`~/.claude/`) usa ambos: el `CLAUDE.md` se inyecta en cada hilo
  (candidato a caché de prefijo) y los archivos de memoria viva (`MEMORY.md`,
  `feedback_*.md`) son memory externa leída por hooks o skills.

## Veredicto

Prompt caching y memory son complementarios, no alternativos. Usar **prompt
caching** cuando el mismo bloque de texto aparece en múltiples llamadas API
dentro de una ventana corta (mismo agente, mismo documento de referencia);
usar **memory externa** cuando la información debe persistir entre sesiones o
evolucionar de forma estructurada. En la práctica, la combinación óptima para
Claude Code es: `CLAUDE.md` + contexto del proyecto con `cache_control`, y
archivos de memoria viva cargados por skills/hooks. Confianza: 0.85.

## Pendientes

- [ ] Verificar si `cache_control` puede aplicarse a bloques de herramientas
  (`tools`) además de mensajes de sistema y usuario.
- [ ] Medir experimentalmente el ahorro real de coste en un hilo largo de
  Claude Code con `CLAUDE.md` cacheado (~8 k tokens).
- [ ] Revisar si la duración del caché (5 min) varía según plan de API.
