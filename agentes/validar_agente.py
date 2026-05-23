#!/usr/bin/env python3
"""
Validador de Agentes Claude Code · v3.0.0 (canon-runtime alignment)

Acepta el formato single-file `<nombre-agente>.md` con frontmatter
runtime (name, description, tools, model) + cuerpo en secciones canon
(System, Persona, Tasks, Tools MCP, Memory, Subagents, References).

Uso:
    python validar_agente.py agentes/ejemplo_agente.md
    python validar_agente.py agentes/ejemplo_agente.md --strict
    python validar_agente.py ~/.claude/agents/code-reviewer.md --strict

Compatibilidad: si se pasa un directorio (estructura legado), se valida
buscando `AGENT.md` dentro y se emite warning indicando migración pendiente.

Referencia:
    - Claude Code Subagents: https://code.claude.com/docs/en/sub-agents.md
    - MCP Spec: https://modelcontextprotocol.io/specification/
"""

import argparse
import sys
from pathlib import Path

# Motor de validación reusable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validadores import (
    BaseValidator,
    Check,
    Resultado,
    Nivel,
    check_yaml_frontmatter,
)

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

FRONTMATTER_REQUIRED = ["name", "description", "tools", "model"]
FRONTMATTER_OPTIONAL = ["effort", "permission_scope", "primary_skill", "skills"]

VALID_MODELS = {"opus", "sonnet", "haiku", "opusplan"}

VALID_TOOLS = {
    "Read", "Grep", "Glob", "Edit", "Write", "Bash",
    "Agent", "TodoWrite", "TaskCreate", "TaskUpdate", "TaskList",
    "WebFetch", "WebSearch", "NotebookEdit", "LSP",
}

REQUIRED_SECTIONS = [
    "## System",
    "## Persona",
    "## Tasks",
    "## Tools MCP",
    "## Memory",
    "## Subagents",
    "## References",
]

KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDADOR
# ═══════════════════════════════════════════════════════════════════════════════

class AgentValidator(BaseValidator):
    """Validador para agentes single-file (formato canon-runtime)."""

    def __init__(self, archivo: Path, strict: bool = False):
        # Usamos el directorio padre como `ruta` para reusar helpers de BaseValidator
        # pero todos los checks operan sobre `self.archivo`.
        super().__init__(archivo.parent, strict)
        self.archivo = archivo.resolve()
        self.es_plantilla = self.archivo.name.startswith("plantilla_")
        self.checks = [
            Check("formato", self._check_formato),
            Check("frontmatter", self._check_frontmatter),
            Check("modelo", self._check_modelo),
            Check("tools", self._check_tools),
            Check("name_kebab", self._check_name_kebab),
            Check("secciones", self._check_secciones),
            Check("placeholders", self._check_placeholders),
            Check("longitud", self._check_longitud),
        ]

    # ──────────────────────────────────────────────────────────────────────

    def _rel_archivo(self) -> str:
        try:
            return str(self.archivo.relative_to(self.ruta))
        except ValueError:
            return self.archivo.name

    def _frontmatter_data(self):
        """Extrae el frontmatter YAML como dict, o None si falla."""
        if not HAS_YAML:
            return None
        content = self.archivo.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return None
        parts = content.split("---", 2)
        if len(parts) < 3:
            return None
        try:
            data = yaml.safe_load(parts[1])
            return data if isinstance(data, dict) else None
        except Exception:
            return None

    def _cuerpo(self) -> str:
        """Devuelve el cuerpo del archivo sin el frontmatter."""
        content = self.archivo.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return content
        parts = content.split("---", 2)
        return parts[2] if len(parts) >= 3 else content

    # ──────────────────────────────────────────────────────────────────────
    # Checks
    # ──────────────────────────────────────────────────────────────────────

    def _check_formato(self):
        if not self.archivo.is_file():
            return [Resultado(Nivel.ERROR, "formato",
                              f"{self._rel_archivo()} no es un archivo")]
        if self.archivo.suffix != ".md":
            return [Resultado(Nivel.ERROR, "formato",
                              f"{self._rel_archivo()} no termina en .md")]
        return []

    def _check_frontmatter(self):
        if not self.archivo.is_file():
            return []
        return check_yaml_frontmatter(self, self.archivo, FRONTMATTER_REQUIRED)

    def _check_modelo(self):
        data = self._frontmatter_data()
        if not data or "model" not in data:
            return []
        model = data["model"]
        if model not in VALID_MODELS:
            return [Resultado(Nivel.WARNING, "modelo",
                              f"model '{model}' no reconocido (válidos: {sorted(VALID_MODELS)})")]
        return []

    def _check_tools(self):
        data = self._frontmatter_data()
        if not data or "tools" not in data:
            return []
        tools = data["tools"]
        if not isinstance(tools, list):
            return [Resultado(Nivel.ERROR, "tools",
                              "campo 'tools' debe ser una lista")]
        resultados = []
        for tool in tools:
            if not isinstance(tool, str):
                resultados.append(Resultado(Nivel.ERROR, "tools",
                                            f"tool inválido: {tool!r}"))
                continue
            base = tool.split("(")[0]  # acepta Bash(git:*) etc
            if base not in VALID_TOOLS and not base.startswith("mcp__"):
                resultados.append(Resultado(Nivel.WARNING, "tools",
                                            f"tool '{tool}' no está en la lista canon"))
        return resultados

    def _check_name_kebab(self):
        data = self._frontmatter_data()
        if not data or "name" not in data:
            return []
        name = data["name"]
        if not isinstance(name, str) or not KEBAB_RE.match(name):
            # Plantillas usan placeholders en MAYÚSCULAS → solo warning
            nivel = Nivel.WARNING if self.es_plantilla else Nivel.ERROR
            return [Resultado(nivel, "name_kebab",
                              f"name '{name}' no es kebab-case válido"
                              + (" (esperado en plantilla)" if self.es_plantilla else ""))]
        # Verificar que el filename coincide con el name (excepto plantilla/ejemplo)
        expected = f"{name}.md"
        if self.archivo.name not in (expected, "plantilla_agente.md", "ejemplo_agente.md"):
            return [Resultado(Nivel.WARNING, "name_kebab",
                              f"archivo '{self.archivo.name}' no coincide con name '{name}'")]
        return []

    def _check_secciones(self):
        cuerpo = self._cuerpo()
        resultados = []
        for seccion in REQUIRED_SECTIONS:
            if seccion not in cuerpo:
                resultados.append(Resultado(Nivel.ERROR, "secciones",
                                            f"falta sección obligatoria: '{seccion}'"))
        return resultados

    def _check_placeholders(self):
        # En plantillas, los placeholders son esperados; se omite el check.
        if self.es_plantilla:
            return []
        cuerpo = self._cuerpo()
        cuerpo_sin_codeblock = self._extraer_fuera_codeblock(cuerpo)
        resultados = []
        for pattern in self.PLACEHOLDER_PATTERNS:
            if pattern.search(cuerpo_sin_codeblock):
                resultados.append(Resultado(Nivel.WARNING, "placeholders",
                                            f"contiene placeholders sin rellenar (patrón: {pattern.pattern})"))
                break
        return resultados

    def _check_longitud(self):
        size = self.archivo.stat().st_size
        if size < 800:
            return [Resultado(Nivel.WARNING, "longitud",
                              f"archivo demasiado corto ({size} bytes); cuerpo del agente posiblemente incompleto")]
        if size > 30_000:
            return [Resultado(Nivel.WARNING, "longitud",
                              f"archivo demasiado largo ({size} bytes); considera dividir en subagentes")]
        return []


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida un agente Claude Code single-file (canon-runtime)."
    )
    parser.add_argument("ruta", help="Ruta al archivo .md del agente (o dir legado)")
    parser.add_argument("--strict", action="store_true",
                        help="Tratar warnings como errores (CI/CD)")
    args = parser.parse_args()

    ruta = Path(args.ruta).resolve()
    if not ruta.exists():
        print(f"❌ No existe: {ruta}")
        return 1

    # Compatibilidad legado: si es dir, buscar AGENT.md dentro
    if ruta.is_dir():
        legacy = ruta / "AGENT.md"
        if not legacy.is_file():
            print(f"❌ Dir sin AGENT.md: {ruta}")
            return 1
        print(f"⚠️  Modo legado: validando {legacy} (migrar a single-file)")
        archivo = legacy
    else:
        archivo = ruta

    validator = AgentValidator(archivo, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
