#!/usr/bin/env python3
"""
Validador de configuraciones dot-claude · v2.0.0 (canon-runtime alignment)

Verifica que un directorio que materializa `.claude/` (global o por proyecto)
cumpla con el schema runtime real de Claude Code 2.1.x:

  - Estructura de archivos requeridos (CLAUDE.md, settings.json, mcp.json, README.md)
  - settings.json con schema canon-runtime (permissions + hooks; sin claves legado)
  - mcp.json con estructura {mcpServers: {...}}
  - CLAUDE.md sin referencias a 'herramientas/' (árbol plano post-reforma)
  - Detección de placeholders sin rellenar (skipped en plantilla_dot_claude)

Uso:
    python dot-claude/validar_dot_claude.py dot-claude/ejemplo_dot_claude --strict
    python dot-claude/validar_dot_claude.py dot-claude/plantilla_dot_claude
    python dot-claude/validar_dot_claude.py ~/.claude
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validadores import (
    BaseValidator,
    Check,
    Resultado,
    Nivel,
    check_placeholders,
)


# ═══════════════════════════════════════════════════════════════════════════
# Configuración
# ═══════════════════════════════════════════════════════════════════════════

REQUIRED_FILES = ["CLAUDE.md", "settings.json", "mcp.json", "README.md"]

# Claves de settings.json que el runtime NO interpreta (legado / inventadas)
SETTINGS_CLAVES_LEGADO = [
    "skillListingBudgetFraction",
    "hooks.enabled",
    "hooks.sources",
    "hooks.autoDiscover",
    "skills.autoDiscover",
    "skills.preload",
    "mcp.servers",
    "output.language",
    "output.style",
]

# Eventos hook canónicos del runtime Claude Code 2.1.x.
VALID_EVENTOS_HOOK = {
    "PreToolUse",
    "PostToolUse",
    "SessionStart",
    "SessionEnd",
    "UserPromptSubmit",
    "Stop",
    "Notification",
    "PreCompact",
}


# ═══════════════════════════════════════════════════════════════════════════
# Validador
# ═══════════════════════════════════════════════════════════════════════════

class DotClaudeValidator(BaseValidator):
    """
    Validador para directorios que materializan .claude/ (global o proyecto).
    Acepta tanto 'plantilla_dot_claude' como 'ejemplo_dot_claude' o un .claude/ real.
    """

    def __init__(self, dot_dir: Path, strict: bool = False):
        super().__init__(dot_dir, strict)
        self.es_plantilla = self.ruta.name == "plantilla_dot_claude"
        self.checks = [
            Check("estructura", self._check_estructura),
            Check("settings_json", self._check_settings_json),
            Check("mcp_json", self._check_mcp_json),
            Check("settings_no_legado", self._check_settings_no_legado),
            Check("claude_md_arbol_plano", self._check_claude_md_arbol_plano),
            Check("placeholders", self._check_placeholders),
        ]

    # ──────────────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────────────

    def _load_json(self, nombre: str):
        """Carga y devuelve el contenido de un JSON del directorio, o None si falla."""
        p = self.ruta / nombre
        if not p.is_file():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None

    # ──────────────────────────────────────────────────────────────────────
    # Checks
    # ──────────────────────────────────────────────────────────────────────

    def _check_estructura(self):
        """Verifica que existan los archivos requeridos."""
        resultados = []
        for f in REQUIRED_FILES:
            p = self.ruta / f
            if not p.is_file():
                resultados.append(Resultado(
                    Nivel.ERROR, "estructura",
                    f"Falta archivo obligatorio: {f}",
                    f,
                ))
        if not resultados:
            resultados.append(Resultado(
                Nivel.OK, "estructura",
                f"Archivos requeridos presentes: {', '.join(REQUIRED_FILES)}",
            ))
        return resultados

    def _check_settings_json(self):
        """
        Valida el schema runtime de settings.json:
          - JSON parseable
          - Top-level dict
          - Contiene 'permissions' y 'hooks'
          - permissions.allow y permissions.deny son listas de strings
          - hooks es dict cuyo valor es lista de {matcher, hooks: [{type, command}]}
        """
        resultados = []
        p = self.ruta / "settings.json"
        if not p.is_file():
            return resultados  # _check_estructura ya lo reporta

        data = self._load_settings_json(p, resultados)
        if data is None:
            return resultados

        resultados.extend(self._validate_permissions(data))
        resultados.extend(self._validate_hooks(data))

        if not resultados:
            resultados.append(Resultado(
                Nivel.OK, "settings_json",
                "settings.json válido (schema canon-runtime)",
                "settings.json",
            ))
        return resultados

    def _load_settings_json(self, p: Path, resultados: list):
        """Carga settings.json; si falla, añade errores y devuelve None."""
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            resultados.append(Resultado(
                Nivel.ERROR, "settings_json",
                f"settings.json JSON inválido: {e}",
                "settings.json",
            ))
            return None

        if not isinstance(data, dict):
            resultados.append(Resultado(
                Nivel.ERROR, "settings_json",
                "settings.json debe ser un objeto JSON (dict)",
                "settings.json",
            ))
            return None
        return data

    def _validate_permissions(self, data: dict):
        """Valida la sección 'permissions' de settings.json."""
        resultados = []
        if "permissions" not in data:
            resultados.append(Resultado(
                Nivel.ERROR, "settings_json",
                "settings.json falta clave 'permissions'",
                "settings.json",
            ))
            return resultados

        perms = data["permissions"]
        if not isinstance(perms, dict):
            resultados.append(Resultado(
                Nivel.ERROR, "settings_json",
                "'permissions' debe ser un objeto",
                "settings.json",
            ))
            return resultados

        for campo in ("allow", "deny"):
            if campo not in perms:
                resultados.append(Resultado(
                    Nivel.ERROR, "settings_json",
                    f"'permissions' falta campo '{campo}'",
                    "settings.json",
                ))
                continue
            if not isinstance(perms[campo], list):
                resultados.append(Resultado(
                    Nivel.ERROR, "settings_json",
                    f"'permissions.{campo}' debe ser una lista",
                    "settings.json",
                ))
                continue
            for item in perms[campo]:
                if not isinstance(item, str):
                    resultados.append(Resultado(
                        Nivel.ERROR, "settings_json",
                        f"'permissions.{campo}' contiene un elemento no-string: {item!r}",
                        "settings.json",
                    ))
                    break
        return resultados

    def _validate_hooks(self, data: dict):
        """Valida la sección 'hooks' de settings.json."""
        resultados = []
        if "hooks" not in data:
            resultados.append(Resultado(
                Nivel.ERROR, "settings_json",
                "settings.json falta clave 'hooks'",
                "settings.json",
            ))
            return resultados

        hooks = data["hooks"]
        if not isinstance(hooks, dict):
            resultados.append(Resultado(
                Nivel.ERROR, "settings_json",
                "'hooks' debe ser un objeto (dict con eventos como claves)",
                "settings.json",
            ))
            return resultados

        for evento, entradas in hooks.items():
            if evento not in VALID_EVENTOS_HOOK:
                resultados.append(Resultado(
                    Nivel.WARNING, "settings_json",
                    f"'hooks.{evento}' no es un evento reconocido por el runtime "
                    f"(válidos: {sorted(VALID_EVENTOS_HOOK)})",
                    "settings.json",
                ))
            resultados.extend(self._validate_hook_event(evento, entradas))
        return resultados

    def _validate_hook_event(self, evento: str, entradas):
        """Valida una lista de entradas para un evento de hooks."""
        resultados = []
        if not isinstance(entradas, list):
            resultados.append(Resultado(
                Nivel.ERROR, "settings_json",
                f"'hooks.{evento}' debe ser una lista",
                "settings.json",
            ))
            return resultados

        for i, entrada in enumerate(entradas):
            if not isinstance(entrada, dict):
                resultados.append(Resultado(
                    Nivel.ERROR, "settings_json",
                    f"'hooks.{evento}[{i}]' debe ser un objeto",
                    "settings.json",
                ))
                continue
            resultados.extend(self._validate_hook_entry(evento, i, entrada))
        return resultados

    def _validate_hook_entry(self, evento: str, i: int, entrada: dict):
        """Valida una entrada {matcher, hooks: [...]} de un evento."""
        resultados = []
        if "matcher" not in entrada:
            resultados.append(Resultado(
                Nivel.ERROR, "settings_json",
                f"'hooks.{evento}[{i}]' falta 'matcher'",
                "settings.json",
            ))
        if "hooks" not in entrada or not isinstance(entrada["hooks"], list):
            resultados.append(Resultado(
                Nivel.ERROR, "settings_json",
                f"'hooks.{evento}[{i}]' falta 'hooks' (lista)",
                "settings.json",
            ))
            return resultados

        for j, h in enumerate(entrada["hooks"]):
            resultados.extend(self._validate_hook_command(evento, i, j, h))
        return resultados

    def _validate_hook_command(self, evento: str, i: int, j: int, h):
        """Valida un comando {type, command} dentro de hooks."""
        resultados = []
        if not isinstance(h, dict):
            resultados.append(Resultado(
                Nivel.ERROR, "settings_json",
                f"'hooks.{evento}[{i}].hooks[{j}]' debe ser un objeto",
                "settings.json",
            ))
            return resultados

        if h.get("type") != "command":
            resultados.append(Resultado(
                Nivel.ERROR, "settings_json",
                f"'hooks.{evento}[{i}].hooks[{j}].type' debe ser 'command'",
                "settings.json",
            ))
        cmd = h.get("command", "")
        if not isinstance(cmd, str) or not cmd.strip():
            resultados.append(Resultado(
                Nivel.ERROR, "settings_json",
                f"'hooks.{evento}[{i}].hooks[{j}].command' debe ser string no vacío",
                "settings.json",
            ))
        return resultados

    def _check_mcp_json(self):
        """Valida que mcp.json tenga la estructura {mcpServers: {...}}."""
        resultados = []
        p = self.ruta / "mcp.json"
        if not p.is_file():
            return resultados  # _check_estructura ya lo reporta

        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            resultados.append(Resultado(
                Nivel.ERROR, "mcp_json",
                f"mcp.json JSON inválido: {e}",
                "mcp.json",
            ))
            return resultados

        if not isinstance(data, dict):
            resultados.append(Resultado(
                Nivel.ERROR, "mcp_json",
                "mcp.json debe ser un objeto JSON",
                "mcp.json",
            ))
            return resultados

        if "mcpServers" not in data:
            resultados.append(Resultado(
                Nivel.ERROR, "mcp_json",
                "mcp.json debe tener clave raíz 'mcpServers'",
                "mcp.json",
            ))
        elif not isinstance(data["mcpServers"], dict):
            resultados.append(Resultado(
                Nivel.ERROR, "mcp_json",
                "'mcpServers' debe ser un objeto",
                "mcp.json",
            ))
        else:
            resultados.append(Resultado(
                Nivel.OK, "mcp_json",
                f"mcp.json válido ({len(data['mcpServers'])} servidor(es))",
                "mcp.json",
            ))
        return resultados

    def _check_settings_no_legado(self):
        """Detecta claves obsoletas (legado) en settings.json y emite WARNING."""
        resultados = []
        p = self.ruta / "settings.json"
        if not p.is_file():
            return resultados

        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return resultados  # _check_settings_json ya lo reporta

        if not isinstance(data, dict):
            return resultados

        encontradas = []

        # Claves top-level
        TOP_LEVEL_LEGADO = {
            "skillListingBudgetFraction",
            "skills",
            "output",
        }
        for clave in TOP_LEVEL_LEGADO:
            if clave in data:
                encontradas.append(clave)

        # Claves anidadas: hooks.enabled, hooks.sources, hooks.autoDiscover
        if "hooks" in data and isinstance(data["hooks"], dict):
            hooks_dict = data["hooks"]
            for sub in ("enabled", "sources", "autoDiscover"):
                if sub in hooks_dict:
                    encontradas.append(f"hooks.{sub}")

        # mcp.servers (dentro del settings, no el mcp.json separado)
        if "mcp" in data and isinstance(data["mcp"], dict):
            if "servers" in data["mcp"]:
                encontradas.append("mcp.servers")

        if encontradas:
            for clave in encontradas:
                resultados.append(Resultado(
                    Nivel.WARNING, "settings_no_legado",
                    f"Clave obsoleta en settings.json: '{clave}' — el runtime la ignora",
                    "settings.json",
                ))
        else:
            resultados.append(Resultado(
                Nivel.OK, "settings_no_legado",
                "Sin claves legado en settings.json",
                "settings.json",
            ))
        return resultados

    def _check_claude_md_arbol_plano(self):
        """Emite WARNING si CLAUDE.md menciona 'herramientas/' (árbol pre-reforma)."""
        resultados = []
        p = self.ruta / "CLAUDE.md"
        if not p.is_file():
            return resultados

        content = p.read_text(encoding="utf-8")
        # Buscar fuera de codeblocks para evitar falsos positivos en ejemplos
        content_sin_code = self._extraer_fuera_codeblock(content)

        if "herramientas/" in content_sin_code:
            resultados.append(Resultado(
                Nivel.WARNING, "claude_md_arbol_plano",
                "CLAUDE.md menciona 'herramientas/' — usar árbol plano post-reforma",
                "CLAUDE.md",
            ))
        else:
            resultados.append(Resultado(
                Nivel.OK, "claude_md_arbol_plano",
                "CLAUDE.md no menciona 'herramientas/' (árbol plano OK)",
                "CLAUDE.md",
            ))
        return resultados

    def _check_placeholders(self):
        """
        Busca placeholders sin rellenar en todos los archivos del directorio.
        Se salta el check si estamos validando plantilla_dot_claude.
        """
        if self.es_plantilla:
            return [Resultado(
                Nivel.OK, "placeholders",
                "Skipped: plantilla_dot_claude (placeholders son esperados)",
            )]
        return check_placeholders(
            self,
            extensiones=(".json", ".md", ".yaml", ".yml", ".txt", ".sh"),
        )


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida un directorio de configuración .claude/ (canon-runtime)."
    )
    parser.add_argument(
        "ruta",
        help="Directorio a validar (plantilla_dot_claude, ejemplo_dot_claude, o ~/.claude)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Tratar warnings como errores (para CI/CD)",
    )
    args = parser.parse_args()

    ruta = Path(args.ruta).resolve()
    if not ruta.exists():
        print(f"No existe: {ruta}")
        return 1
    if not ruta.is_dir():
        print(f"No es un directorio: {ruta}")
        return 1

    validator = DotClaudeValidator(ruta, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
