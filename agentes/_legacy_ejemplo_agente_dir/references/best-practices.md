# Mejores Prácticas · ejemplo-agente

> Síntesis de prácticas oficiales de Anthropic, OpenAI, y Google.

## 1. Diseño de Agentes

### Anthropic: Simplicidad deliberada
- "A simple, single-threaded master loop combined with disciplined tools and
  planning delivers controllable autonomy."
- Prefiere loops debuggeables sobre orquestación compleja.
- Usa TODO-based planning con reminder injection.

### OpenAI: Handoffs claros
- Define handoffs explícitos: qué agente transfiere a qué otro y bajo qué
  condiciones.
- Guardrails paralelos: validación de seguridad sin bloquear ejecución.
- Tracing por defecto: toda ejecución es observable.

### Google: Jerarquía explícita
- Root agent con `sub_agents` declarados.
- Blackboard pattern para estado compartido.
- A2A protocol para comunicación inter-framework.

## 2. Gestión de Contexto

### Progressive Disclosure (MCP / Claude Code)
```
Sesión inicia: solo metadata de skills/tools disponibles.
↓
Skill triggered: carga SKILL.md completo.
↓
Referencia necesaria: carga archivo de referencia.
↓
Resultado: context window usado eficientemente.
```

### Compresión de Contexto (Claude Code)
- A ~92% de context window, resume y archiva a memoria persistente.
- Usa markdown files para memoria a largo plazo.
- Grep/Glob sobre embeddings para navegación en vivo.

## 3. Seguridad

### Permisos por capas
```
Nivel 1: Mode (unrestricted / restricted / ask)
Nivel 2: Tool allow/deny lists
Nivel 3: Bash allow/deny regex
Nivel 4: Filesystem path restrictions
Nivel 5: Hooks (pre/post tool execution)
```

### Validación de Inputs
- Todo tool input debe pasar por schema validation (JSON Schema / Pydantic).
- Sanitizar paths antes de operaciones filesystem.
- Nunca pasar input del usuario directamente a shell sin escaping.

## 4. Calidad de Código Generado

### Checklist post-ejecución
- [ ] Tests existentes siguen pasando.
- [ ] Nuevos tests cubren cambios.
- [ ] No hay warnings de linter/typechecker nuevos.
- [ ] Código sigue convenciones del proyecto.
- [ ] Documentación actualizada si aplica.
- [ ] No hay secrets o credenciales hardcodeadas.

### Principios aplicables
- **KISS**: Keep It Stupidly Simple.
- **YAGNI**: You Aren't Gonna Need It.
- **DRY**: Don't Repeat Yourself (pero prefiera WET sobre abstracción prematura).
- **SOLID**: Aplicable a diseño de clases y módulos.

## 5. Observabilidad

### Tracing
- Toda ejecución de agente debe ser trazable.
- Incluir: input, decisiones de routing, tool calls, outputs, errores.
- Formato: OpenTelemetry para interoperabilidad.

### Cost Tracking
- Monitorear uso de tokens por agente y por tool.
- Downgradear modelo automáticamente para tareas simples.
- Alertar si coste excede presupuesto por sesión.

### Session Storage
- Mirror de transcripts a storage externo (S3, Redis).
- Posibilidad de resumir y reanudar sesiones.
- Retención configurable según política de datos.

## 6. Testing de Agentes

### Estrategia
- **Unit tests**: Testear tools individuales con mocks.
- **Integration tests**: Testear flujos end-to-end con fixtures.
- **Evals**: Benchmarks de calidad de output (ej: SWE-bench).
- **Red teaming**: Probar límites de seguridad y comportamiento adversarial.

### Métricas
- **Task success rate**: % de tareas completadas correctamente.
- **Mean turns to completion**: Número medio de turnos necesarios.
- **Token efficiency**: Tokens usados por tarea completada.
- **User satisfaction**: Rating post-sesión.

## Referencias

- [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices.md)
- [OpenAI Agents SDK Guide](https://openai.github.io/openai-agents-python/)
- [Google ADK Docs](https://google.github.io/adk-docs/)
- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices.md)
