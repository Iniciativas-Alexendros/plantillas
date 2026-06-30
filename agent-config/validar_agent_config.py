#!/usr/bin/env python3
"""
Validador del módulo agent-config · v1.0.0

Verifica que la fuente canónica YAML sea válida, que contenga los campos
obligatorios, y que los artefactos del ejemplo coincidan con la generación
actual (drift check).

Uso:
    python validar_agent_config.py /ruta/al/modulo/agent-config
    python validar_agent_config.py /ruta/al/modulo/agent-config --strict
"""

import argparse
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validadores import (
    BaseValidator,
    Check,
    Resultado,
    Nivel,
    check_yaml_parseable,
)

# Intentar importar yaml
try:
    import yaml

    HAS_YAML = True
except ImportError:  # pragma: no cover
    HAS_YAML = False

REQUIRED_FILES = [
    "plantilla_agent_config.yaml",
    "generar_agent_configs.py",
    "validar_agent_config.py",
    "README.md",
]
REQUIRED_DIRS = ["ejemplo_agent_config"]
REQUIRED_TOP_LEVEL_KEYS = [
    "version",
    "metadata",
    "operator",
    "style",
    "flow",
    "models",
    "security",
    "code_style",
    "hierarchy",
]


def _load_yaml(path: Path) -> dict:
    if not HAS_YAML:
        raise RuntimeError("pyyaml no está instalado")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


class AgentConfigValidator(BaseValidator):
    def __init__(self, ruta_modulo: Path, strict: bool = False):
        super().__init__(ruta_modulo, strict)
        self.checks = [
            Check("estructura", self._check_estructura),
            Check("yaml", self._check_yaml_valido),
            Check("campos", self._check_campos_requeridos),
            Check("secrets", self._check_secrets),
            Check("generador", self._check_generador),
            Check("drift", self._check_drift),
        ]

    def _check_estructura(self) -> list[Resultado]:
        resultados = []
        for nombre in REQUIRED_FILES:
            p = self.ruta / nombre
            if not p.is_file():
                resultados.append(
                    Resultado(
                        Nivel.ERROR,
                        "estructura",
                        f"Falta archivo obligatorio: {nombre}",
                        nombre,
                    )
                )
        for d in REQUIRED_DIRS:
            p = self.ruta / d
            if not p.is_dir():
                resultados.append(
                    Resultado(
                        Nivel.ERROR,
                        "estructura",
                        f"Falta directorio obligatorio: {d}/",
                        d,
                    )
                )
        return resultados

    def _check_yaml_valido(self) -> list[Resultado]:
        source = self.ruta / "plantilla_agent_config.yaml"
        if not source.is_file():
            return []
        return check_yaml_parseable(self, source)

    def _check_campos_requeridos(self) -> list[Resultado]:
        resultados = []
        source = self.ruta / "plantilla_agent_config.yaml"
        if not source.is_file() or not HAS_YAML:
            return resultados

        try:
            cfg = _load_yaml(source)
        except Exception:
            return resultados

        for key in REQUIRED_TOP_LEVEL_KEYS:
            if key not in cfg:
                resultados.append(
                    Resultado(
                        Nivel.ERROR,
                        "campos",
                        f"plantilla_agent_config.yaml falta clave obligatoria: '{key}'",
                        "plantilla_agent_config.yaml",
                    )
                )

        # Validaciones específicas de subcampos
        op = cfg.get("operator", {})
        for subkey in ("name", "location", "language"):
            if subkey not in op:
                resultados.append(
                    Resultado(
                        Nivel.WARNING,
                        "campos",
                        f"operator.{subkey} no está definido",
                        "plantilla_agent_config.yaml",
                    )
                )

        sec = cfg.get("security", {})
        for subkey in ("env_files", "git_push", "rm"):
            if subkey not in sec:
                resultados.append(
                    Resultado(
                        Nivel.WARNING,
                        "campos",
                        f"security.{subkey} no está definido",
                        "plantilla_agent_config.yaml",
                    )
                )

        return resultados

    def _check_secrets(self) -> list[Resultado]:
        resultados = []
        source = self.ruta / "plantilla_agent_config.yaml"
        if not source.is_file():
            return resultados
        text = source.read_text(encoding="utf-8")
        # Heurísticas básicas: tokens largos de GitHub, OpenAI, AWS, etc.
        patrones = [
            r"gh[pousr]_[A-Za-z0-9_]{36,}",
            r"sk-[a-zA-Z0-9]{20,}",
            r"AKIA[0-9A-Z]{16}",
            r"[0-9a-f]{32}-[0-9a-f]{32}",
            r"private[_-]?key\s*[:=]\s*['\"]?[\w/+]{20,}",
        ]
        import re

        for pat in patrones:
            for match in re.finditer(pat, text):
                resultados.append(
                    Resultado(
                        Nivel.ERROR,
                        "secrets",
                        f"Posible secret en fuente canónica: {match.group(0)[:20]}...",
                        "plantilla_agent_config.yaml",
                    )
                )
                break
        return resultados

    def _check_generador(self) -> list[Resultado]:
        resultados = []
        script = self.ruta / "generar_agent_configs.py"
        if not script.is_file():
            return resultados

        # Verificar sintaxis con py_compile
        import py_compile

        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as e:
            resultados.append(
                Resultado(
                    Nivel.ERROR,
                    "generador",
                    f"generar_agent_configs.py tiene error de sintaxis: {e}",
                    "generar_agent_configs.py",
                )
            )
            return resultados

        return resultados

    def _check_drift(self) -> list[Resultado]:
        """Genera los artefactos en un tmpdir y compara con el ejemplo."""
        resultados = []
        source = self.ruta / "plantilla_agent_config.yaml"
        script = self.ruta / "generar_agent_configs.py"
        ejemplo = self.ruta / "ejemplo_agent_config"
        if not source.is_file() or not script.is_file() or not ejemplo.is_dir():
            return resultados

        import subprocess

        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp)
            try:
                subprocess.run(
                    [
                        sys.executable,
                        str(script),
                        str(source),
                        "--home",
                        str(tmp_home),
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
            except subprocess.CalledProcessError as e:
                resultados.append(
                    Resultado(
                        Nivel.ERROR,
                        "drift",
                        f"El generador falló: {e.stderr}",
                        "generar_agent_configs.py",
                    )
                )
                return resultados

            mapping = [
                (tmp_home / ".claude" / "CLAUDE.md", ejemplo / ".claude" / "CLAUDE.md"),
                (
                    tmp_home / ".claude" / "settings.json",
                    ejemplo / ".claude" / "settings.json",
                ),
                (tmp_home / ".claude" / ".mcp.json", ejemplo / ".claude" / ".mcp.json"),
                (tmp_home / "AGENTS.md", ejemplo / "AGENTS.md"),
                (
                    tmp_home / ".config" / "devin" / "AGENTS.md",
                    ejemplo / ".config" / "devin" / "AGENTS.md",
                ),
                (
                    tmp_home / ".config" / "devin" / "config.json",
                    ejemplo / ".config" / "devin" / "config.json",
                ),
                (
                    tmp_home / ".codeium" / "windsurf" / "memories" / "global_rules.md",
                    ejemplo / ".codeium" / "windsurf" / "memories" / "global_rules.md",
                ),
            ]

            for generated, expected in mapping:
                if not expected.exists():
                    resultados.append(
                        Resultado(
                            Nivel.WARNING,
                            "drift",
                            f"Falta archivo de ejemplo: {self._rel(expected)}",
                            self._rel(expected),
                        )
                    )
                    continue
                if not generated.exists():
                    resultados.append(
                        Resultado(
                            Nivel.ERROR,
                            "drift",
                            f"El generador no produjo: {expected.name}",
                            self._rel(expected),
                        )
                    )
                    continue

                gen_text = generated.read_text(encoding="utf-8")
                exp_text = expected.read_text(encoding="utf-8")

                if gen_text != exp_text:
                    resultados.append(
                        Resultado(
                            Nivel.ERROR,
                            "drift",
                            f"El ejemplo {self._rel(expected)} no coincide con la fuente canónica. "
                            f"Ejecuta: python generar_agent_configs.py --home ejemplo_agent_config",
                            self._rel(expected),
                        )
                    )
                else:
                    resultados.append(
                        Resultado(
                            Nivel.OK,
                            "drift",
                            f"{self._rel(expected)} sincronizado con la fuente",
                            self._rel(expected),
                        )
                    )

        return resultados


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("modulo", help="Directorio del módulo agent-config")
    parser.add_argument(
        "--strict", action="store_true", help="Tratar warnings como errores"
    )
    args = parser.parse_args()

    ruta = Path(args.modulo).resolve()
    if not ruta.exists():
        print(f"❌ El directorio no existe: {ruta}")
        return 1

    validator = AgentConfigValidator(ruta, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
