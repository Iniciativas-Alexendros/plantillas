# tools/README.md · Playbook de contenido

> **Propósito**: Catálogo de herramientas disponibles para el agente.
> Documenta qué tools nativas y MCP tiene a disposición, cuándo usarlas,
> y cómo extenderlas con tools custom.
>
> **Qué hacer**: Completa el catálogo con las tools REALES que tu agente
> usará. Incluye ejemplos concretos de invocación. Elimina estas instrucciones.

---

## Filosofía de Tools

Basada en **MCP (Model Context Protocol)** de Anthropic y **Function Tools**
de OpenAI Agents SDK.

Las herramientas son la **interfaz entre el agente y el mundo externo**.
Cada tool debe ser:

1. **Bien documentada**: Descripción clara del propósito y comportamiento.
2. **Schema-validada**: Inputs y outputs con tipos definidos (JSON Schema / Pydantic).
3. **Idempotente cuando sea posible**: Mismo input → mismo output.
4. **Segura**: Validación de inputs, sandboxing de ejecución, timeouts.

> Referencia: [MCP Tools Spec](https://modelcontextprotocol.io/specification/2025-11-25/server/tools.md)

---

## SECCIÓN 1: Tools Nativas de Claude Code

Documenta cada tool que el agente tiene habilitada en `AGENT.md`.

### Template por tool nativa:

```markdown
### [Nombre de la tool]

**Propósito**: [Qué hace en 1 oración]
**Cuándo usar**: [Trigger específico]
**Parámetros clave**:
- `[param1]`: [Tipo] — [Descripción]
- `[param2]`: [Tipo] — [Descripción]
**Limitaciones**:
- [Límite 1]
- [Límite 2]
**Ejemplo de uso**:
```
[Tool call de ejemplo]
```
**Riesgo**: [Gray / Green / Amber / Red]
```

### Ejemplo completado:

```markdown
### Read

**Propósito**: Leer contenido de archivos del filesystem.
**Cuándo usar**: Antes de cualquier modificación. Siempre lee antes de tocar.
**Parámetros clave**:
- `path`: string — Ruta absoluta o relativa al archivo.
- `offset`: integer — Línea de inicio (opcional, default 1).
- `limit`: integer — Número de líneas a leer (opcional, default ~2000).
**Limitaciones**:
- Máximo ~2000 líneas por lectura. Para archivos grandes, usa offset+limit.
- No puede leer archivos binarios.
**Ejemplo de uso**:
```
Read(path="src/main.py", offset=1, limit=100)
```
**Riesgo**: Gray (solo lectura)
```

#### Tools nativas disponibles (completar las que apliquen):

| Tool | Riesgo | Propósito principal |
|------|--------|---------------------|
| Read | Gray | Leer archivos |
| Grep | Gray | Buscar patrones regex |
| Glob | Gray | Listar archivos por patrón |
| Edit | Amber | Modificar archivos (diff) |
| Write | Amber | Crear/sobrescribir archivos |
| Bash | Amber/Red | Ejecutar comandos shell |
| Agent | Green | Spawn subagentes |
| TodoWrite | Gray | Gestionar tareas |

---

## SECCIÓN 2: MCP Servers Configurados

Documenta cada servidor MCP configurado en `tools/mcp.json`.

### Template por MCP server:

```markdown
### [Nombre del server]

**Propósito**: [Qué capacidades añade al agente]
**Transporte**: [stdio | sse | http]
**Comando**: `[comando para lanzar]`
**Tools expuestas**:
| Tool | Input | Output | Cuándo usar |
|------|-------|--------|-------------|
| `[tool1]` | [schema] | [schema] | [trigger] |

**Configuración requerida**:
- [Variable de entorno o archivo necesario]

**Ejemplo de uso**:
```
[Tool call de ejemplo]
```
```

### Ejemplo completado:

```markdown
### github

**Propósito**: Integración con GitHub para PRs, issues, y repos.
**Transporte**: stdio
**Comando**: `npx -y @modelcontextprotocol/server-github`
**Tools expuestas**:
| Tool | Input | Output | Cuándo usar |
|------|-------|--------|-------------|
| `create_issue` | `{owner, repo, title, body}` | Issue creado | Reportar bugs encontrados |
| `get_pull_request` | `{owner, repo, number}` | PR details | Revisar PRs externos |
| `search_code` | `{query}` | Resultados de búsqueda | Encontrar ejemplos en GitHub |

**Configuración requerida**:
- `GITHUB_PERSONAL_ACCESS_TOKEN` con scopes: `repo`, `issues`, `pull_requests`

**Ejemplo de uso**:
```
github:create_issue({
  owner: "mi-org",
  repo: "mi-proyecto",
  title: "Bug: race condition en auth",
  body: "## Descripción\n..."
})
```
```

---

## SECCIÓN 3: Tools Custom

Espacio para documentar herramientas custom desarrolladas específicamente
para este agente.

### Cómo crear una tool custom:

1. **Implementa la función** en `tools/custom/` (Python o TypeScript).
2. **Documenta el docstring**: El docstring se usa como descripción de la tool.
3. **Define el schema**: Usa type hints (Python) o Zod (TypeScript).
4. **Registra en MCP**: Expón vía MCP SDK (`@tool` / `createSdkMcpServer`).

### Template de implementación (Python):

```python
# tools/custom/mi_tool.py

from agents import function_tool
from pydantic import BaseModel

class MiToolInput(BaseModel):
    parametro: str
    opcional: int = 10

class MiToolOutput(BaseModel):
    resultado: str
    procesado: int

@function_tool
def mi_tool(input: MiToolInput) -> MiToolOutput:
    """
    Descripción clara de qué hace la tool.
    Esta descripción aparece en el catálogo de tools del agente.

    Args:
        parametro: Descripción del parámetro obligatorio.
        opcional: Descripción del parámetro opcional (default: 10).

    Returns:
        Dict con resultado estructurado.
    """
    return MiToolOutput(
        resultado=input.parametro.upper(),
        procesado=input.opcional * 2
    )
```

### Template de implementación (TypeScript):

```typescript
// tools/custom/mi_tool.ts

import { functionTool } from "@anthropic-ai/agents";
import { z } from "zod";

const MiToolSchema = z.object({
  parametro: z.string().describe("Descripción del parámetro"),
  opcional: z.number().default(10).describe("Descripción opcional"),
});

export const miTool = functionTool({
  name: "mi_tool",
  description: "Descripción clara de qué hace la tool.",
  parameters: MiToolSchema,
  execute: async (input) => {
    return {
      resultado: input.parametro.toUpperCase(),
      procesado: input.opcional * 2,
    };
  },
});
```

---

## SECCIÓN 4: Escalado con Tool Search

Para agentes con >50 tools, habilitar **tool search**:

### Configuración:

```json
{
  "toolSearch": {
    "enabled": true,
    "maxToolsPerQuery": 10,
    "descriptionEmbeddingModel": "text-embedding-3-small"
  }
}
```

### Beneficios:
- **Menor consumo de contexto**: Solo las tools necesarias se cargan.
- **Mayor precisión**: Menos ruido = mejor selección de tool por el LLM.
- **Escalabilidad**: Agente puede tener cientos de tools sin degradación.

### Referencias:
- [Claude Code: Tool Search](https://code.claude.com/docs/en/agent-sdk/tool-search.md)
- [MCP: Client Best Practices](https://modelcontextprotocol.io/docs/develop/clients/client-best-practices.md)

---

## REFERENCIAS

- **MCP Tools Spec**: https://modelcontextprotocol.io/specification/2025-11-25/server/tools.md
  (Schema, errors, validation, pagination)
- **OpenAI Agents SDK: Tools**: https://openai.github.io/openai-agents-python/tools/
  (Function tools, hosted tools, agents as tools, Codex tool)
- **Claude Code: Custom Tools**: https://code.claude.com/docs/en/agent-sdk/custom-tools.md
  (In-process MCP servers, @tool decorator)
- **Claude Code: Tools Reference**: https://code.claude.com/docs/en/tools-reference.md
  (Comportamiento nativo de cada tool)
