# [Nombre del Entorno] · `.claude/`

> Configuración global de Claude Code para [tu nombre/organización]

## Estructura

```
.claude/
├── CLAUDE.md              ← Instrucciones globales (norma, maestrías, doctrinas)
├── settings.json          ← Configuración técnica (permisos, hooks, skills)
├── mcp.json               ← Servidores MCP globales
├── README.md              ← Este archivo
│
├── agents/                ← Agentes especializados globales
├── skills/                ← Skills reutilizables globales
├── commands/              ← Comandos slash personalizados
├── hooks/                 ← Hooks de interceptación globales
├── plugins/               ← Plugins de extensión
├── scripts/               ← Scripts de utilidad personal
├── plantillas/            ← Plantillas personales
│
├── projects/              ← Memoria por proyecto
├── logs/                  ← Logs de sesiones
├── jobs/                  ← Jobs en background
├── uploads/               ← Archivos temporales
├── sessions/              ← Sesiones persistentes
├── state/                 ← Estado interno
│
├── cache/                 ← Cache (symlink → logs/runtime/cache)
├── daemon/                ← Configuración del daemon
├── runtime/               ← Datos de runtime
├── file-history/          ← Historial de archivos
├── paste-cache/           ← Cache de clipboard
├── session-env/           ← Variables de entorno por sesión
├── shell-snapshots/       ← Snapshots de shell
├── plans/                 ← Planes en curso
└── tasks/                 ← Tareas programadas
```

## Uso

Esta configuración se aplica automáticamente al iniciar Claude Code.
No requiere activación manual.

## Personalización

1. Edita `CLAUDE.md` para cambiar doctrinas y maestrías.
2. Edita `settings.json` para ajustar permisos y comportamiento.
3. Añade skills en `skills/` para capacidades reutilizables.
4. Añade agentes en `agents/` para especialistas.

## Referencias

- [Claude Code Directory Structure](https://code.claude.com/docs/en/claude-directory.md)
