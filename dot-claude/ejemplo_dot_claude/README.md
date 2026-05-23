# Alexendros · `.claude/`

> Ejemplo de configuración global de Claude Code para el usuario Alexendros.

## Estructura

```
.claude/
├── CLAUDE.md              ← Instrucciones globales (norma, maestrías, doctrinas)
├── settings.json          ← Configuración técnica (permisos, hooks, env)
├── mcp.json               ← Servidores MCP globales
├── README.md              ← Este archivo
│
├── agents/                ← Agentes especializados globales
├── skills/                ← Skills reutilizables globales
├── commands/              ← Comandos slash personalizados
├── hooks/                 ← Hooks de interceptación globales
├── scripts/               ← Scripts de utilidad personal
├── plugins/               ← Plugins de extensión
├── mcp/                   ← Configuración adicional de servidores MCP
├── miniapps/              ← Mini-aplicaciones HTML/SPA
├── autoresearch/          ← Investigaciones automáticas
├── cuadernos/             ← Cuadernos de trabajo
├── knowledge/             ← Base de conocimiento
├── artefactos/            ← Outputs entregados al operador
└── projects/              ← Memoria por proyecto
```

## Uso

Esta configuración se aplica automáticamente al iniciar Claude Code.
No requiere activación manual.

## Personalización

1. Edita `CLAUDE.md` para cambiar doctrinas y maestrías.
2. Edita `settings.json` para ajustar permisos, hooks y variables de entorno.
3. Edita `mcp.json` para añadir o quitar servidores MCP.
4. Añade skills en `skills/` para capacidades reutilizables.
5. Añade agentes en `agents/` para especialistas.

## Referencias

- [Claude Code Directory Structure](https://code.claude.com/docs/en/claude-directory.md)
- [Claude Code Memory & CLAUDE.md](https://code.claude.com/docs/en/memory.md)
- [Claude Code Settings](https://code.claude.com/docs/en/settings.md)
