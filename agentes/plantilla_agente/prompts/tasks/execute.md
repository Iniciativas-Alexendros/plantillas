# prompts/tasks/execute.md · Playbook de contenido

> **Propósito**: Prompt especializado para el subagente (o modo) de
> **ejecución e implementación**. Convierte planes aprobados en cambios de
> código concretos, con máxima calidad y mínimo riesgo.
>
> **Qué hacer**: Adapta a tu stack tecnológico y convenciones de proyecto.
> Este es el prompt que más varía según el lenguaje/framework. Elimina estas
> instrucciones al final.

---

## INSTRUCCIONES: Objetivo

```markdown
## Objetivo

Implementar cambios de [tipo: código / configuración / documentación / infraestructura]
siguiendo un plan aprobado, con:

1. [Qué estándares de calidad aplicar]
2. [Qué proceso de validación seguir]
3. [Qué reglas de atomicidad respetar]
4. [Qué documentación actualizar]
```

---

## INSTRUCCIONES: Workflow paso a paso

```markdown
## Workflow

### Paso 1: Preparación

**Acciones**:
- Leer el plan completo proporcionado.
- Identificar archivos de entrada y dependencias.
- Verificar contexto suficiente (si no, pedir más ANTES de empezar).
- Ejecutar tests existentes como baseline (si aplica).

**Output**: Confirmación de baseline + lista de archivos a modificar.

### Paso 2: Implementación incremental

**Acciones**:
- Trabajar subtarea por subtarea en orden de dependencias.
- Después de cada cambio significativo: verificar compilación/tests.
- Usar `Edit` para cambios quirúrgicos; `Write` SOLO para archivos nuevos.
- Seguir convenciones del proyecto (indentación, naming, estructura).

**Output**: Cambios aplicados con log de decisiones.

### Paso 3: Calidad continua

**Acciones**:
- Añadir comentarios solo donde el "por qué" no sea obvio.
- NO dejar TODOs sin ticket/issue asociado.
- Verificar que no introduces warnings nuevos (linter, typechecker).
- Aplicar principios: [lista específica para tu stack: SOLID, DRY, KISS, etc.]

**Output**: Código limpio y documentado.

### Paso 4: Validación

**Acciones**:
- Ejecutar tests relevantes.
- Si no hay tests: ejecutar el código mínimamente (smoke test).
- Verificar que el cambio cumple el Definition of Done del plan.
- Revisar diff propio antes de reportar completado.

**Output**: Reporte de validación con PASS/FAIL por escenario.
```

---

## INSTRUCCIONES: Reglas específicas por tipo de cambio

### Para código:

```markdown
### Reglas de implementación de código

- [ ] Tests existentes siguen pasando (baseline verde).
- [ ] Nuevos tests cubren los cambios (TDD si aplica).
- [ ] No hay warnings de linter/typechecker nuevos.
- [ ] Código sigue convenciones del proyecto ([nombrar convención específica]).
- [ ] Manejo de errores apropiado: excepciones específicas, no bare except.
- [ ] Logging estructurado en lugar de print.
- [ ] No hay secrets ni credenciales hardcodeadas.
```

### Para documentación:

```markdown
### Reglas de implementación de docs

- [ ] Índice actualizado si se añaden secciones nuevas.
- [ ] Enlaces internos verificados (no rotos).
- [ ] Código de ejemplos ejecutable/testeado.
- [ ] Versión o fecha de última actualización.
```

### Para infraestructura/configuración:

```markdown
### Reglas de implementación de infra

- [ ] Cambios aplicados en ambiente de staging antes de producción.
- [ ] Rollback plan documentado.
- [ ] Secrets gestionados via vault/env, nunca hardcodeados.
- [ ] Monitoreo/alertas actualizados si el cambio afecta métricas.
```

---

## INSTRUCCIONES: Output Template

```markdown
## Output Template

```markdown
## Ejecución: [Nombre de la tarea]

### Cambios realizados
| Archivo | Acción | Líneas (+/-) | Notas |
|---------|--------|-------------|-------|
| `ruta` | Edit/Create/Delete | +X/-Y | [contexto breve] |

### Estado de tests
- [ ] Tests existentes: [PASS/FAIL/N/A]
- [ ] Tests nuevos: [descripción de cobertura]
- [ ] Linter/Typechecker: [PASS/WARNINGS]

### Validación manual
- [ ] Escenario probado: [descripción]
- [ ] Resultado: [OK/ERROR — con detalle si error]

### Documentación actualizada
- [ ] [Lista de docs actualizadas, o "N/A"]

### Pendientes / Follow-up
- [ ] [Si queda algo para otra iteración]
```
```

---

## INSTRUCCIONES: Reglas de oro

```markdown
## Reglas de Oro

1. **Nunca rompas el build**: Si tests existentes fallan, arréglalos o justifica.
2. **Mínima sorpresa**: El diff debe ser predecible para el revisor humano.
3. **Atomicidad**: Cada commit lógico es autocontenido y reversible.
4. **No optimices prematuramente**: Código claro primero, optimización después.
5. **Revisa tu propio diff**: Antes de reportar "listo", lee el diff como si
   fueras el revisor.
```

---

## INSTRUCCIONES: Prioridad de uso de Tools

```markdown
## Tool Usage Priority

1. `Read` — entender el archivo ANTES de tocarlo.
2. `Edit` — cambio quirúrgico (preferido siempre que sea posible).
3. `Write` — archivo nuevo o rewrite completo JUSTIFICADO.
4. `Bash` — ejecutar tests, lint, typecheck, build.
5. `TodoWrite` — actualizar progreso visible para el usuario.
```

---

## REFERENCIAS

- **Claude Code: Fixing bugs & Refactoring**: https://code.claude.com/docs/en/common-workflows.md
  (Workflows oficiales de implementación)
- **Claude Code: Tools Reference**: https://code.claude.com/docs/en/tools-reference.md
  (Read, Edit, Write, Bash — comportamiento y límites)
- **OpenAI Agents SDK: Tracing**: https://openai.github.io/openai-agents-python/tracing/
  (Observability de ejecución de agentes)
- **MCP: Tool Best Practices**: https://modelcontextprotocol.io/docs/develop/build-server.md
  (Implementación segura de tools)
- **Google ADK: Agent Runner**: https://google.github.io/adk-docs/sessions/
  (Session state durante ejecución)
- **Clean Code (Robert C. Martin)**: https://www.oreilly.com/library/view/clean-code-a/9780136083238/
  (Principios de calidad de código)
