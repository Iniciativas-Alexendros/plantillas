#!/usr/bin/env python3
"""
Validador de Mini-apps Claude Code · v1.0.0 (canon-runtime alignment)

Acepta `<slug>.md` single-file con frontmatter (name, description,
category, runtime, version, last_updated) + cuerpo en secciones canon
(Propósito, Cuándo usar, …). Cuando además existe `<slug>.html` adjunto,
hace checks ligeros sobre el HTML (no se inventa parser DOM completo).

Uso:
    python validar_miniapps.py miniapps/ejemplo_miniapps.md
    python validar_miniapps.py miniapps/ejemplo_miniapps.md --strict
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


FRONTMATTER_REQUIRED = ["name", "description", "category", "runtime", "version", "last_updated"]
VALID_CATEGORIES = {"dashboard", "explorer", "tool", "playbook"}
VALID_RUNTIMES = {"browser", "electron", "static"}

REQUIRED_SECTIONS = [
    "## Propósito",
    "## Cuándo usar",
]

KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[\w.]+)?$")
ISODATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class MiniappValidator(BaseValidator):
    def __init__(self, archivo: Path, strict: bool = False):
        super().__init__(archivo.parent, strict)
        self.archivo = archivo.resolve()
        self.es_plantilla = self.archivo.name.startswith("plantilla_")
        self.checks = [
            Check("formato", self._check_formato),
            Check("frontmatter", self._check_frontmatter),
            Check("category", self._check_category),
            Check("runtime", self._check_runtime),
            Check("version", self._check_version),
            Check("last_updated", self._check_last_updated),
            Check("name_kebab", self._check_name_kebab),
            Check("secciones", self._check_secciones),
            Check("placeholders", self._check_placeholders),
            Check("html_adjunto", self._check_html_adjunto),
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
            return [Resultado(Nivel.ERROR, "formato", f"{self.archivo.name} no es un archivo")]
        if self.archivo.suffix != ".md":
            return [Resultado(Nivel.ERROR, "formato", f"{self.archivo.name} no termina en .md")]
        return []

    def _check_frontmatter(self):
        if not self.archivo.is_file():
            return []
        return check_yaml_frontmatter(self, self.archivo, FRONTMATTER_REQUIRED)

    def _check_category(self):
        data = self._frontmatter_data()
        if not data or "category" not in data:
            return []
        cat = data["category"]
        if cat not in VALID_CATEGORIES:
            return [Resultado(Nivel.ERROR, "category",
                              f"category '{cat}' inválida (válidas: {sorted(VALID_CATEGORIES)})")]
        return []

    def _check_runtime(self):
        data = self._frontmatter_data()
        if not data or "runtime" not in data:
            return []
        rt = data["runtime"]
        if rt not in VALID_RUNTIMES:
            return [Resultado(Nivel.ERROR, "runtime",
                              f"runtime '{rt}' inválido (válidos: {sorted(VALID_RUNTIMES)})")]
        return []

    def _check_version(self):
        data = self._frontmatter_data()
        if not data or "version" not in data:
            return []
        v = str(data["version"])
        if not SEMVER_RE.match(v):
            return [Resultado(Nivel.WARNING, "version", f"version '{v}' no es SemVer (X.Y.Z)")]
        return []

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
                                  f"contiene placeholders sin rellenar (patrón: {pattern.pattern})")]
        return []

    def _check_html_adjunto(self):
        """Si existe <slug>.html junto al .md, comprueba que es single-file y no carga JS externo."""
        data = self._frontmatter_data()
        if not data or "name" not in data:
            return []
        name = data["name"]
        if not isinstance(name, str):
            return []
        html_path = self.archivo.parent / f"{name}.html"
        if not html_path.is_file():
            return []
        try:
            html = html_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return []
        resultados = []
        # JS externo sin SRI = anti-patrón
        if re.search(r"<script[^>]+src=['\"]https?://", html, re.IGNORECASE):
            if "integrity=" not in html:
                resultados.append(Resultado(Nivel.WARNING, "html_adjunto",
                                            f"{html_path.name} carga JS externo sin atributo 'integrity'"))
        # Embed de secretos
        if re.search(r"(sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9_]{36,})", html):
            resultados.append(Resultado(Nivel.ERROR, "html_adjunto",
                                        f"{html_path.name} contiene token/secret embebido"))
        return resultados


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida una mini-app Claude Code (single-file).")
    parser.add_argument("ruta", help="Ruta al archivo .md de la mini-app")
    parser.add_argument("--strict", action="store_true", help="Tratar warnings como errores")
    args = parser.parse_args()

    ruta = Path(args.ruta).resolve()
    if not ruta.exists():
        print(f"❌ No existe: {ruta}")
        return 1
    if ruta.is_dir():
        # Convención: dir contiene plantilla_<dir>.md o ejemplo_<dir>.md
        candidatos = list(ruta.glob("*.md"))
        if not candidatos:
            print(f"❌ Dir sin .md dentro: {ruta}")
            return 1
        archivo = candidatos[0]
    else:
        archivo = ruta

    validator = MiniappValidator(archivo, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
