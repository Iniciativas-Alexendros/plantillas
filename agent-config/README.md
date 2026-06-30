# agent-config · Configuración cross-platform para agentes IA

Módulo canónico que centraliza en una fuente YAML la configuración global para Claude Code, OpenCode, Devin y Windsurf/Cascade.

## Estructura

| Archivo | Propósito |
|---|---|
| `plantilla_agent_config.yaml` | Fuente canónica de verdad. Edita solo este archivo. |
| `generar_agent_configs.py` | Genera los artefactos de cada plataforma. |
| `validar_agent_config.py` | Valida la fuente, el generador y detecta drift en el ejemplo. |
| `ejemplo_agent_config/` | Salidas generadas para las 4 plataformas. |

## Flujo de trabajo

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

## Targets

- **Claude Code**: `~/.claude/CLAUDE.md`, `~/.claude/settings.json`, `~/.claude/.mcp.json`
- **OpenCode**: `~/AGENTS.md`
- **Devin**: `~/.config/devin/AGENTS.md`, `~/.config/devin/config.json`
- **Windsurf/Cascade**: `~/.codeium/windsurf/memories/global_rules.md`

## Notas

- `global_rules.md` tiene límite de ~6.000 caracteres en Windsurf; el generador avisa si se excede.
- No incluyas secretos en la fuente canónica; usa variables de entorno o `pass-cli`.
- El drift check falla si `ejemplo_agent_config/` no coincide con la generación actual.
