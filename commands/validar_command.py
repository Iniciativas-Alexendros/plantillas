#!/usr/bin/env python3
"""
Validador de Commands Claude Code · v2.0.0 (canon-runtime alignment)

Acepta el formato single-file `<nombre-comando>.md` con frontmatter
(description + opcionales argument-hint, allowed-tools) + cuerpo en
secciones canon (Trigger, Instrucciones, Parámetros, Output esperado,
Restricciones, Referencias).

Uso:
    python validar_command.py commands/ejemplo_command.md
    python validar_command.py commands/ejemplo_command.md --strict
    python validar_command.py commands/plantilla_command.md

Compatibilidad: si se pasa un directorio (estructura legado), busca
`COMMAND.md` dentro y emite warning de migración pendiente.

Referencia:
    - Claude Code Commands: https://code.claude.com/docs/en/commands.md
"""

import argparse
import re
import sys
from pathlib import Path

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

FRONTMATTER_REQUIRED = ["description"]

VALID_TOOLS = {
    "Read", "Grep", "Glob", "Edit", "Write", "Bash",
    "Agent", "TodoWrite", "TaskCreate", "TaskUpdate", "TaskList",
    "WebFetch", "WebSearch", "NotebookEdit", "LSP",
}

REQUIRED_SECTIONS = [
    "## Trigger",
    "## Instrucciones",
    "## Parámetros",
    "## Output esperado",
    "## Restricciones",
    "## Referencias",
]

# Kebab-case estricto o nombres reservados para plantilla/ejemplo
KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")
NOMBRES_ESPECIALES = {"plantilla_command", "ejemplo_command"}

MIN_BYTES = 500
MAX_BYTES = 15_000


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDADOR
# ═══════════════════════════════════════════════════════════════════════════════

class CommandValidator(BaseValidator):
    """Validador para commands single-file (formato canon-runtime v2)."""

    def __init__(self, archivo: Path, strict: bool = False):
        # BaseValidator necesita un directorio; usamos el padre del archivo.
        super().__init__(archivo.parent, strict)
        self.archivo = archivo.resolve()
        self.es_plantilla = self.archivo.name.startswith("plantilla_")
        self.checks = [
            Check("formato",      self._check_formato),
            Check("frontmatter",  self._check_frontmatter),
            Check("allowed_tools",self._check_allowed_tools),
            Check("secciones",    self._check_secciones),
            Check("placeholders", self._check_placeholders),
            Check("longitud",     self._check_longitud),
            Check("slug_filename",self._check_slug_filename),
        ]

    # ──────────────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────────────

    def _frontmatter_data(self):
        """Extrae el frontmatter YAML como dict, o None si falla/no hay yaml."""
        if not HAS_YAML or not self.archivo.is_file():
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
        if not self.archivo.is_file():
            return ""
        content = self.archivo.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return content
        parts = content.split("---", 2)
        return parts[2] if len(parts) >= 3 else content

    def _rel(self, p: Path) -> str:
        """Override: devuelve ruta relativa al archivo, no al parent dir."""
        try:
            return str(p.relative_to(self.archivo.parent))
        except ValueError:
            return p.name

    # ──────────────────────────────────────────────────────────────────────
    # Checks
    # ──────────────────────────────────────────────────────────────────────

    def _check_formato(self):
        if not self.archivo.is_file():
            return [Resultado(Nivel.ERROR, "formato",
                              f"{self.archivo.name} no es un archivo")]
        if self.archivo.suffix != ".md":
            return [Resultado(Nivel.ERROR, "formato",
                              f"{self.archivo.name} no termina en .md")]
        return []

    def _check_frontmatter(self):
        if not self.archivo.is_file():
            return []
        # Usa el helper canónico de validadores/checks.py
        return check_yaml_frontmatter(self, self.archivo, FRONTMATTER_REQUIRED)

    def _check_allowed_tools(self):
        """Valida el campo opcional `allowed-tools` si está presente."""
        data = self._frontmatter_data()
        if not data or "allowed-tools" not in data:
            return []
        tools = data["allowed-tools"]
        if not isinstance(tools, list):
            return [Resultado(Nivel.ERROR, "allowed_tools",
                              "campo 'allowed-tools' debe ser una lista")]
        resultados = []
        for tool in tools:
            if not isinstance(tool, str):
                resultados.append(Resultado(Nivel.ERROR, "allowed_tools",
                                            f"tool inválido: {tool!r}"))
                continue
            base = tool.split("(")[0]
            if base not in VALID_TOOLS and not base.startswith("mcp__"):
                resultados.append(Resultado(Nivel.WARNING, "allowed_tools",
                                            f"tool '{tool}' no está en la lista canon"))
        return resultados

    def _check_secciones(self):
        """Verifica que todas las secciones canon están presentes."""
        cuerpo = self._cuerpo()
        resultados = []
        for seccion in REQUIRED_SECTIONS:
            if seccion not in cuerpo:
                resultados.append(Resultado(Nivel.ERROR, "secciones",
                                            f"falta sección obligatoria: '{seccion}'"))
        return resultados

    def _check_placeholders(self):
        """En plantillas, los placeholders son esperados y se omite el check."""
        if self.es_plantilla:
            return []
        cuerpo = self._cuerpo()
        cuerpo_limpio = self._extraer_fuera_codeblock(cuerpo)
        for pattern in self.PLACEHOLDER_PATTERNS:
            if pattern.search(cuerpo_limpio):
                return [Resultado(Nivel.WARNING, "placeholders",
                                  f"contiene placeholders sin rellenar "
                                  f"(patrón: {pattern.pattern})")]
        return []

    def _check_longitud(self):
        """Warning si el archivo es sospechosamente corto o muy largo."""
        if not self.archivo.is_file():
            return []
        size = self.archivo.stat().st_size
        resultados = []
        if size < MIN_BYTES:
            resultados.append(Resultado(Nivel.WARNING, "longitud",
                                        f"archivo demasiado corto ({size} bytes); "
                                        f"cuerpo del comando posiblemente incompleto"))
        elif size > MAX_BYTES:
            resultados.append(Resultado(Nivel.WARNING, "longitud",
                                        f"archivo demasiado largo ({size} bytes); "
                                        f"considera dividir en subcomandos"))
        return resultados

    def _check_slug_filename(self):
        """El nombre del archivo (sin .md) debe ser kebab-case o un nombre especial."""
        slug = self.archivo.stem  # nombre sin extensión
        if slug in NOMBRES_ESPECIALES:
            return []
        if not KEBAB_RE.match(slug):
            return [Resultado(Nivel.ERROR, "slug_filename",
                              f"nombre de archivo '{slug}' no es kebab-case "
                              f"(ej: test-cobertura, deploy, code-review)")]
        return []


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida un command Claude Code single-file (canon-runtime v2)."
    )
    parser.add_argument("ruta", help="Ruta al archivo .md del comando (o dir legado)")
    parser.add_argument("--strict", action="store_true",
                        help="Tratar warnings como errores (CI/CD)")
    args = parser.parse_args()

    ruta = Path(args.ruta).resolve()

    if not ruta.exists():
        print(f"❌ No existe: {ruta}")
        return 1

    # Compatibilidad legado: si se pasa un directorio, buscar COMMAND.md dentro
    if ruta.is_dir():
        legacy = ruta / "COMMAND.md"
        if not legacy.is_file():
            print(f"❌ Dir sin COMMAND.md: {ruta}")
            return 1
        print(f"⚠️  Modo legado: validando {legacy} "
              f"(migrar a single-file <nombre>.md)")
        archivo = legacy
    else:
        archivo = ruta

    validator = CommandValidator(archivo, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
