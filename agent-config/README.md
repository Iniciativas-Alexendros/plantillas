# agent-config · Configuración cross-platform para agentes IA

Módulo canónico que centraliza en una fuente YAML la configuración global para Claude Code, OpenCode, Devin y Windsurf/Cascade.

## Estructura

| Archivo                                  | Propósito                                                              |
| ---------------------------------------- | ---------------------------------------------------------------------- |
| `plantilla_agent_config.yaml`            | Fuente canónica de verdad. Edita solo este archivo.                    |
| `generar_agent_configs.py`               | Genera los artefactos de cada plataforma (actual).                     |
| `validar_agent_config.py`                | Valida la fuente, el generador y detecta drift en el ejemplo (actual). |
| `ejemplo_agent_config/`                  | Salidas generadas para las 4 plataformas.                              |
| `src/plantillas/agent_config/schema.py`  | Esquema Pydantic `AgentConfig` (Bloque 2).                             |
| `src/plantillas/agent_config/templates/` | Templates Jinja2 por target (Bloque 2).                                |

## Flujo de trabajo

### Actual

1. Modifica `plantilla_agent_config.yaml`.
2. Regenera el ejemplo:
   ```bash
   python generar_agent_configs.py --home ejemplo_agent_config
   ```
3. Valida:
   ```bash
   python validar_agent_config.py . --strict
   ```
4. Aplica a tu home (con backup):
   ```bash
   python generar_agent_configs.py --backup
   ```

### Bloque 2

1. Modifica `plantilla_agent_config.yaml`.
2. Sincroniza:
   ```bash
   plantillas sync agent-config --home ~ --backup
   ```
3. Valida:
   ```bash
   plantillas validate agent-config --strict
   ```

## Targets

- **Claude Code**: `~/.claude/CLAUDE.md`, `~/.claude/settings.json`, `~/.claude/.mcp.json`
- **OpenCode**: `~/AGENTS.md`
- **Devin**: `~/.config/devin/AGENTS.md`, `~/.config/devin/config.json`
- **Windsurf/Cascade**: `~/.codeium/windsurf/memories/global_rules.md`

## Esquema Pydantic (Bloque 2)

El YAML se carga en la clase `AgentConfig` de Pydantic v2, que valida:

- `metadata`: versión, idioma, descripción.
- `operator`: nombre, contacto, idioma, zona horaria.
- `style`: tono, extensión, idioma de respuesta.
- `models`: preferencias por defecto.
- `tooling`: tools permitidas, MCP servers, skills.
- `security`: reglas de secretos, permisos, `.env`.
- `hierarchy`: determinismo, reglas globales, memoria.
- `targets`: overrides específicos por plataforma.

## Templates Jinja2 (Bloque 2)

Cada target tiene un template `.j2` en `src/plantillas/agent_config/templates/`:

- `claude.md.j2` → `~/.claude/CLAUDE.md`
- `claude_settings.json.j2` → `~/.claude/settings.json`
- `claude_mcp.json.j2` → `~/.claude/mcp.json`
- `opencode.md.j2` → `~/AGENTS.md`
- `devin.md.j2` → `~/.config/devin/AGENTS.md`
- `windsurf.md.j2` → `~/.codeium/windsurf/memories/global_rules.md`

Añadir un nuevo target es crear un nuevo template y registrarlo en el generador.

## Notas

- `global_rules.md` tiene límite de ~6.000 caracteres en Windsurf; el generador avisa si se excede.
- No incluyas secretos en la fuente canónica; usa variables de entorno o `pass-cli`.
- El drift check falla si `ejemplo_agent_config/` no coincide con la generación actual.
- En el Bloque 2, el drift check se hace con tests de snapshot sin escribir en `$HOME`.
