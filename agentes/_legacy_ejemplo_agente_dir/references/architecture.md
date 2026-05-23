# Arquitectura de Referencia · ejemplo-agente

## Patrón: Hub-and-Spoke (Orquestador-Especialistas)

```
                    ┌─────────────┐
                    │  Usuario    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Orquestador │  ← ejemplo-agente (sonnet)
                    │  (Hub)      │     Síntesis, decisión, entrega
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌─────▼─────┐      ┌────▼────┐
   │ Explorer│      │  Planner  │      │ Reviewer│
   │(sonnet) │      │ (sonnet)  │      │ (haiku) │
   └─────────┘      └───────────┘      └─────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Executor   │  ← Subagente de ejecución
                    │  (sonnet)   │     Implementación de cambios
                    └─────────────┘
```

## Flujo de Mensajes

### Caso: Nueva Feature

```
Usuario: "Añade autenticación JWT al API"
  → Orquestador: clasifica como "nueva feature"
  → Orquestador: TodoWrite con plan macro
  → Orquestador → Explorer: "Mapea el API actual, entry points, auth existente"
  → Explorer → Orquestador: [reporte de exploración]
  → Orquestador → Planner: "Diseña auth JWT basado en exploración"
  → Planner → Orquestador: [plan detallado]
  → Orquestador: valida plan con usuario (si requerido)
  → Orquestador → Executor: "Implementa paso 1 del plan"
  → Executor → Orquestador: [cambios realizados + estado tests]
  → Orquestador → Reviewer: "Revisa los cambios de auth"
  → Reviewer → Orquestador: [reporte de review]
  → Orquestador: síntesis final + entrega al usuario
```

## Decisiones de Arquitectura

### ¿Por qué Hub-and-Spoke y no multi-agent libre?

- **Debuggeabilidad**: Un solo punto de coordinación facilita tracing.
- **Control de recursos**: El hub gestiona cuántos subagentes corren y cuándo.
- **Contexto eficiente**: Cada spoke solo ve lo que necesita.

### ¿Por qué modelos diferentes por rol?

- **Orquestador/Planner/Explorer**: Requieren razonamiento complejo → sonnet.
- **Reviewer**: Tarea paralelizable, mayor volumen → haiku (coste eficiente).
- **Executor**: Generación de código, contexto amplio → sonnet.

### ¿Por qué MCP como capa de tools?

- **Interoperabilidad**: Tools reutilizables entre agentes diferentes.
- **Seguridad**: Servidores MCP corren sandboxed.
- **Descubrimiento**: Tool search permite escalado sin sobrecarga de contexto.

## Anti-patrones a evitar

1. **Spoke hablando con spoke**: Toda comunicación inter-spoke pasa por el hub.
2. **Hub haciendo trabajo**: El hub orquesta, no ejecuta código.
3. **Subagentes anidados infinitos**: Máximo 3 niveles de profundidad.
4. **Contexto completo a todos**: Cada subagente recibe solo contexto relevante.

## Referencias

- [OpenAI Multi-Agent Orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [Claude Code: Agent Teams](https://code.claude.com/docs/en/agent-teams.md)
- [Google ADK: Multi-Agent Systems](https://google.github.io/adk-docs/multi-agent/)
