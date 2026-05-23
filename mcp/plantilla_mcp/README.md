# MCP Server · Playbook de contenido

> **Propósito**: Los servidores MCP (Model Context Protocol) exponen tools,
> resources, y prompts a los agentes de Claude Code. Son la interfaz
> estandarizada entre el agente y el mundo externo.
>
> **Qué hacer**: Define la estructura del servidor MCP, sus tools, y cómo
> se conecta a Claude Code. Elimina estas instrucciones.

---

## INSTRUCCIONES: Estructura del proyecto

```
[nombre-mcp-server]/
├── README.md             ← Documentación
├── pyproject.toml        ← Config Python (si es Python)
│   o package.json        ← Config Node (si es TypeScript)
│
├── src/
│   ├── server.py         ← Punto de entrada del servidor
│   ├── tools/            ← Implementación de tools
│   │   └── [tool].py
│   ├── resources/        ← Implementación de resources
│   │   └── [resource].py
│   └── prompts/          ← Prompts pre-definidos
│       └── [prompt].py
│
└── tests/                ← Tests del servidor
    └── test_server.py
```

---

## INSTRUCCIONES: Implementación mínima (Python)

```python
# src/server.py
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("[nombre-del-server]")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="mi_tool",
            description="Descripción de qué hace esta tool",
            inputSchema={
                "type": "object",
                "properties": {
                    "parametro": {
                        "type": "string",
                        "description": "Descripción del parámetro"
                    }
                },
                "required": ["parametro"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "mi_tool":
        resultado = procesar(arguments["parametro"])
        return [TextContent(type="text", text=resultado)]
    raise ValueError(f"Tool desconocida: {name}")

if __name__ == "__main__":
    app.run(transport="stdio")
```

---

## INSTRUCCIONES: Configuración en Claude Code

Añade el servidor a `mcp.json`:

```json
{
  "mcpServers": {
    "[nombre-del-server]": {
      "command": "python",
      "args": ["/ruta/al/server/src/server.py"],
      "env": {
        "[VARIABLE]": "${VALOR}"
      }
    }
  }
}
```

---

## INSTRUCCIONES: Testing

```python
# tests/test_server.py
import pytest
from src.server import app

@pytest.mark.asyncio
async def test_mi_tool():
    result = await app.call_tool("mi_tool", {"parametro": "test"})
    assert len(result) == 1
    assert "test" in result[0].text
```

---

## REFERENCIAS

- **MCP: Build a Server**: https://modelcontextprotocol.io/docs/develop/build-server.md
- **MCP: Tools Spec**: https://modelcontextprotocol.io/specification/2025-11-25/server/tools.md
- **MCP: Resources Spec**: https://modelcontextprotocol.io/specification/2025-11-25/server/resources.md
- **MCP: Python SDK**: https://github.com/modelcontextprotocol/python-sdk
