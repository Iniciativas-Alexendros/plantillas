"""
Smoke tests · Validan que cada módulo puede copiar su plantilla y validarla.

Ejecutar:
    pytest tests/test_smoke.py -v
"""

import shutil
import subprocess
import sys
from pathlib import Path

PLANTILLAS = Path(__file__).resolve().parents[1]

MODULOS = [
    ("agentes", "validar_agente.py", "ejemplo_agente"),
    ("skills", "validar_skill.py", "ejemplo_skill"),
    ("commands", "validar_command.py", "ejemplo_command"),
    ("hooks", "validar_hook.py", "ejemplo_hook"),
    ("mcp", "validar_mcp.py", "ejemplo_mcp"),
    ("plugins", "validar_plugin.py", "ejemplo_plugin"),
    ("dot-claude", "validar_dot_claude.py", "ejemplo_dot_claude"),
    ("repositorios", "validar_repositorio.py", "ejemplo_repositorio"),
    ("modulo", "validar_modulo.py", "modulo"),
    ("proyecto", "validar_proyecto.py", "proyecto"),
]


class TestSmoke:
    def test_todos_los_ejemplos_pasan_strict(self, tmp_path):
        """Cada ejemplo debe pasar su validador en modo strict."""
        for modulo, script, ejemplo in MODULOS:
            script_path = PLANTILLAS / modulo / script
            ejemplo_path = PLANTILLAS / modulo / ejemplo

            assert script_path.exists(), f"Falta validador: {script_path}"
            assert ejemplo_path.exists(), f"Falta ejemplo: {ejemplo_path}"

            extra = ["--visibility", "public"] if modulo == "repositorios" else []
            result = subprocess.run(
                [sys.executable, str(script_path), str(ejemplo_path), "--strict"] + extra,
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0, (
                f"{modulo} falló strict:\nstdout: {result.stdout}\nstderr: {result.stderr}"
            )

    def test_copiar_plantilla_y_validar(self, tmp_path):
        """Copiar plantilla a /tmp y validar debe detectar placeholders."""
        # Usamos skills como caso de prueba (plantilla más simple)
        src = PLANTILLAS / "skills" / "plantilla_skill"
        dst = tmp_path / "mi-skill"
        shutil.copytree(src, dst)

        script_path = PLANTILLAS / "skills" / "validar_skill.py"
        result = subprocess.run(
            [sys.executable, str(script_path), str(dst), "--strict"],
            capture_output=True,
            text=True,
        )
        # La plantilla tiene placeholders → debe fallar en strict
        assert result.returncode == 1, (
            f"Se esperaba fallo por placeholders, pero salió {result.returncode}"
        )
        assert "placeholder" in result.stdout.lower() or "placeholder" in result.stderr.lower()
