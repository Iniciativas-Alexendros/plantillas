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

# (modulo, script, base_ejemplo) — base_ejemplo se resuelve dinámicamente:
# si existe `<mod>/<base>` (dir canon legado) lo usa; si no, busca
# `<mod>/<base>.<ext>` para los módulos single-file post canon-runtime
# (`.md` o `.sh.template`). Se añade `agent-config` como módulo cross-platform.
MODULOS = [
    ("agentes", "validar_agente.py", "ejemplo_agente"),
    ("skills", "validar_skill.py", "ejemplo_skill"),
    ("commands", "validar_command.py", "ejemplo_command"),
    ("hooks", "validar_hook.py", "ejemplo_hook"),
    ("mcp", "validar_mcp.py", "ejemplo_mcp"),
    ("plugins", "validar_plugin.py", "ejemplo_plugin"),
    ("agent-config", "validar_agent_config.py", "ejemplo_agent_config"),
    ("repositorios", "validar_repositorio.py", "ejemplo_repositorio"),
    ("modulo", "validar_modulo.py", "modulo"),
    ("proyecto", "validar_proyecto.py", "proyecto"),
    ("miniapps", "validar_miniapps.py", "ejemplo_miniapps"),
]


def _resolve_ejemplo(modulo: str, base: str) -> Path:
    """Devuelve el path al ejemplo aceptando dir o single-file.

    Para módulos especiales (`modulo`, `proyecto`, `agent-config`), su raíz ES
    la plantilla/ejemplo. Para el resto se prueba primero el dir legacy
    `<mod>/<base>/`; si no existe se busca `<mod>/<base>.<ext>` con cualquier
    extensión.
    """
    mod_dir = PLANTILLAS / modulo
    if modulo in {"modulo", "proyecto", "agent-config"}:
        return mod_dir
    legacy = mod_dir / base
    if legacy.is_dir():
        return legacy
    matches = sorted(
        p
        for p in mod_dir.glob(f"{base}.*")
        if p.is_file() and not p.name.endswith(".bak")
    )
    if matches:
        return matches[0]
    return mod_dir / base  # devolver el path inexistente para que el assert lo cace


class TestSmoke:
    def test_todos_los_ejemplos_pasan_strict(self, tmp_path):
        """Cada ejemplo debe pasar su validador en modo strict."""
        for modulo, script, ejemplo in MODULOS:
            script_path = PLANTILLAS / modulo / script
            ejemplo_path = _resolve_ejemplo(modulo, ejemplo)

            assert script_path.exists(), f"Falta validador: {script_path}"
            assert ejemplo_path.exists(), f"Falta ejemplo: {ejemplo_path}"

            extra = ["--visibility", "public"] if modulo == "repositorios" else []
            result = subprocess.run(
                [sys.executable, str(script_path), str(ejemplo_path), "--strict"]
                + extra,
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
        assert (
            "placeholder" in result.stdout.lower()
            or "placeholder" in result.stderr.lower()
        )
