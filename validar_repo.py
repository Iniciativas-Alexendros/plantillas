#!/usr/bin/env python3
"""
Validador Global del Repositorio · v1.0.0

Protege la estructura canónica del sistema de plantillas contra mutaciones
indeseadas: archivos core, directorios permitidos, estructura de módulos,
.gitignore, archivos prohibidos, y merge-conflicts.

Uso:
    python validar_repo.py
    python validar_repo.py --strict
    python validar_repo.py /ruta/al/repo --strict
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validadores import (
    BaseValidator,
    Check,
    Resultado,
    Nivel,
    check_archivos_prohibidos,
    check_gitignore_minimo,
    check_merge_conflicts,
    check_secrets,
    check_tamanio_maximo,
)


# ──────────────────────────────────────────────────────────────────────────
# Configuración canónica del repositorio
# ──────────────────────────────────────────────────────────────────────────

ARCHIVOS_CORE = [
    "INDEX.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "INTEGRACION.md",
    "install.sh",
    "claude-init",
    "update.sh",
    ".pre-commit-config.yaml",
]

ARCHIVOS_RAIZ_REQUERIDOS = ARCHIVOS_CORE + [".gitignore", "README.md"]

DIRECTORIOS_PERMITIDOS = {
    "agent-config",
    "agentes",
    "artefactos",
    "commands",
    "estandares",
    "hooks",
    "mcp",
    "miniapps",
    "modulo",
    "plugins",
    "proyecto",
    "repositorios",
    "skills",
    "tests",
    "validadores",
}

MODULOS_CANONICOS = [
    "agent-config",
    "agentes",
    "skills",
    "commands",
    "hooks",
    "mcp",
    "plugins",
    "repositorios",
    "modulo",
    "proyecto",
    "miniapps",
]

# Módulos que no siguen el patrón plantilla_*/ejemplo_* porque su raíz ES la plantilla
MODULOS_ESPECIALES = {"modulo", "proyecto"}

NOMBRE_SINGULAR = {
    "agent-config": "agent_config",
    "agentes": "agente",
    "skills": "skill",
    "commands": "command",
    "hooks": "hook",
    "mcp": "mcp",
    "plugins": "plugin",
    "repositorios": "repositorio",
    "miniapps": "miniapps",
}

ARCHIVOS_PROHIBIDOS = [
    ".env",
    ".env.local",
    ".env.production",
    "*.pem",
    "*.key",
    "id_rsa",
    "id_rsa.pub",
    "secrets",
    "secrets.json",
    "credentials.json",
]

PATRONES_SECRETO = [
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{36,}"),  # GitHub tokens
    re.compile(r"sk-[a-zA-Z0-9]{20,}"),  # OpenAI / Stripe sk
    re.compile(r"AKIA[0-9A-Z]{16}"),  # AWS Access Key
    re.compile(r"[0-9a-f]{32}-[0-9a-f]{32}"),  # SendGrid
    re.compile(r"private[_-]?key\s*[:=]\s*['\"]?[\w/+]{20,}"),
]

MAX_FILE_SIZE_KB = 500

GITIGNORE_MINIMO = [
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "secrets/",
    "__pycache__/",
    ".DS_Store",
    "/vap/",
    "/cuaderno-plantilla/",
    "/artefactos/operador/",
]


# ──────────────────────────────────────────────────────────────────────────
# ValidadorGlobal
# ──────────────────────────────────────────────────────────────────────────


class ValidadorGlobal(BaseValidator):
    def __init__(self, ruta_repo: Path, strict: bool = False):
        super().__init__(ruta_repo, strict)
        self.checks = [
            Check("archivos_core", self._check_archivos_core),
            Check("directorios_raiz", self._check_directorios_raiz),
            Check("estructura_modulos", self._check_estructura_modulos),
            Check("gitignore", self._check_gitignore),
            Check("archivos_prohibidos", self._check_archivos_prohibidos),
            Check("tamanio_archivos", self._check_tamanio),
            Check("merge_conflicts", self._check_merge_conflicts),
            Check("secrets_texto_plano", self._check_secrets),
        ]

    # ── Checks ────────────────────────────────────────────────────────────

    def _check_archivos_core(self) -> list[Resultado]:
        """Verifica que existan los archivos core de la raíz."""
        resultados = []
        for nombre in ARCHIVOS_RAIZ_REQUERIDOS:
            path = self.ruta / nombre
            if not path.is_file():
                resultados.append(
                    Resultado(
                        Nivel.ERROR,
                        "archivos_core",
                        f"Falta archivo core en raíz: {nombre}",
                        nombre,
                    )
                )
            else:
                resultados.append(
                    Resultado(
                        Nivel.OK,
                        "archivos_core",
                        f"Archivo core presente: {nombre}",
                        nombre,
                    )
                )
        return resultados

    def _gitignore_patterns(self) -> set[str]:
        gi = self.ruta / ".gitignore"
        if not gi.is_file():
            return set()
        patterns = set()
        for line in gi.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            patterns.add(line.lstrip("/"))
        return patterns

    def _check_directorios_raiz(self) -> list[Resultado]:
        """Lista blanca de directorios en raíz."""
        resultados = []
        gitignore = self._gitignore_patterns()
        for path in self.ruta.iterdir():
            if not path.is_dir():
                continue
            if path.name.startswith("."):
                continue  # .git, .github
            if path.name in gitignore or f"{path.name}/" in gitignore:
                continue  # Ignorar directorios en .gitignore
            if path.name not in DIRECTORIOS_PERMITIDOS:
                resultados.append(
                    Resultado(
                        Nivel.ERROR,
                        "directorios_raiz",
                        f"Directorio no permitido en raíz: {path.name}/"
                        f" — Si es un nuevo módulo, añádelo a DIRECTORIOS_PERMITIDOS"
                        f" y a los tests",
                        str(path.relative_to(self.ruta)),
                    )
                )
        for nombre in sorted(DIRECTORIOS_PERMITIDOS):
            path = self.ruta / nombre
            if path.is_dir():
                resultados.append(
                    Resultado(
                        Nivel.OK,
                        "directorios_raiz",
                        f"Directorio permitido presente: {nombre}/",
                        nombre,
                    )
                )
        return resultados

    def _check_estructura_modulos(self) -> list[Resultado]:
        """Cada módulo canónico debe tener plantilla, ejemplo, validador y workflow."""
        resultados = []
        for mod in MODULOS_CANONICOS:
            mod_path = self.ruta / mod
            if not mod_path.is_dir():
                resultados.append(
                    Resultado(
                        Nivel.ERROR,
                        "estructura_modulos",
                        f"Módulo canónico no encontrado: {mod}/",
                        mod,
                    )
                )
                continue

            singular = NOMBRE_SINGULAR.get(mod, mod)

            if mod not in MODULOS_ESPECIALES:
                # Plantilla: aceptar dir legado o single-file `plantilla_<base>.*` (canon-runtime).
                # Extensiones canónicas: .md (la mayoría) o .sh.template (hooks).
                base_plantilla = f"plantilla_{singular}"
                plantilla_dir = mod_path / base_plantilla
                plantilla_files = [
                    p
                    for p in mod_path.glob(f"{base_plantilla}.*")
                    if p.is_file() and not p.name.endswith(".bak")
                ]
                if not plantilla_dir.is_dir() and not plantilla_files:
                    resultados.append(
                        Resultado(
                            Nivel.ERROR,
                            "estructura_modulos",
                            f"{mod}/ falta plantilla (ni dir '{base_plantilla}/' ni archivo '{base_plantilla}.*')",
                            f"{mod}/{base_plantilla}",
                        )
                    )

                # Ejemplo: aceptar dir legado o single-file `ejemplo_<base>.*`.
                base_ejemplo = f"ejemplo_{singular}"
                ejemplo_dir = mod_path / base_ejemplo
                ejemplo_files = [
                    p
                    for p in mod_path.glob(f"{base_ejemplo}.*")
                    if p.is_file() and not p.name.endswith(".bak")
                ]
                if not ejemplo_dir.is_dir() and not ejemplo_files:
                    resultados.append(
                        Resultado(
                            Nivel.ERROR,
                            "estructura_modulos",
                            f"{mod}/ falta ejemplo (ni dir '{base_ejemplo}/' ni archivo '{base_ejemplo}.*')",
                            f"{mod}/{base_ejemplo}",
                        )
                    )
            else:
                # Módulos especiales: su raíz ES la plantilla; validan estructura propia
                if mod == "modulo":
                    req_files = ["README.md", "MODULO.md", "ejemplo_modulo/EJEMPLO.md"]
                elif mod == "proyecto":
                    req_files = [
                        "README.md",
                        "CLAUDE.md",
                        "settings.json",
                        "mcp.json",
                        ".github/workflows/ci.yml",
                    ]
                for rf in req_files:
                    if not (mod_path / rf).exists():
                        resultados.append(
                            Resultado(
                                Nivel.ERROR,
                                "estructura_modulos",
                                f"{mod}/ falta archivo requerido: {rf}",
                                f"{mod}/{rf}",
                            )
                        )

            # Validador
            script = mod_path / f"validar_{singular}.py"
            if mod == "agentes":
                script = mod_path / "validar_agente.py"
            elif mod == "skills":
                script = mod_path / "validar_skill.py"
            elif mod == "commands":
                script = mod_path / "validar_command.py"
            elif mod == "hooks":
                script = mod_path / "validar_hook.py"
            elif mod == "mcp":
                script = mod_path / "validar_mcp.py"
            elif mod == "plugins":
                script = mod_path / "validar_plugin.py"
            elif mod == "repositorios":
                script = mod_path / "validar_repositorio.py"

            if not script.is_file():
                resultados.append(
                    Resultado(
                        Nivel.ERROR,
                        "estructura_modulos",
                        f"{mod}/ falta validador: {script.name}",
                        str(script.relative_to(self.ruta)),
                    )
                )

            # Workflow
            wf = mod_path / ".github" / "workflows" / f"validar-{mod}.yml"
            if not wf.is_file():
                resultados.append(
                    Resultado(
                        Nivel.WARNING,
                        "estructura_modulos",
                        f"{mod}/ falta workflow CI: {wf.name}",
                        str(wf.relative_to(self.ruta)),
                    )
                )
            else:
                resultados.append(
                    Resultado(
                        Nivel.OK,
                        "estructura_modulos",
                        f"{mod}/ estructura canónica OK",
                        mod,
                    )
                )
        return resultados

    def _check_gitignore(self) -> list[Resultado]:
        """Verifica que .gitignore contenga exclusiones mínimas."""
        return check_gitignore_minimo(self, GITIGNORE_MINIMO)

    def _check_archivos_prohibidos(self) -> list[Resultado]:
        """Detecta archivos que nunca deben estar en el repo."""
        return check_archivos_prohibidos(self, ARCHIVOS_PROHIBIDOS)

    def _check_tamanio(self) -> list[Resultado]:
        """Ningún archivo debe superar MAX_FILE_SIZE_KB."""
        return check_tamanio_maximo(self, MAX_FILE_SIZE_KB)

    def _check_merge_conflicts(self) -> list[Resultado]:
        """Detecta marcadores de conflicto no resueltos."""
        return check_merge_conflicts(self)

    def _check_secrets(self) -> list[Resultado]:
        """Heurística básica de detección de secrets en texto plano."""
        return check_secrets(self, PATRONES_SECRETO)


# ──────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Validador global de estructura del repositorio de plantillas"
    )
    parser.add_argument(
        "repo",
        nargs="?",
        default=".",
        help="Ruta al repositorio (default: .)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Trata warnings como errores",
    )
    args = parser.parse_args()

    ruta = Path(args.repo).resolve()
    validator = ValidadorGlobal(ruta, strict=args.strict)
    sys.exit(validator.run())


if __name__ == "__main__":
    main()
