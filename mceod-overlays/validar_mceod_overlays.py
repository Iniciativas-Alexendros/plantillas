#!/usr/bin/env python3
"""
Validador de plantillas mceod-overlays · v1.0.0

Verifica la integridad estructural del módulo `mceod-overlays/` que provee los
overlays L0–L3 consumidos por MCEOD (`claude-deploy.sh` → `apply/consolidate`).

Reglas:
  - Cada nivel L0, L1, L2, L3 existe como subdirectorio.
  - Cada nivel contiene README.md y gitignore.template.
  - settings.json.template es opcional pero, si existe, debe ser JSON válido
    (tras sustituir {{VARS}} por "SENTINEL").
  - L0 y L1 deben proveer CLAUDE.md.template; NO deben proveer _INIT.md.template
    ni overlay-metadata.template (esos pertenecen al régimen L2/L3 generado por
    `/init` real + cabecera MCEOD).
  - L2 y L3 deben proveer _INIT.md.template y overlay-metadata.template; NO
    deben proveer CLAUDE.md.template (lo emite `/init` real, no plantilla).
  - Ningún nivel debe contener archivos *.deprecated (residuos de migraciones).
  - --strict bumpea warnings a errores (para CI/CD).

Uso:
    python mceod-overlays/validar_mceod_overlays.py [ruta] [--strict]

Si `ruta` se omite, valida el directorio donde reside este script.
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validadores import BaseValidator, Check, Resultado, Nivel


# ═══════════════════════════════════════════════════════════════════════════
# Configuración
# ═══════════════════════════════════════════════════════════════════════════

NIVELES = ("L0", "L1", "L2", "L3")

# Archivos comunes obligatorios por nivel.
ARCHIVOS_COMUNES = ("README.md", "gitignore.template")

# Archivos requeridos en L0/L1 (régimen "plantilla directa").
ARCHIVOS_L0_L1_REQ = ("CLAUDE.md.template",)

# Archivos prohibidos en L0/L1.
ARCHIVOS_L0_L1_PROH = ("_INIT.md.template", "overlay-metadata.template")

# Archivos requeridos en L2/L3 (régimen "init real + cabecera MCEOD").
ARCHIVOS_L2_L3_REQ = ("_INIT.md.template", "overlay-metadata.template")

# Archivos prohibidos en L2/L3.
ARCHIVOS_L2_L3_PROH = ("CLAUDE.md.template",)

# Sentinel para sustituir placeholders {{VAR}} antes de parsear JSON.
SENTINEL = "SENTINEL"
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")


# ═══════════════════════════════════════════════════════════════════════════
# Validador
# ═══════════════════════════════════════════════════════════════════════════

class MceodOverlaysValidator(BaseValidator):
    """Validador para el módulo mceod-overlays/."""

    def __init__(self, ruta: Path, strict: bool = False):
        super().__init__(ruta, strict)
        self.checks = [
            Check("niveles_presentes", self._check_niveles_presentes),
            Check("archivos_por_nivel", self._check_archivos_por_nivel),
            Check("json_templates_parseables", self._check_json_templates),
            Check("sin_deprecated", self._check_sin_deprecated),
        ]

    # ──────────────────────────────────────────────────────────────────────
    # Checks
    # ──────────────────────────────────────────────────────────────────────

    def _check_niveles_presentes(self):
        """Cada nivel L0..L3 debe existir como subdirectorio."""
        resultados = []
        for nivel in NIVELES:
            p = self.ruta / nivel
            if not p.is_dir():
                resultados.append(Resultado(
                    Nivel.ERROR, "niveles_presentes",
                    f"Falta subdirectorio de nivel: {nivel}/",
                    nivel,
                ))
        if not resultados:
            resultados.append(Resultado(
                Nivel.OK, "niveles_presentes",
                f"Niveles presentes: {', '.join(NIVELES)}",
            ))
        return resultados

    def _check_archivos_por_nivel(self):
        """Valida archivos requeridos/prohibidos por nivel."""
        resultados = []
        for nivel in NIVELES:
            dir_nivel = self.ruta / nivel
            if not dir_nivel.is_dir():
                continue  # ya reportado por _check_niveles_presentes

            # Comunes
            for nombre in ARCHIVOS_COMUNES:
                if not (dir_nivel / nombre).is_file():
                    resultados.append(Resultado(
                        Nivel.ERROR, "archivos_por_nivel",
                        f"{nivel}/ falta archivo obligatorio: {nombre}",
                        f"{nivel}/{nombre}",
                    ))

            if nivel in ("L0", "L1"):
                for nombre in ARCHIVOS_L0_L1_REQ:
                    if not (dir_nivel / nombre).is_file():
                        resultados.append(Resultado(
                            Nivel.ERROR, "archivos_por_nivel",
                            f"{nivel}/ falta archivo obligatorio: {nombre}",
                            f"{nivel}/{nombre}",
                        ))
                for nombre in ARCHIVOS_L0_L1_PROH:
                    if (dir_nivel / nombre).exists():
                        resultados.append(Resultado(
                            Nivel.ERROR, "archivos_por_nivel",
                            f"{nivel}/ contiene archivo prohibido para "
                            f"plantilla directa: {nombre}",
                            f"{nivel}/{nombre}",
                        ))
            else:  # L2, L3
                for nombre in ARCHIVOS_L2_L3_REQ:
                    if not (dir_nivel / nombre).is_file():
                        resultados.append(Resultado(
                            Nivel.ERROR, "archivos_por_nivel",
                            f"{nivel}/ falta archivo obligatorio: {nombre}",
                            f"{nivel}/{nombre}",
                        ))
                for nombre in ARCHIVOS_L2_L3_PROH:
                    if (dir_nivel / nombre).exists():
                        resultados.append(Resultado(
                            Nivel.ERROR, "archivos_por_nivel",
                            f"{nivel}/ contiene archivo prohibido en régimen "
                            f"init-real: {nombre}",
                            f"{nivel}/{nombre}",
                        ))

        if not any(r.nivel == Nivel.ERROR for r in resultados):
            resultados.append(Resultado(
                Nivel.OK, "archivos_por_nivel",
                "Archivos por nivel (requeridos/prohibidos) OK",
            ))
        return resultados

    def _check_json_templates(self):
        """Parsea todos los *.json.template tras sustituir {{VAR}} → SENTINEL."""
        resultados = []
        candidatos = sorted(self.ruta.rglob("*.json.template"))
        if not candidatos:
            resultados.append(Resultado(
                Nivel.WARNING, "json_templates_parseables",
                "No se encontró ningún *.json.template",
            ))
            return resultados

        for p in candidatos:
            rel = self._rel(p)
            try:
                raw = p.read_text(encoding="utf-8")
            except OSError as e:
                resultados.append(Resultado(
                    Nivel.ERROR, "json_templates_parseables",
                    f"No se pudo leer {rel}: {e}",
                    rel,
                ))
                continue

            sustituido = PLACEHOLDER_RE.sub(SENTINEL, raw)
            try:
                json.loads(sustituido)
            except json.JSONDecodeError as e:
                resultados.append(Resultado(
                    Nivel.ERROR, "json_templates_parseables",
                    f"JSON inválido tras sustituir placeholders: {e}",
                    rel,
                ))

        if not any(r.nivel == Nivel.ERROR for r in resultados):
            resultados.append(Resultado(
                Nivel.OK, "json_templates_parseables",
                f"Todos los *.json.template parseables ({len(candidatos)} archivos)",
            ))
        return resultados

    def _check_sin_deprecated(self):
        """Ningún archivo *.deprecated debe estar presente."""
        resultados = []
        deprecados = sorted(self.ruta.rglob("*.deprecated"))
        for p in deprecados:
            resultados.append(Resultado(
                Nivel.ERROR, "sin_deprecated",
                f"Archivo residual *.deprecated: {self._rel(p)}",
                self._rel(p),
            ))
        if not deprecados:
            resultados.append(Resultado(
                Nivel.OK, "sin_deprecated",
                "Sin archivos *.deprecated",
            ))
        return resultados


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida el módulo mceod-overlays/ (overlays L0–L3 MCEOD)."
    )
    parser.add_argument(
        "ruta",
        nargs="?",
        default=str(Path(__file__).resolve().parent),
        help="Directorio mceod-overlays/ a validar (por defecto el del script)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Tratar warnings como errores (para CI/CD)",
    )
    args = parser.parse_args()

    ruta = Path(args.ruta).resolve()
    if not ruta.exists():
        print(f"No existe: {ruta}")
        return 1
    if not ruta.is_dir():
        print(f"No es un directorio: {ruta}")
        return 1

    validator = MceodOverlaysValidator(ruta, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
