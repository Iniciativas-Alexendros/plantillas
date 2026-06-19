"""
Tests unitarios para el motor de validación reusable.

Ejecutar:
    pytest tests/test_validadores.py -v
    pytest tests/ -v --tb=short
"""

import re
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
    check_archivos_prohibidos,
    check_tamanio_maximo,
    check_merge_conflicts,
    check_secrets,
    check_gitignore_minimo,
)


class FakeValidator(BaseValidator):
    """Validator de prueba que no aplica checks por defecto."""

    def __init__(self, ruta, strict=False):
        super().__init__(ruta, strict)
        self.checks = []


class TestCheckEstructura:
    def test_directorio_requerido_faltante(self, tmp_path):
        v = FakeValidator(tmp_path)
        resultados = check_estructura(
            v, dirs_requeridos=["src"], archivos_requeridos=[]
        )
        assert any(r.nivel == Nivel.ERROR and "src" in r.mensaje for r in resultados)

    def test_archivo_requerido_presente(self, tmp_path):
        (tmp_path / "README.md").write_text("# Test")
        v = FakeValidator(tmp_path)
        resultados = check_estructura(
            v, dirs_requeridos=[], archivos_requeridos=["README.md"]
        )
        assert all(r.nivel != Nivel.ERROR for r in resultados)


class TestCheckArchivosVacios:
    def test_archivo_muy_pequeno(self, tmp_path):
        p = tmp_path / "tiny.md"
        p.write_text("x")
        v = FakeValidator(tmp_path)
        resultados = check_archivos_vacios(v, min_bytes=50)
        assert any(
            r.nivel == Nivel.WARNING and "tiny.md" in r.mensaje for r in resultados
        )

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
        assert any(
            r.nivel == Nivel.ERROR and "[nombre-de-skill]" in r.mensaje
            for r in resultados
        )

    def test_sin_placeholders(self, tmp_path):
        p = tmp_path / "clean.md"
        p.write_text("Esto está completo y no tiene placeholders.")
        v = FakeValidator(tmp_path)
        resultados = check_placeholders(v)
        assert len(resultados) == 0


class TestCheckArchivosProhibidos:
    def test_nombre_exacto_detectado(self, tmp_path):
        (tmp_path / ".env").write_text("SECRET=1")
        v = FakeValidator(tmp_path)
        resultados = check_archivos_prohibidos(v, [".env"])
        assert any(r.nivel == Nivel.ERROR and ".env" in r.mensaje for r in resultados)

    def test_glob_extension_detectado(self, tmp_path):
        (tmp_path / "clave.pem").write_text("-----BEGIN-----")
        v = FakeValidator(tmp_path)
        resultados = check_archivos_prohibidos(v, ["*.pem"])
        assert any(
            r.nivel == Nivel.ERROR and "clave.pem" in r.mensaje for r in resultados
        )

    def test_archivo_permitido_no_marca(self, tmp_path):
        (tmp_path / "README.md").write_text("# ok")
        v = FakeValidator(tmp_path)
        resultados = check_archivos_prohibidos(v, [".env", "*.pem"])
        assert len(resultados) == 0


class TestCheckTamanioMaximo:
    def test_archivo_excede_limite(self, tmp_path):
        (tmp_path / "grande.bin").write_bytes(b"x" * 2048)
        v = FakeValidator(tmp_path)
        resultados = check_tamanio_maximo(v, max_kb=1)
        assert any(
            r.nivel == Nivel.ERROR and "grande.bin" in r.mensaje for r in resultados
        )

    def test_archivo_dentro_de_limite(self, tmp_path):
        (tmp_path / "pequeno.txt").write_text("hola")
        v = FakeValidator(tmp_path)
        resultados = check_tamanio_maximo(v, max_kb=500)
        assert len(resultados) == 0


class TestCheckMergeConflicts:
    def test_marcador_detectado(self, tmp_path):
        (tmp_path / "conflicto.txt").write_text(
            "<<<<<<< HEAD\nfoo\n=======\nbar\n>>>>>>> rama\n"
        )
        v = FakeValidator(tmp_path)
        resultados = check_merge_conflicts(v)
        assert any(
            r.nivel == Nivel.ERROR and "conflicto.txt" in r.mensaje for r in resultados
        )

    def test_archivo_limpio(self, tmp_path):
        (tmp_path / "limpio.txt").write_text("contenido normal sin conflictos")
        v = FakeValidator(tmp_path)
        resultados = check_merge_conflicts(v)
        assert len(resultados) == 0


class TestCheckSecrets:
    def test_token_detectado(self, tmp_path):
        patrones = [re.compile(r"AKIA[0-9A-Z]{16}")]
        # Construido por partes: evita que el literal dispare el escáner de
        # secrets del propio repo al validar este archivo de tests.
        fake_key = "AKIA" + "IOSFODNN7EXAMPLE"
        (tmp_path / "config.txt").write_text(f"aws_key = {fake_key}")
        v = FakeValidator(tmp_path)
        resultados = check_secrets(v, patrones)
        assert any(
            r.nivel == Nivel.ERROR and "config.txt" in r.mensaje for r in resultados
        )

    def test_sin_secrets(self, tmp_path):
        patrones = [re.compile(r"AKIA[0-9A-Z]{16}")]
        (tmp_path / "doc.md").write_text("Texto inofensivo sin credenciales.")
        v = FakeValidator(tmp_path)
        resultados = check_secrets(v, patrones)
        assert len(resultados) == 0


class TestCheckGitignoreMinimo:
    def test_falta_gitignore(self, tmp_path):
        v = FakeValidator(tmp_path)
        resultados = check_gitignore_minimo(v, [".env"])
        assert any(
            r.nivel == Nivel.ERROR and ".gitignore" in r.mensaje for r in resultados
        )

    def test_entrada_faltante_es_warning(self, tmp_path):
        (tmp_path / ".gitignore").write_text(".env\n")
        v = FakeValidator(tmp_path)
        resultados = check_gitignore_minimo(v, [".env", "*.key"])
        assert any(
            r.nivel == Nivel.WARNING and "*.key" in r.mensaje for r in resultados
        )
        assert not any("'.env'" in r.mensaje for r in resultados)

    def test_todas_las_entradas_presentes(self, tmp_path):
        (tmp_path / ".gitignore").write_text(".env\n*.key\nsecrets/\n")
        v = FakeValidator(tmp_path)
        resultados = check_gitignore_minimo(v, [".env", "*.key", "secrets/"])
        assert len(resultados) == 0


class TestArchivosExcluye:
    """Regresión del bug B4: `_archivos()` no debe recursar en vendor/cachés."""

    def test_ignora_node_modules(self, tmp_path):
        (tmp_path / "real.md").write_text("contenido canónico suficiente.")
        nm = tmp_path / "node_modules" / "pkg"
        nm.mkdir(parents=True)
        (nm / "index.js").write_text("")  # archivo vacío que NO debe reportarse
        v = FakeValidator(tmp_path)
        archivos = v._archivos()
        nombres = {p.name for p in archivos}
        assert "real.md" in nombres
        assert "index.js" not in nombres
        # Y por extensión, ningún check debe quejarse del vacío vendorizado.
        resultados = check_archivos_vacios(v, min_bytes=50)
        assert not any("index.js" in r.mensaje for r in resultados)

    def test_ignora_venv_y_worktrees(self, tmp_path):
        for sub in (".venv/lib", ".claude/worktrees/wt1", "dist", "__pycache__"):
            d = tmp_path / sub
            d.mkdir(parents=True)
            (d / "x.txt").write_text("")
        (tmp_path / "ok.md").write_text("x" * 100)
        v = FakeValidator(tmp_path)
        rels = {p.relative_to(tmp_path).as_posix() for p in v._archivos()}
        assert rels == {"ok.md"}


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
        v.checks = [
            Check("test", lambda: [Resultado(Nivel.WARNING, "test", "cuidado")])
        ]
        assert v.run() == 1
