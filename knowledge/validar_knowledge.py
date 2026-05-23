#!/usr/bin/env python3
"""
Validador de artículos KB (Knowledge) · v1.0.0 (canon-runtime alignment)

Acepta `<slug>.md` single-file con frontmatter canon (name, description,
domain, references, status, last_updated, authority) + cuerpo en secciones
obligatorias (Resumen, Contenido, Aplicación, Limitaciones, Referencias).

Uso:
    python knowledge/validar_knowledge.py knowledge/ejemplo_knowledge.md
    python knowledge/validar_knowledge.py knowledge/ejemplo_knowledge.md --strict
    python knowledge/validar_knowledge.py knowledge/plantilla_knowledge.md
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
# Constantes canónicas
# ──────────────────────────────────────────────────────────────────────────

FRONTMATTER_REQUIRED = [
    "name",
    "description",
    "domain",
    "references",
    "status",
    "last_updated",
    "authority",
]

VALID_STATUSES = {"draft", "review", "published", "deprecated"}
VALID_AUTHORITIES = {"official", "community", "inferred"}

REQUIRED_SECTIONS = [
    "## Resumen",
    "## Contenido",
    "## Aplicación",
    "## Limitaciones",
    "## Referencias",
]

KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")
ISODATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Umbral mínimo de coherencia: al menos esta fracción de references del
# frontmatter deben aparecer como substring en la sección ## Referencias.
COHERENCIA_UMBRAL = 0.5


class KnowledgeValidator(BaseValidator):
    def __init__(self, archivo: Path, strict: bool = False):
        super().__init__(archivo.parent, strict)
        self.archivo = archivo.resolve()
        self.es_plantilla = self.archivo.name.startswith("plantilla_")
        self.checks = [
            Check("formato", self._check_formato),
            Check("frontmatter", self._check_frontmatter),
            Check("status", self._check_status),
            Check("authority", self._check_authority),
            Check("domain", self._check_domain),
            Check("references", self._check_references),
            Check("related_skills", self._check_related_skills),
            Check("last_updated", self._check_last_updated),
            Check("name_kebab", self._check_name_kebab),
            Check("secciones", self._check_secciones),
            Check("coherencia_referencias", self._check_coherencia_referencias),
            Check("placeholders", self._check_placeholders),
            Check("deprecated_status", self._check_deprecated_status),
        ]

    # ───────── helpers ─────────

    def _frontmatter_data(self):
        if not self.archivo.is_file():
            return None
        content = self.archivo.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return None
        parts = content.split("---", 2)
        if len(parts) < 3:
            return None
        if not HAS_YAML:
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

    def _seccion_referencias(self) -> str:
        """Extrae el texto de la sección ## Referencias del cuerpo."""
        cuerpo = self._cuerpo()
        # Busca desde ## Referencias hasta el siguiente ## (o fin)
        match = re.search(r"## Referencias\n([\s\S]*?)(?=\n## |\Z)", cuerpo)
        if match:
            return match.group(1)
        return ""

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
        if st not in VALID_STATUSES:
            return [Resultado(Nivel.ERROR, "status",
                              f"status '{st}' inválido (válidos: {sorted(VALID_STATUSES)})")]
        return []

    def _check_authority(self):
        data = self._frontmatter_data()
        if not data or "authority" not in data:
            return []
        auth = data["authority"]
        if auth not in VALID_AUTHORITIES:
            return [Resultado(Nivel.ERROR, "authority",
                              f"authority '{auth}' inválida "
                              f"(válidas: {sorted(VALID_AUTHORITIES)})")]
        return []

    def _check_domain(self):
        data = self._frontmatter_data()
        if not data or "domain" not in data:
            return []
        domain = str(data["domain"])
        if not KEBAB_RE.match(domain):
            nivel = Nivel.WARNING if self.es_plantilla else Nivel.ERROR
            return [Resultado(nivel, "domain",
                              f"domain '{domain}' no es kebab-case "
                              f"(solo minúsculas, dígitos y guiones; min 2 chars)"
                              + (" (esperado en plantilla)" if self.es_plantilla else ""))]
        return []

    def _check_references(self):
        data = self._frontmatter_data()
        if not data or "references" not in data:
            return []
        refs = data["references"]
        status = data.get("status", "draft")

        if not isinstance(refs, list):
            return [Resultado(Nivel.ERROR, "references",
                              "references debe ser una lista YAML")]

        if len(refs) == 0:
            if status == "published":
                return [Resultado(Nivel.ERROR, "references",
                                  "status 'published' requiere al menos 1 reference")]
            else:
                return [Resultado(Nivel.WARNING, "references",
                                  f"references vacío en status '{status}' "
                                  f"(recomendado añadir fuentes antes de publicar)")]
        return []

    def _check_related_skills(self):
        data = self._frontmatter_data()
        if not data or "related_skills" not in data:
            return []
        skills = data["related_skills"]
        if not isinstance(skills, list):
            return [Resultado(Nivel.ERROR, "related_skills",
                              "related_skills debe ser una lista YAML")]
        resultados = []
        for skill in skills:
            if not isinstance(skill, str):
                resultados.append(Resultado(Nivel.WARNING, "related_skills",
                                            f"related_skills: elemento '{skill}' no es string"))
                continue
            # Skills pueden tener mayúsculas (ej. CREA_playground) — validamos
            # que sean identificadores razonables: solo alnum, _ y -
            if not re.match(r"^[A-Za-z0-9][A-Za-z0-9_-]*$", skill):
                resultados.append(Resultado(Nivel.WARNING, "related_skills",
                                            f"related_skills: '{skill}' contiene caracteres inesperados"))
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

    def _check_coherencia_referencias(self):
        """
        Warning si ## Referencias no menciona suficiente texto de references:.
        Heurística: al menos COHERENCIA_UMBRAL (50%) de las referencias del
        frontmatter aparecen como substring en la sección ## Referencias.
        """
        data = self._frontmatter_data()
        if not data or "references" not in data:
            return []
        refs = data.get("references", [])
        if not isinstance(refs, list) or len(refs) == 0:
            return []

        seccion = self._seccion_referencias()
        if not seccion:
            # Si la sección no existe, _check_secciones ya lo reporta
            return []

        encontradas = 0
        for ref in refs:
            if not isinstance(ref, str):
                continue
            # Buscar alguna parte significativa: URL o texto de al menos 10 chars
            fragmento = ref.strip()
            # Intentar con la URL si existe
            url_match = re.search(r"https?://\S+", fragmento)
            if url_match:
                if url_match.group(0) in seccion:
                    encontradas += 1
                    continue
            # Si no, buscar el texto completo o una parte suficiente (30+ chars)
            if fragmento in seccion:
                encontradas += 1
            elif len(fragmento) > 30 and fragmento[:30] in seccion:
                encontradas += 1

        cobertura = encontradas / len(refs) if refs else 1.0
        if cobertura < COHERENCIA_UMBRAL:
            return [Resultado(Nivel.WARNING, "coherencia_referencias",
                              f"Sección '## Referencias' cubre solo {encontradas}/{len(refs)} "
                              f"referencias del frontmatter "
                              f"({cobertura:.0%} < umbral {COHERENCIA_UMBRAL:.0%}). "
                              f"Verificar que las URLs/textos del frontmatter aparezcan en la sección.")]
        return []

    def _check_placeholders(self):
        if self.es_plantilla:
            return []
        cuerpo = self._extraer_fuera_codeblock(self._cuerpo())
        # Patrones propios de knowledge además de los heredados de BaseValidator
        knowledge_patterns = [
            re.compile(r"\bNOMBRE-KB-KEBAB\b"),
            re.compile(r"\bDOMINIO-KEBAB\b"),
            re.compile(r"\bRESUMEN-DEL-CONTENIDO\b"),
            re.compile(r"\bCONTENIDO-DETALLADO\b"),
            re.compile(r"\bFUENTE-[0-9]+\b"),
            re.compile(r"\bLIMITACIÓN-[0-9]+\b"),
            re.compile(r"\bDISPARADOR-[0-9]+\b"),
            re.compile(r"\bANTI-PATRÓN-[0-9]+\b"),
        ]
        all_patterns = list(self.PLACEHOLDER_PATTERNS) + knowledge_patterns
        for pattern in all_patterns:
            if pattern.search(cuerpo):
                return [Resultado(Nivel.WARNING, "placeholders",
                                  f"contiene placeholders sin rellenar "
                                  f"(patrón: {pattern.pattern})")]
        return []

    def _check_deprecated_status(self):
        """
        Warning explícito cuando status == 'deprecated'.
        No es un error (el artículo sigue siendo válido), pero el validador
        lo señala para que el operador sea consciente de que valida contenido obsoleto.
        """
        data = self._frontmatter_data()
        if not data:
            return []
        if data.get("status") == "deprecated":
            return [Resultado(Nivel.WARNING, "deprecated_status",
                              f"El artículo '{data.get('name', self.archivo.name)}' "
                              f"tiene status 'deprecated'. Su contenido puede estar obsoleto. "
                              f"Considerar actualizar o reemplazar por un artículo nuevo.")]
        return []


# ──────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida un artículo KB de Claude Code (single-file .md)."
    )
    parser.add_argument("ruta", help="Ruta al archivo .md del artículo KB")
    parser.add_argument("--strict", action="store_true",
                        help="Tratar warnings como errores")
    args = parser.parse_args()

    ruta = Path(args.ruta).resolve()
    if not ruta.exists():
        print(f"No existe: {ruta}")
        return 1

    if ruta.is_dir():
        # Modo legado: si recibe dir, busca primer .md y emite warning
        candidatos = list(ruta.glob("*.md"))
        if not candidatos:
            print(f"Dir sin .md dentro: {ruta}")
            return 1
        archivo = candidatos[0]
        print(f"[AVISO] Se recibió un directorio; usando primer .md encontrado: {archivo.name}")
        print("        Recomendado: pasar la ruta al .md directamente.\n")
    else:
        archivo = ruta

    validator = KnowledgeValidator(archivo, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
