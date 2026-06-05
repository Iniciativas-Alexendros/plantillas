"""
Motor de validación reusable para plantillas de Claude Code.

Uso:
    from validadores import BaseValidator, Check, Resultado

    class MiValidador(BaseValidator):
        def __init__(self, ruta):
            super().__init__(ruta)
            self.checks = [
                Check("estructura", self.check_estructura),
                Check("frontmatter", self.check_frontmatter),
            ]

    validador = MiValidador("/ruta/al/modulo")
    exit_code = validador.run()
"""

from .base import BaseValidator, Check, Resultado, Nivel
from .checks import (
    check_yaml_frontmatter,
    check_json_parseable,
    check_yaml_parseable,
    check_placeholders,
    check_archivos_vacios,
    check_estructura,
    check_archivos_prohibidos,
    check_tamanio_maximo,
    check_merge_conflicts,
    check_secrets,
    check_gitignore_minimo,
)
from .reporte import reportar_resultados

__all__ = [
    "BaseValidator",
    "Check",
    "Resultado",
    "Nivel",
    "check_yaml_frontmatter",
    "check_json_parseable",
    "check_yaml_parseable",
    "check_placeholders",
    "check_archivos_vacios",
    "check_estructura",
    "check_archivos_prohibidos",
    "check_tamanio_maximo",
    "check_merge_conflicts",
    "check_secrets",
    "check_gitignore_minimo",
    "reportar_resultados",
]
