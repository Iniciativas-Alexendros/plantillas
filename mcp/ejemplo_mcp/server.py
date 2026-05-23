#!/usr/bin/env python3
"""
MCP Server Ejemplo: Utils
Expone tools de utilidad: timestamp y clima simulado.

Uso:
    python server.py

Configuración en mcp.json:
    {
      "mcpServers": {
        "utils": {
          "command": "python",
          "args": ["/ruta/a/server.py"]
        }
      }
    }
"""

from datetime import datetime
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("utils")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_timestamp",
            description="Devuelve la fecha y hora actual en formato ISO",
            inputSchema={
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "description": "Formato de fecha (iso, human, unix)",
                        "enum": ["iso", "human", "unix"],
                        "default": "iso"
                    }
                }
            }
        ),
        Tool(
            name="get_weather",
            description="Devuelve el clima simulado para una ciudad",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Nombre de la ciudad",
                        "default": "Madrid"
                    },
                    "units": {
                        "type": "string",
                        "description": "Unidades de temperatura (celsius, fahrenheit)",
                        "enum": ["celsius", "fahrenheit"],
                        "default": "celsius"
                    }
                },
                "required": ["city"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_timestamp":
        fmt = arguments.get("format", "iso")
        now = datetime.now()

        if fmt == "iso":
            text = now.isoformat()
        elif fmt == "human":
            text = now.strftime("%Y-%m-%d %H:%M:%S")
        elif fmt == "unix":
            text = str(int(now.timestamp()))
        else:
            raise ValueError(f"Formato no soportado: {fmt}")

        return [TextContent(type="text", text=text)]

    if name == "get_weather":
        city = arguments.get("city", "Madrid")
        units = arguments.get("units", "celsius")

        # Simulación determinista basada en hash del nombre
        import hashlib
        h = int(hashlib.md5(city.lower().encode()).hexdigest(), 16)
        temp_c = 5 + (h % 30)  # 5°C a 35°C
        conditions = ["Soleado", "Nublado", "Lluvia ligera", "Parcialmente nublado"]
        condition = conditions[h % len(conditions)]
        humidity = 30 + (h % 50)

        if units == "fahrenheit":
            temp = temp_c * 9 // 5 + 32
            unit_symbol = "°F"
        else:
            temp = temp_c
            unit_symbol = "°C"

        text = (
            f"Clima en {city}: {condition}\n"
            f"Temperatura: {temp}{unit_symbol}\n"
            f"Humedad: {humidity}%"
        )
        return [TextContent(type="text", text=text)]

    raise ValueError(f"Tool desconocida: {name}")


if __name__ == "__main__":
    app.run(transport="stdio")
