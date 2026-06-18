#!/usr/bin/env python3
"""
Validador de Repositorios GitHub · v1.0.0

Verifica que un repositorio cumpla con el canon de community health,
estructura profesional, y metodología de trabajo definidos por el
sistema de plantillas.

Uso:
    python validar_repositorio.py /ruta/al/repo
    python validar_repositorio.py /ruta/al/repo --strict
    python validar_repositorio.py /ruta/al/repo --visibility public
    python validar_repositorio.py /ruta/al/repo --visibility private
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validadores import (
    BaseValidator,
    Check,
    Resultado,
    Nivel,
    check_placeholders,
    check_archivos_vacios,
)


# Archivos obligatorios para todo repo
REQUIRED_FILES = [
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "AUTHORS.md",
    "SUPPORT.md",
    "MAINTAINERS.md",
    "RELEASE.md",
    "ROADMAP.md",
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    ".github/CODEOWNERS",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/dependabot.yml",
    ".github/workflows/ci.yml",
    "docs/adr/0001-usar-madr-para-adrs.md",
    "docs/README.md",
]

# Archivos obligatorios solo para repos públicos
REQUIRED_FILES_PUBLIC = [
    ".github/FUNDING.yml",
    ".github/ISSUE_TEMPLATE/bug.yml",
    ".github/ISSUE_TEMPLATE/feature.yml",
    ".github/ISSUE_TEMPLATE/question.yml",
    ".github/ISSUE_TEMPLATE/security.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
]

LICENSE_FILES = ["LICENSE", "COPYRIGHT.md"]


class RepoValidator(BaseValidator):
    def __init__(
        self, repo_dir: Path, strict: bool = False, visibility: str = "public"
    ):
        super().__init__(repo_dir, strict)
        self.visibility = visibility
        self.checks = [
            Check("estructura", self._check_estructura),
            Check("readme", self._check_readme),
            Check("licencia", self._check_licencia),
            Check("changelog", self._check_changelog),
            Check("contributing", self._check_contributing),
            Check("security", self._check_security),
            Check("codeowners", self._check_codeowners),
            Check("github", self._check_github_files),
            Check("ci", self._check_ci),
            Check("dependabot", self._check_dependabot),
            Check("adr", self._check_adr),
            Check("placeholder", self._check_placeholders),
            Check("vacio", self._check_empty_files),
        ]

    def _check_estructura(self):
        resultados = []
        for f in REQUIRED_FILES:
            p = self.ruta / f
            if not p.is_file():
                resultados.append(
                    Resultado(
                        Nivel.ERROR, "estructura", f"Falta archivo obligatorio: {f}"
                    )
                )

        if self.visibility == "public":
            for f in REQUIRED_FILES_PUBLIC:
                p = self.ruta / f
                if not p.is_file():
                    resultados.append(
                        Resultado(
                            Nivel.ERROR, "estructura", f"Falta archivo obligatorio: {f}"
                        )
                    )

        # Licencia: LICENSE o COPYRIGHT.md (al menos uno)
        tiene_licencia = any((self.ruta / f).is_file() for f in LICENSE_FILES)
        if not tiene_licencia:
            resultados.append(
                Resultado(Nivel.ERROR, "estructura", "Falta LICENSE o COPYRIGHT.md")
            )

        return resultados

    def _check_readme(self):
        resultados = []
        readme = self.ruta / "README.md"
        if not readme.exists():
            return resultados

        content = readme.read_text(encoding="utf-8")

        # Repos docs-only (sin manifiesto de código) no tienen Stack ni
        # instalación de dependencias: esas secciones no aplican. Se detecta
        # por ausencia de manifiestos de los stacks soportados.
        manifiestos = [
            "package.json",
            "pyproject.toml",
            "requirements.txt",
            "go.mod",
            "Cargo.toml",
        ]
        es_docs_only = not any((self.ruta / m).is_file() for m in manifiestos)

        secciones_obligatorias = [
            ("## Qué es", "Qué es"),
            ("## Estructura", "Estructura"),
            ("## Licencia", "Licencia"),
        ]
        if not es_docs_only:
            secciones_obligatorias.extend(
                [
                    ("## Stack", "Stack"),
                    ("## Instala", "Instala"),
                ]
            )
        for marcador, nombre in secciones_obligatorias:
            if marcador not in content:
                resultados.append(
                    Resultado(
                        Nivel.WARNING,
                        "readme",
                        f"README.md debería tener '{nombre}'",
                        "README.md",
                    )
                )

        if "badge" not in content.lower() and "![" not in content:
            resultados.append(
                Resultado(
                    Nivel.WARNING,
                    "readme",
                    "README.md debería tener un badge de CI",
                    "README.md",
                )
            )

        return resultados

    def _check_licencia(self):
        resultados = []
        licencia = None
        for f in LICENSE_FILES:
            p = self.ruta / f
            if p.exists():
                licencia = p
                break

        if not licencia:
            resultados.append(
                Resultado(Nivel.ERROR, "licencia", "Falta LICENSE o COPYRIGHT.md")
            )
            return resultados

        content = licencia.read_text(encoding="utf-8")
        if "{{YEAR}}" in content or "{{COPYRIGHT_HOLDER}}" in content:
            resultados.append(
                Resultado(
                    Nivel.ERROR,
                    "licencia",
                    f"{licencia.name} contiene placeholders sin rellenar",
                    licencia.name,
                )
            )

        return resultados

    def _check_changelog(self):
        resultados = []
        changelog = self.ruta / "CHANGELOG.md"
        if not changelog.exists():
            return resultados

        content = changelog.read_text(encoding="utf-8")

        if "## [Unreleased]" not in content and "## [Sin publicar]" not in content:
            resultados.append(
                Resultado(
                    Nivel.WARNING,
                    "changelog",
                    "CHANGELOG.md debería tener '[Unreleased]'",
                    "CHANGELOG.md",
                )
            )

        secciones_map = {
            "Added": ["### Added", "### Añadido"],
            "Changed": ["### Changed", "### Cambiado"],
            "Deprecated": ["### Deprecated", "### Obsoleto"],
            "Removed": ["### Removed", "### Eliminado"],
            "Fixed": ["### Fixed", "### Corregido"],
            "Security": ["### Security", "### Seguridad"],
        }
        for seccion, variantes in secciones_map.items():
            if not any(v in content for v in variantes):
                resultados.append(
                    Resultado(
                        Nivel.WARNING,
                        "changelog",
                        f"CHANGELOG.md falta sección '{seccion}'",
                        "CHANGELOG.md",
                    )
                )

        return resultados

    def _check_contributing(self):
        resultados = []
        contributing = self.ruta / "CONTRIBUTING.md"
        if not contributing.exists():
            return resultados

        content = contributing.read_text(encoding="utf-8")

        if "conventional commits" not in content.lower():
            resultados.append(
                Resultado(
                    Nivel.WARNING,
                    "contributing",
                    "CONTRIBUTING.md debería mencionar Conventional Commits",
                    "CONTRIBUTING.md",
                )
            )

        if "signed" not in content.lower() and "firma" not in content.lower():
            resultados.append(
                Resultado(
                    Nivel.WARNING,
                    "contributing",
                    "CONTRIBUTING.md debería mencionar commits firmados",
                    "CONTRIBUTING.md",
                )
            )

        return resultados

    def _check_security(self):
        resultados = []
        security = self.ruta / "SECURITY.md"
        if not security.exists():
            return resultados

        content = security.read_text(encoding="utf-8")

        if "report" not in content.lower() and "reportar" not in content.lower():
            resultados.append(
                Resultado(
                    Nivel.WARNING,
                    "security",
                    "SECURITY.md debería explicar cómo reportar vulnerabilidades",
                    "SECURITY.md",
                )
            )

        return resultados

    def _check_codeowners(self):
        resultados = []
        codeowners = self.ruta / ".github/CODEOWNERS"
        if not codeowners.exists():
            return resultados

        content = codeowners.read_text(encoding="utf-8")

        if "*" not in content:
            resultados.append(
                Resultado(
                    Nivel.WARNING,
                    "codeowners",
                    "CODEOWNERS debería tener un owner por defecto (*)",
                    ".github/CODEOWNERS",
                )
            )

        return resultados

    def _check_github_files(self):
        resultados = []
        pr_template = self.ruta / ".github/PULL_REQUEST_TEMPLATE.md"
        if pr_template.exists():
            content = pr_template.read_text(encoding="utf-8")
            if "Qué" not in content or "Por qué" not in content:
                resultados.append(
                    Resultado(
                        Nivel.WARNING,
                        "github",
                        "PR template debería tener 'Qué' y 'Por qué'",
                        ".github/PULL_REQUEST_TEMPLATE.md",
                    )
                )

        if self.visibility == "public":
            for tmpl in [
                "bug.yml",
                "feature.yml",
                "question.yml",
                "security.yml",
                "config.yml",
            ]:
                p = self.ruta / ".github/ISSUE_TEMPLATE" / tmpl
                if not p.exists():
                    resultados.append(
                        Resultado(
                            Nivel.ERROR, "github", f"Falta template de issue: {tmpl}"
                        )
                    )

        return resultados

    def _check_ci(self):
        resultados = []
        ci_dir = self.ruta / ".github/workflows"
        if not ci_dir.exists():
            resultados.append(
                Resultado(Nivel.ERROR, "ci", "Falta directorio .github/workflows/")
            )
            return resultados

        ymls = list(ci_dir.glob("*.yml")) + list(ci_dir.glob("*.yaml"))
        if not ymls:
            resultados.append(
                Resultado(Nivel.ERROR, "ci", "No hay workflows de GitHub Actions")
            )
            return resultados

        for yml in ymls:
            content = yml.read_text(encoding="utf-8")
            if "permissions:" not in content:
                resultados.append(
                    Resultado(
                        Nivel.WARNING,
                        "ci",
                        f"{self._rel(yml)} debería definir 'permissions' explícitos",
                        self._rel(yml),
                    )
                )

        return resultados

    def _check_dependabot(self):
        resultados = []
        dependabot = self.ruta / ".github/dependabot.yml"
        if not dependabot.exists():
            resultados.append(
                Resultado(Nivel.WARNING, "dependabot", "Falta .github/dependabot.yml")
            )
            return resultados

        content = dependabot.read_text(encoding="utf-8")
        if "package-ecosystem" not in content:
            resultados.append(
                Resultado(
                    Nivel.WARNING,
                    "dependabot",
                    "dependabot.yml debería tener 'package-ecosystem'",
                    ".github/dependabot.yml",
                )
            )

        return resultados

    def _check_adr(self):
        resultados = []
        adr_dir = self.ruta / "docs/adr"
        if not adr_dir.exists():
            resultados.append(
                Resultado(Nivel.WARNING, "adr", "Falta directorio docs/adr/")
            )
            return resultados

        adrs = list(adr_dir.glob("*.md"))
        if not adrs:
            resultados.append(
                Resultado(Nivel.WARNING, "adr", "No hay ADRs en docs/adr/")
            )
            return resultados

        for adr in adrs:
            content = adr.read_text(encoding="utf-8")
            if "status:" not in content.lower() and "estado:" not in content.lower():
                resultados.append(
                    Resultado(
                        Nivel.WARNING,
                        "adr",
                        f"{self._rel(adr)} debería tener 'status'",
                        self._rel(adr),
                    )
                )

        return resultados

    def _check_placeholders(self):
        return check_placeholders(
            self, extensiones=(".md", ".json", ".yaml", ".yml", ".txt")
        )

    def _check_empty_files(self):
        # VERSIÓN/VERSION: ficheros de versión semántica cuyo contenido mínimo
        # ("0.2.0\n") es correcto por diseño, no son ficheros vacíos.
        return check_archivos_vacios(
            self, min_bytes=30, archivos_ignorados=["VERSIÓN", "VERSION"]
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida un repositorio GitHub profesional."
    )
    parser.add_argument("repo_dir", help="Directorio del repositorio a validar")
    parser.add_argument(
        "--strict", action="store_true", help="Tratar warnings como errores"
    )
    parser.add_argument(
        "--visibility",
        choices=["public", "private"],
        default="public",
        help="Visibilidad del repo (afecta checks de templates públicos)",
    )
    args = parser.parse_args()

    repo_path = Path(args.repo_dir)
    if not repo_path.exists():
        print(f"❌ El directorio no existe: {repo_path}")
        return 1
    if not repo_path.is_dir():
        print(f"❌ No es un directorio: {repo_path}")
        return 1

    validator = RepoValidator(repo_path, strict=args.strict, visibility=args.visibility)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
