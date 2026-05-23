#!/usr/bin/env python3
"""
Validador de Cuadernos Claude Code · v1.0.0 (canon-runtime alignment)

Un cuaderno es una nota estructurada del operador con anclaje semántico:
idea, log, decisión o playbook. Acepta `<slug>.md` single-file con
frontmatter (name, description, kind, tags, last_updated, status) +
cuerpo con secciones obligatorias (## Contexto, ## Contenido, ## Referencias)
y secciones recomendadas según `kind`.

Uso:
    python validar_cuadernos.py cuadernos/ejemplo_cuadernos.md
    python validar_cuadernos.py cuadernos/ejemplo_cuadernos.md --strict
    python validar_cuadernos.py cuadernos/plantilla_cuadernos.md
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


# ──────────────────────────────────────────────────────────────────────────
# Constantes
# ──────────────────────────────────────────────────────────────────────────

FRONTMATTER_REQUIRED = [
    "name",
    "description",
    "kind",
    "tags",
    "last_updated",
    "status",
]

VALID_KINDS = {"idea", "log", "decision", "playbook"}
VALID_STATUSES = {"draft", "active", "archived"}

# Secciones obligatorias → ERROR si faltan
REQUIRED_SECTIONS = [
    "## Contexto",
    "## Contenido",
    "## Referencias",
]

# Secciones recomendadas por kind → WARNING si faltan
RECOMMENDED_SECTIONS: dict[str, list[str]] = {
    "idea": ["## Hipótesis", "## Próximos pasos"],
    "log": ["## Eventos"],
    "decision": ["## Decisión", "## Alternativas consideradas", "## Consecuencias"],
    "playbook": ["## Pasos", "## Cuándo aplicar"],
}

KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")
ISODATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TAG_KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")


# ──────────────────────────────────────────────────────────────────────────
# CuadernoValidator
# ──────────────────────────────────────────────────────────────────────────

class CuadernoValidator(BaseValidator):
    def __init__(self, archivo: Path, strict: bool = False):
        # BaseValidator requiere un directorio; pasamos el directorio padre
        super().__init__(archivo.parent, strict)
        self.archivo = archivo.resolve()
        self.es_plantilla = self.archivo.name.startswith("plantilla_")
        self.checks = [
            Check("formato", self._check_formato),
            Check("frontmatter", self._check_frontmatter),
            Check("kind", self._check_kind),
            Check("status", self._check_status),
            Check("tags", self._check_tags),
            Check("last_updated", self._check_last_updated),
            Check("name_kebab", self._check_name_kebab),
            Check("secciones_obligatorias", self._check_secciones_obligatorias),
            Check("secciones_recomendadas", self._check_secciones_recomendadas),
            Check("placeholders", self._check_placeholders),
        ]

    # ───────── helpers ─────────

    def _frontmatter_data(self) -> dict | None:
        """Parsea y devuelve el frontmatter YAML, o None si no disponible."""
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
        """Devuelve el cuerpo del cuaderno (sin frontmatter)."""
        if not self.archivo.is_file():
            return ""
        content = self.archivo.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return content
        parts = content.split("---", 2)
        return parts[2] if len(parts) >= 3 else content

    # ───────── checks ─────────

    def _check_formato(self) -> list[Resultado]:
        if not self.archivo.is_file():
            return [Resultado(Nivel.ERROR, "formato",
                              f"{self.archivo.name} no es un archivo")]
        if self.archivo.suffix != ".md":
            return [Resultado(Nivel.ERROR, "formato",
                              f"{self.archivo.name} no termina en .md")]
        return []

    def _check_frontmatter(self) -> list[Resultado]:
        if not self.archivo.is_file():
            return []
        return check_yaml_frontmatter(self, self.archivo, FRONTMATTER_REQUIRED)

    def _check_kind(self) -> list[Resultado]:
        data = self._frontmatter_data()
        if not data or "kind" not in data:
            return []
        kind = data["kind"]
        if kind not in VALID_KINDS:
            return [Resultado(Nivel.ERROR, "kind",
                              f"kind '{kind}' inválido "
                              f"(válidos: {sorted(VALID_KINDS)})")]
        return []

    def _check_status(self) -> list[Resultado]:
        data = self._frontmatter_data()
        if not data or "status" not in data:
            return []
        status = data["status"]
        if status not in VALID_STATUSES:
            return [Resultado(Nivel.ERROR, "status",
                              f"status '{status}' inválido "
                              f"(válidos: {sorted(VALID_STATUSES)})")]
        return []

    def _check_tags(self) -> list[Resultado]:
        data = self._frontmatter_data()
        if not data:
            return []
        if "tags" not in data:
            return []
        tags = data["tags"]

        # Si pyyaml no está disponible, degradar a warning
        if not HAS_YAML:
            return [Resultado(Nivel.WARNING, "tags",
                              "No se puede validar 'tags' sin pyyaml")]

        if not isinstance(tags, list) or len(tags) == 0:
            return [Resultado(Nivel.ERROR, "tags",
                              "tags debe ser una lista no vacía")]

        resultados = []
        for tag in tags:
            if not isinstance(tag, str):
                resultados.append(Resultado(Nivel.ERROR, "tags",
                                            f"tag inválido (no es string): {tag!r}"))
            elif len(tag) < 2:
                resultados.append(Resultado(Nivel.ERROR, "tags",
                                            f"tag demasiado corto (mín. 2 chars): '{tag}'"))
            elif not TAG_KEBAB_RE.match(tag):
                resultados.append(Resultado(Nivel.ERROR, "tags",
                                            f"tag no es kebab-case: '{tag}' "
                                            f"(patrón: ^[a-z0-9][a-z0-9-]*[a-z0-9]$)"))
        return resultados

    def _check_last_updated(self) -> list[Resultado]:
        data = self._frontmatter_data()
        if not data or "last_updated" not in data:
            return []
        d = str(data["last_updated"])
        if not ISODATE_RE.match(d):
            return [Resultado(Nivel.ERROR, "last_updated",
                              f"last_updated '{d}' no es ISO-8601 (YYYY-MM-DD)")]
        return []

    def _check_name_kebab(self) -> list[Resultado]:
        data = self._frontmatter_data()
        if not data or "name" not in data:
            return []
        name = data["name"]
        if not isinstance(name, str) or not KEBAB_RE.match(name):
            nivel = Nivel.WARNING if self.es_plantilla else Nivel.ERROR
            return [Resultado(nivel, "name_kebab",
                              f"name '{name}' no es kebab-case"
                              + (" (esperado en plantilla)" if self.es_plantilla else ""))]
        return []

    def _check_secciones_obligatorias(self) -> list[Resultado]:
        """ERROR si falta alguna de las 3 secciones obligatorias."""
        cuerpo = self._cuerpo()
        resultados = []
        for seccion in REQUIRED_SECTIONS:
            if seccion not in cuerpo:
                resultados.append(Resultado(Nivel.ERROR, "secciones_obligatorias",
                                            f"falta sección obligatoria: '{seccion}'"))
        return resultados

    def _check_secciones_recomendadas(self) -> list[Resultado]:
        """WARNING si faltan secciones recomendadas según el kind."""
        data = self._frontmatter_data()
        if not data or "kind" not in data:
            return []
        kind = data["kind"]
        if kind not in VALID_KINDS:
            return []

        cuerpo = self._cuerpo()
        recomendadas = RECOMMENDED_SECTIONS.get(kind, [])
        resultados = []
        for seccion in recomendadas:
            if seccion not in cuerpo:
                resultados.append(Resultado(Nivel.WARNING, "secciones_recomendadas",
                                            f"sección recomendada para kind='{kind}' ausente: "
                                            f"'{seccion}'"))
        return resultados

    def _check_placeholders(self) -> list[Resultado]:
        """WARNING si el cuaderno (no plantilla) contiene placeholders sin rellenar."""
        if self.es_plantilla:
            return []
        cuerpo = self._extraer_fuera_codeblock(self._cuerpo())
        # Placeholders en MAYÚSCULAS-CON-GUIONES característicos de plantillas
        patron_upper = re.compile(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+){1,}\b")
        for pattern in self.PLACEHOLDER_PATTERNS:
            if pattern.search(cuerpo):
                return [Resultado(Nivel.WARNING, "placeholders",
                                  f"contiene placeholders sin rellenar "
                                  f"(patrón: {pattern.pattern})")]
        if patron_upper.search(cuerpo):
            return [Resultado(Nivel.WARNING, "placeholders",
                              "contiene texto en MAYÚSCULAS-CON-GUIONES "
                              "(posibles placeholders sin rellenar)")]
        return []


# ──────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida un cuaderno Claude Code (single-file .md)."
    )
    parser.add_argument("ruta", help="Ruta al archivo .md del cuaderno")
    parser.add_argument(
        "--strict", action="store_true",
        help="Tratar warnings como errores"
    )
    args = parser.parse_args()

    ruta = Path(args.ruta).resolve()

    if not ruta.exists():
        print(f"❌ No existe: {ruta}")
        return 1

    # Modo legado: si recibe directorio, buscar primer .md y warning
    if ruta.is_dir():
        candidatos = sorted(ruta.glob("*.md"))
        if not candidatos:
            print(f"❌ Directorio sin archivos .md: {ruta}")
            return 1
        archivo = candidatos[0]
        print(f"⚠️  Se recibió un directorio; usando primer .md encontrado: {archivo.name}")
        print("   Considera pasar la ruta del archivo directamente.")
    else:
        archivo = ruta

    validator = CuadernoValidator(archivo, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
