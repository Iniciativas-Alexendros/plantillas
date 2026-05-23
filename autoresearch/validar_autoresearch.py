#!/usr/bin/env python3
"""
Validador de artículos de Auto-investigación (autoresearch) · v1.0.0 (canon-runtime alignment)

Acepta `<slug>.md` single-file con frontmatter (name, description, topic,
sources, status, last_updated, confidence) + cuerpo en secciones canon
(Pregunta, Fuentes, Hallazgos, Veredicto, Pendientes).

Uso:
    python validar_autoresearch.py autoresearch/ejemplo_autoresearch.md
    python validar_autoresearch.py autoresearch/ejemplo_autoresearch.md --strict
    python validar_autoresearch.py autoresearch/  # modo legado: busca primer .md
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


FRONTMATTER_REQUIRED = [
    "name", "description", "topic", "sources",
    "status", "last_updated", "confidence",
]

VALID_STATUSES = {"draft", "review", "published", "archived"}

# status que requieren al menos 1 source
STATUSES_REQUIRE_SOURCES = {"review", "published"}

REQUIRED_SECTIONS = [
    "## Pregunta",
    "## Fuentes",
    "## Hallazgos",
    "## Veredicto",
    "## Pendientes",
]

KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")
ISODATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL_RE = re.compile(r"^https?://\S+|^/\S+")


class AutoresearchValidator(BaseValidator):
    def __init__(self, archivo: Path, strict: bool = False):
        super().__init__(archivo.parent, strict)
        self.archivo = archivo.resolve()
        self.es_plantilla = self.archivo.name.startswith("plantilla_")
        self.checks = [
            Check("formato", self._check_formato),
            Check("frontmatter", self._check_frontmatter),
            Check("status", self._check_status),
            Check("confidence", self._check_confidence),
            Check("sources", self._check_sources),
            Check("last_updated", self._check_last_updated),
            Check("name_kebab", self._check_name_kebab),
            Check("secciones", self._check_secciones),
            Check("placeholders", self._check_placeholders),
            Check("coherencia_sources", self._check_coherencia_sources),
        ]

    # ───────── helpers ─────────

    def _frontmatter_data(self):
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
        if not self.archivo.is_file():
            return ""
        content = self.archivo.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return content
        parts = content.split("---", 2)
        return parts[2] if len(parts) >= 3 else content

    # ───────── checks ─────────

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
        return check_yaml_frontmatter(self, self.archivo, FRONTMATTER_REQUIRED)

    def _check_status(self):
        data = self._frontmatter_data()
        if not data or "status" not in data:
            return []
        st = data["status"]
        if not isinstance(st, str) or st not in VALID_STATUSES:
            return [Resultado(Nivel.ERROR, "status",
                              f"status '{st}' inválido "
                              f"(válidos: {sorted(VALID_STATUSES)})")]
        return []

    def _check_confidence(self):
        data = self._frontmatter_data()
        if not data or "confidence" not in data:
            return []
        c = data["confidence"]
        try:
            c_float = float(c)
        except (TypeError, ValueError):
            return [Resultado(Nivel.ERROR, "confidence",
                              f"confidence '{c}' no es un número")]
        if not (0.0 <= c_float <= 1.0):
            return [Resultado(Nivel.ERROR, "confidence",
                              f"confidence '{c_float}' fuera del rango 0.0–1.0")]
        return []

    def _check_sources(self):
        data = self._frontmatter_data()
        if not data or "sources" not in data:
            return []
        sources = data["sources"]
        resultados = []

        if not isinstance(sources, list):
            return [Resultado(Nivel.ERROR, "sources",
                              "sources debe ser una lista YAML")]

        # Cada elemento debe ser string con esquema http(s) o ruta absoluta
        for i, src in enumerate(sources):
            if not isinstance(src, str):
                resultados.append(Resultado(Nivel.WARNING, "sources",
                                            f"sources[{i}] no es string: {src!r}"))
            elif not URL_RE.match(src.strip()):
                resultados.append(Resultado(Nivel.WARNING, "sources",
                                            f"sources[{i}] no parece URL ni ruta: {src!r}"))

        # Si status es review/published, necesita al menos 1 source
        st = data.get("status", "draft")
        if st in STATUSES_REQUIRE_SOURCES and len(sources) == 0:
            resultados.append(Resultado(Nivel.ERROR, "sources",
                                        f"status '{st}' requiere al menos 1 source en la lista"))

        return resultados

    def _check_last_updated(self):
        data = self._frontmatter_data()
        if not data or "last_updated" not in data:
            return []
        d = str(data["last_updated"])
        if not ISODATE_RE.match(d):
            return [Resultado(Nivel.WARNING, "last_updated",
                              f"last_updated '{d}' no es ISO-8601 (YYYY-MM-DD)")]
        return []

    def _check_name_kebab(self):
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

    def _check_secciones(self):
        cuerpo = self._cuerpo()
        resultados = []
        for seccion in REQUIRED_SECTIONS:
            if seccion not in cuerpo:
                resultados.append(Resultado(Nivel.ERROR, "secciones",
                                            f"falta sección obligatoria: '{seccion}'"))
        return resultados

    def _check_placeholders(self):
        if self.es_plantilla:
            return []
        cuerpo = self._extraer_fuera_codeblock(self._cuerpo())
        for pattern in self.PLACEHOLDER_PATTERNS:
            if pattern.search(cuerpo):
                return [Resultado(Nivel.WARNING, "placeholders",
                                  f"contiene placeholders sin rellenar "
                                  f"(patrón: {pattern.pattern})")]
        # Detectar placeholders MAYUSCULA-CON-GUION propios de este módulo
        if re.search(r"\b[A-Z][A-Z0-9]*(?:-[A-Z][A-Z0-9]*)+\b", cuerpo):
            return [Resultado(Nivel.WARNING, "placeholders",
                              "contiene tokens MAYUSCULA-CON-GUION sin reemplazar")]
        return []

    def _check_coherencia_sources(self):
        """
        Warning si la sección ## Fuentes no menciona alguna URL del frontmatter sources:.
        """
        data = self._frontmatter_data()
        if not data:
            return []
        sources = data.get("sources", [])
        if not isinstance(sources, list) or len(sources) == 0:
            return []

        cuerpo = self._cuerpo()
        # Extraer el bloque de ## Fuentes hasta el siguiente ##
        match = re.search(r"## Fuentes(.*?)(?=\n## |\Z)", cuerpo, re.DOTALL)
        if not match:
            return []
        bloque_fuentes = match.group(1)

        resultados = []
        for src in sources:
            if not isinstance(src, str):
                continue
            # Extraer dominio o path significativo para la búsqueda
            src_clean = src.strip()
            # Buscar la URL (o al menos el dominio) en el bloque
            if src_clean not in bloque_fuentes:
                # Intento con dominio extraído
                domain_match = re.search(r"https?://([^/]+)", src_clean)
                if domain_match:
                    domain = domain_match.group(1)
                    if domain not in bloque_fuentes:
                        resultados.append(
                            Resultado(Nivel.WARNING, "coherencia_sources",
                                      f"La sección ## Fuentes no menciona: {src_clean!r}"))
                else:
                    resultados.append(
                        Resultado(Nivel.WARNING, "coherencia_sources",
                                  f"La sección ## Fuentes no menciona: {src_clean!r}"))
        return resultados


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida un cuaderno de auto-investigación Claude Code (single-file)."
    )
    parser.add_argument("ruta", help="Ruta al archivo .md del cuaderno")
    parser.add_argument("--strict", action="store_true",
                        help="Tratar warnings como errores")
    args = parser.parse_args()

    ruta = Path(args.ruta).resolve()
    if not ruta.exists():
        print(f"No existe: {ruta}")
        return 1

    if ruta.is_dir():
        # Modo legado: buscar primer .md dentro del directorio
        candidatos = sorted(ruta.glob("*.md"))
        if not candidatos:
            print(f"Dir sin .md dentro: {ruta}")
            return 1
        archivo = candidatos[0]
        print(f"⚠️  Modo legado: validando {archivo.name} (migrar a single-file)")
    else:
        archivo = ruta

    validator = AutoresearchValidator(archivo, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
