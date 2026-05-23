# references/best-practices.md · Playbook de contenido

> **Propósito**: Síntesis de mejores prácticas oficiales de Anthropic, OpenAI,
> y Google aplicadas al dominio de este agente. Sirve como referencia rápida
> y justificación de por qué el agente está diseñado así.
>
> **Qué hacer**: Adapta cada sección al dominio del agente. Incluye
> prácticas específicas del stack tecnológico. Elimina estas instrucciones.

---

## INSTRUCCIONES: Secciones obligatorias

### 1. Diseño de Agentes

```markdown
## 1. Diseño de Agentes

### Anthropic: Simplicidad deliberada
> "A simple, single-threaded master loop combined with disciplined tools and
> planning delivers controllable autonomy."
- Prefiere loops debuggeables sobre orquestación compleja.
- Usa TODO-based planning con reminder injection.

### OpenAI: Handoffs claros
- Define handoffs explícitos: qué agente transfiere a qué otro.
- Guardrails paralelos: validación de seguridad sin bloquear ejecución.
- Tracing por defecto: toda ejecución es observable.

### Google: Jerarquía explícita
- Root agent con `sub_agents` declarados.
- Blackboard pattern para estado compartido.
- A2A protocol para comunicación inter-framework.
```

### 2. Gestión de Contexto

```markdown
## 2. Gestión de Contexto

### Progressive Disclosure (MCP / Claude Code)
```
Sesión inicia: solo metadata de skills/tools.
↓
Skill triggered: carga SKILL.md completo.
↓
Referencia necesaria: carga archivo de referencia.
```

### Compresión de Contexto (Claude Code)
- A ~92% de context window, resume y archiva a memoria persistente.
- Usa markdown files para memoria a largo plazo.
- Grep/Glob sobre embeddings para navegación en vivo.
```

### 3. Seguridad

```markdown
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
- Todo tool input pasa por schema validation.
- Sanitizar paths antes de operaciones filesystem.
- Nunca pasar input de usuario directamente a shell sin escaping.
```

### 4. Calidad de Código Generado

```markdown
## 4. Calidad

### Checklist post-ejecución
- [ ] Tests existentes pasan.
- [ ] Nuevos tests cubren cambios.
- [ ] No hay warnings nuevos.
- [ ] Código sigue convenciones.
- [ ] Documentación actualizada.
- [ ] No hay secrets hardcodeados.

### Principios aplicables
- KISS, YAGNI, DRY, SOLID (adaptar al paradigma del agente)
```

### 5. Observabilidad

```markdown
## 5. Observabilidad

### Tracing
- Toda ejecución trazable (OpenTelemetry).
- Incluir: input, decisiones, tool calls, outputs, errores.

### Cost Tracking
- Monitorear tokens por agente y por tool.
- Downgradear modelo para tareas simples.
- Alertar si coste excede presupuesto.

### Session Storage
- Mirror de transcripts a storage externo.
- Posibilidad de resumir y reanudar sesiones.
```

### 6. Testing de Agentes

```markdown
## 6. Testing

### Estrategia
- **Unit tests**: Tools individuales con mocks.
- **Integration tests**: Flujos end-to-end con fixtures.
- **Evals**: Benchmarks de calidad (ej: SWE-bench).
- **Red teaming**: Probar límites de seguridad.

### Métricas
- Task success rate, mean turns to completion, token efficiency.
```

---

## INSTRUCCIONES: Prácticas específicas del dominio

Añade una sección con prácticas específicas del stack/lenguaje/framework
que use tu agente:

```markdown
## 7. Prácticas específicas de [dominio]

### [Tecnología 1]
- [Práctica específica 1]
- [Práctica específica 2]

### [Tecnología 2]
- [Práctica específica 1]
```

---

## REFERENCIAS

- **Claude Code Best Practices**: https://code.claude.com/docs/en/best-practices.md
- **OpenAI Agents SDK Guide**: https://openai.github.io/openai-agents-python/
- **Google ADK Docs**: https://google.github.io/adk-docs/
- **MCP Security Best Practices**: https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices.md
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **Clean Code (Robert C. Martin)**: https://www.oreilly.com/library/view/clean-code-a/9780136083238/
