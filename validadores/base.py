"""
BaseValidator · Clase base para todos los validadores del sistema.
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable, List


class Nivel(Enum):
    ERROR = "error"
    WARNING = "warning"
    OK = "ok"


@dataclass
class Resultado:
    """Un resultado de validación individual."""
    nivel: Nivel
    check: str          # Nombre del check
    mensaje: str        # Descripción del hallazgo
    archivo: str = ""   # Archivo relacionado (opcional)
    linea: int = 0      # Línea relacionada (opcional)


@dataclass
class Check:
    """Un check individual que se ejecuta sobre un módulo."""
    nombre: str
    funcion: Callable[[], List[Resultado]]


class BaseValidator:
    """
    Clase base para validadores de módulos.

    Subclases deben:
      1. Definir self.checks en __init__
      2. (Opcional) Sobrescribir check_estructura_base()
    """

    PLACEHOLDER_PATTERNS = [
        re.compile(r"\[dominio\]-\[rol\]"),
        re.compile(r"\[AS[IÍ]\]"),
        re.compile(r"\[nombre-.+?\]"),
        re.compile(r"\[Nombre .+?\]"),
        re.compile(r"\[descripción .+?\]"),
        re.compile(r"\[tool[0-9]*\]"),
        re.compile(r"\[skill[0-9]*\]"),
        re.compile(r"\[Paso [0-9]+\]"),
        re.compile(r"\[propósito\]"),
        re.compile(r"\[qué .+?\]"),
        re.compile(r"\[cuándo .+?\]"),
        re.compile(r"\[cómo .+?\]"),
    ]

    MIN_FILE_SIZE = 50

    def __init__(self, ruta_modulo: Path, strict: bool = False):
        self.ruta = Path(ruta_modulo).resolve()
        self.strict = strict
        self.resultados: List[Resultado] = []
        self.checks: List[Check] = []

        if not self.ruta.exists():
            raise FileNotFoundError(f"No existe: {self.ruta}")
        if not self.ruta.is_dir():
            raise NotADirectoryError(f"No es un directorio: {self.ruta}")

    # ──────────────────────────────────────────────────────────────────────
    # API pública
    # ──────────────────────────────────────────────────────────────────────

    def run(self) -> int:
        """Ejecuta todos los checks y devuelve código de salida."""
        print(f"🔍 Validando: {self.ruta}")
        print(f"   Modo: {'strict' if self.strict else 'normal'}")
        print()

        for check in self.checks:
            try:
                resultados = check.funcion()
                self.resultados.extend(resultados)
            except Exception as e:
                self.resultados.append(
                    Resultado(
                        nivel=Nivel.ERROR,
                        check=check.nombre,
                        mensaje=f"Excepción durante check: {e}",
                    )
                )

        return self._reportar()

    def agregar_error(self, check: str, mensaje: str, archivo: str = "", linea: int = 0):
        self.resultados.append(Resultado(Nivel.ERROR, check, mensaje, archivo, linea))

    def agregar_warning(self, check: str, mensaje: str, archivo: str = "", linea: int = 0):
        self.resultados.append(Resultado(Nivel.WARNING, check, mensaje, archivo, linea))

    def agregar_ok(self, check: str, mensaje: str, archivo: str = "", linea: int = 0):
        self.resultados.append(Resultado(Nivel.OK, check, mensaje, archivo, linea))

    # ──────────────────────────────────────────────────────────────────────
    # Helpers protegidos
    # ──────────────────────────────────────────────────────────────────────

    def _archivos(self, patron: str = "*") -> List[Path]:
        """Devuelve archivos dentro del módulo que coinciden con el patrón."""
        return [p for p in self.ruta.rglob(patron) if p.is_file()]

    def _rel(self, p: Path) -> str:
        """Devuelve la ruta relativa al módulo."""
        return str(p.relative_to(self.ruta))

    def _reportar(self) -> int:
        """Reporta resultados y devuelve código de salida."""
        from .reporte import reportar_resultados
        return reportar_resultados(self.resultados, self.strict)

    def _extraer_fuera_codeblock(self, content: str) -> str:
        """Extrae texto fuera de bloques markdown ```."""
        cleaned = re.sub(r"```[\s\S]*?```", "", content)
        cleaned = re.sub(r"`[^`]+`", "", cleaned)
        return cleaned
