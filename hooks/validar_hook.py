#!/usr/bin/env python3
"""
Validador de Hooks Claude Code · v3.0.0 (canon-runtime alignment)

Acepta el formato single-file `<nombre-hook>.sh.template` (o `.sh`) con
cabecera declarativa bash + cuerpo del hook que emite JSON {decision, reason}
a stdout.

Uso:
    python validar_hook.py hooks/ejemplo_hook.sh.template --strict
    python validar_hook.py hooks/plantilla_hook.sh.template
    python validar_hook.py ~/.claude/hooks/pre-bash-secret-guard.sh --strict

Compatibilidad legado: si se pasa un directorio, busca el primer archivo .sh*
dentro y emite warning indicando migración pendiente.

Referencia:
    - Claude Code Hooks: https://code.claude.com/docs/en/hooks.md
    - Claude Code Hooks Guide: https://code.claude.com/docs/en/hooks-guide.md
"""

import argparse
import os
import re
import sys
from pathlib import Path

# Motor de validación reusable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validadores import (
    BaseValidator,
    Check,
    Resultado,
    Nivel,
)

# pyyaml no es necesario en este validador: los hooks son scripts shell, no YAML.


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

VALID_MATCHERS = {
    "PreToolUse",
    "PostToolUse",
    "SessionStart",
    "SessionEnd",
    "UserPromptSubmit",
    "Stop",
    "Notification",
    "PreCompact",
}

VALID_SHEBANGS = {
    "#!/usr/bin/env bash",
    "#!/bin/bash",
}

HEADER_REQUIRED = ["# name:", "# matcher:", "# description:"]

KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")

# Heurística: el hook escribe JSON de decisión a stdout
SALIDA_JSON_RE = re.compile(
    r"""(printf|echo)\s+['"]\s*\{.*"decision".*\}""",
    re.DOTALL,
)

# Placeholders tipo MAYÚSCULAS-CON-GUIONES detectables en ejemplos
PLACEHOLDER_RE = re.compile(r"\b[A-Z][A-Z0-9]*(?:-[A-Z][A-Z0-9]*)+\b")


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDADOR
# ═══════════════════════════════════════════════════════════════════════════════

class HookValidator(BaseValidator):
    """Validador para hooks single-file (formato canon-runtime)."""

    def __init__(self, archivo: Path, strict: bool = False):
        # BaseValidator requiere un directorio; usamos el parent del archivo.
        super().__init__(archivo.parent, strict)
        self.archivo = archivo.resolve()
        self.es_plantilla = self.archivo.name.startswith("plantilla_")
        self.checks = [
            Check("formato", self._check_formato),
            Check("shebang", self._check_shebang),
            Check("cabecera", self._check_cabecera),
            Check("matcher_valido", self._check_matcher_valido),
            Check("name_kebab", self._check_name_kebab),
            Check("placeholders", self._check_placeholders),
            Check("ejecutable", self._check_ejecutable),
            Check("salida_json", self._check_salida_json),
        ]

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _lines(self):
        """Devuelve las líneas del archivo."""
        return self.archivo.read_text(encoding="utf-8").splitlines()

    def _content(self) -> str:
        return self.archivo.read_text(encoding="utf-8")

    def _header_value(self, key: str) -> str:
        """
        Extrae el valor de una clave de cabecera tipo '# key: valor'.
        Devuelve '' si no se encuentra.
        """
        for line in self._lines():
            stripped = line.strip()
            if stripped.startswith(f"# {key}:"):
                return stripped[len(f"# {key}:"):].strip()
        return ""

    # ── Checks ───────────────────────────────────────────────────────────────

    def _check_formato(self):
        if not self.archivo.is_file():
            return [Resultado(Nivel.ERROR, "formato",
                              f"{self.archivo.name} no existe o no es un archivo")]
        name = self.archivo.name
        if not (name.endswith(".sh") or name.endswith(".sh.template")):
            return [Resultado(Nivel.ERROR, "formato",
                              f"{name} debe terminar en .sh o .sh.template")]
        return []

    def _check_shebang(self):
        if not self.archivo.is_file():
            return []
        lines = self._lines()
        if not lines:
            return [Resultado(Nivel.ERROR, "shebang",
                              f"{self.archivo.name} está vacío")]
        first = lines[0].strip()
        if first not in VALID_SHEBANGS:
            return [Resultado(Nivel.ERROR, "shebang",
                              f"Primera línea '{first}' no es un shebang válido "
                              f"(esperado: {sorted(VALID_SHEBANGS)})")]
        return []

    def _check_cabecera(self):
        if not self.archivo.is_file():
            return []
        content = self._content()
        resultados = []
        for campo in HEADER_REQUIRED:
            if campo not in content:
                resultados.append(Resultado(Nivel.ERROR, "cabecera",
                                            f"Falta campo obligatorio en cabecera: '{campo}'"))
        return resultados

    def _check_matcher_valido(self):
        if not self.archivo.is_file():
            return []
        matcher_raw = self._header_value("matcher")
        if not matcher_raw:
            # Si la cabecera completa falta, _check_cabecera ya lo reporta.
            return []
        # El campo matcher puede tener varios valores separados por " | "
        matchers = [m.strip() for m in matcher_raw.split("|")]
        resultados = []
        for m in matchers:
            # Ignorar placeholders en plantillas
            if self.es_plantilla and PLACEHOLDER_RE.match(m):
                continue
            if m and m not in VALID_MATCHERS:
                resultados.append(Resultado(Nivel.ERROR, "matcher_valido",
                                            f"Matcher '{m}' no reconocido "
                                            f"(válidos: {sorted(VALID_MATCHERS)})"))
        return resultados

    def _check_name_kebab(self):
        if not self.archivo.is_file():
            return []
        name = self._header_value("name")
        if not name:
            return []
        if not KEBAB_RE.match(name):
            # En plantillas el name es un placeholder → solo warning
            nivel = Nivel.WARNING if self.es_plantilla else Nivel.ERROR
            return [Resultado(nivel, "name_kebab",
                              f"name '{name}' no es kebab-case válido"
                              + (" (esperado en plantilla)" if self.es_plantilla else ""))]
        return []

    def _check_placeholders(self):
        """Solo se aplica a ejemplos (no plantillas)."""
        if self.es_plantilla:
            return []
        if not self.archivo.is_file():
            return []
        content = self._content()
        # Buscar patrones TODO explícitos fuera de comentarios de cabecera
        if re.search(r"\bTODO\b.*reemplazar\b", content, re.IGNORECASE):
            return [Resultado(Nivel.WARNING, "placeholders",
                              f"{self.archivo.name} contiene TODOs sin rellenar")]
        return []

    def _check_ejecutable(self):
        """Warning si el archivo no tiene bit de ejecución."""
        if not self.archivo.is_file():
            return []
        if not os.access(self.archivo, os.X_OK):
            return [Resultado(Nivel.WARNING, "ejecutable",
                              f"{self.archivo.name} no tiene bit +x "
                              f"(ejecutar: chmod +x {self.archivo.name})")]
        return []

    def _check_salida_json(self):
        """
        Heurística: verifica que el hook emite JSON con 'decision' a stdout
        mediante printf o echo.
        """
        if not self.archivo.is_file():
            return []
        content = self._content()
        if not SALIDA_JSON_RE.search(content):
            return [Resultado(Nivel.WARNING, "salida_json",
                              f"{self.archivo.name} no contiene patrón "
                              f"printf/echo '{{\"decision\"...}}'; verifica que el hook "
                              f"emite JSON de decisión a stdout")]
        return []


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida un hook Claude Code single-file (canon-runtime)."
    )
    parser.add_argument(
        "ruta",
        help="Ruta al archivo .sh o .sh.template del hook (o dir legado)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Tratar warnings como errores (CI/CD)",
    )
    args = parser.parse_args()

    ruta = Path(args.ruta).resolve()

    if not ruta.exists():
        print(f"❌ No existe: {ruta}")
        return 1

    # Compatibilidad legado: si es un directorio, buscar primer .sh* dentro.
    if ruta.is_dir():
        candidatos = sorted(ruta.glob("*.sh*"))
        if not candidatos:
            print(f"❌ Dir sin archivos .sh / .sh.template: {ruta}")
            return 1
        archivo = candidatos[0]
        print(f"⚠️  Modo legado: validando {archivo.name} (migrar a single-file)")
    else:
        archivo = ruta

    validator = HookValidator(archivo, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
