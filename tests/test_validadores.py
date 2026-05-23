"""
Tests unitarios para el motor de validación reusable.

Ejecutar:
    pytest tests/test_validadores.py -v
    pytest tests/ -v --tb=short
"""

import sys
from pathlib import Path

# Asegurar que el motor de validación está en path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validadores import (
    BaseValidator,
    Check,
    Resultado,
    Nivel,
    check_estructura,
    check_archivos_vacios,
    check_placeholders,
)


class FakeValidator(BaseValidator):
    """Validator de prueba que no aplica checks por defecto."""

    def __init__(self, ruta, strict=False):
        super().__init__(ruta, strict)
        self.checks = []


class TestCheckEstructura:
    def test_directorio_requerido_faltante(self, tmp_path):
        v = FakeValidator(tmp_path)
        resultados = check_estructura(v, dirs_requeridos=["src"], archivos_requeridos=[])
        assert any(r.nivel == Nivel.ERROR and "src" in r.mensaje for r in resultados)

    def test_archivo_requerido_presente(self, tmp_path):
        (tmp_path / "README.md").write_text("# Test")
        v = FakeValidator(tmp_path)
        resultados = check_estructura(v, dirs_requeridos=[], archivos_requeridos=["README.md"])
        assert all(r.nivel != Nivel.ERROR for r in resultados)


class TestCheckArchivosVacios:
    def test_archivo_muy_pequeno(self, tmp_path):
        p = tmp_path / "tiny.md"
        p.write_text("x")
        v = FakeValidator(tmp_path)
        resultados = check_archivos_vacios(v, min_bytes=50)
        assert any(r.nivel == Nivel.WARNING and "tiny.md" in r.mensaje for r in resultados)

    def test_archivo_suficientemente_grande(self, tmp_path):
        p = tmp_path / "big.md"
        p.write_text("x" * 100)
        v = FakeValidator(tmp_path)
        resultados = check_archivos_vacios(v, min_bytes=50)
        assert not any("big.md" in r.mensaje for r in resultados)


class TestCheckPlaceholders:
    def test_placeholder_detectado(self, tmp_path):
        p = tmp_path / "test.md"
        p.write_text("Esto tiene un placeholder [nombre-de-skill] sin rellenar.")
        v = FakeValidator(tmp_path)
        resultados = check_placeholders(v)
        assert any(r.nivel == Nivel.ERROR and "[nombre-de-skill]" in r.mensaje for r in resultados)

    def test_sin_placeholders(self, tmp_path):
        p = tmp_path / "clean.md"
        p.write_text("Esto está completo y no tiene placeholders.")
        v = FakeValidator(tmp_path)
        resultados = check_placeholders(v)
        assert len(resultados) == 0


class TestBaseValidator:
    def test_run_sin_checks(self, tmp_path):
        v = FakeValidator(tmp_path)
        assert v.run() == 0

    def test_run_con_error(self, tmp_path):
        v = FakeValidator(tmp_path)
        v.checks = [Check("test", lambda: [Resultado(Nivel.ERROR, "test", "fallo")])]
        assert v.run() == 1

    def test_run_strict_warning(self, tmp_path):
        v = FakeValidator(tmp_path, strict=True)
        v.checks = [Check("test", lambda: [Resultado(Nivel.WARNING, "test", "cuidado")])]
        assert v.run() == 1
