"""
Smoke tests · Validan que cada módulo puede copiar su plantilla y validarla.

Ejecutar:
    pytest tests/test_smoke.py -v

El test descubre los módulos con `validator:` declarado en `modules.yaml`.
Añadir un módulo al catálogo + script `validar_<x>.py` lo incorpora
automáticamente.
"""

import shutil
import subprocess
import sys
from pathlib import Path

from plantillas.catalog import load_catalog

PLANTILLAS = Path(__file__).resolve().parents[1]


def _modulos_con_validador() -> list[tuple[str, str, str]]:
    """Lee `modules.yaml` y devuelve [(modulo, script, base_ejemplo)]."""
    catalog = load_catalog()
    out: list[tuple[str, str, str]] = []
    for module in catalog.canonical_ids():
        entry = catalog.by_id(module)
        if entry is None or not entry.validator:
            continue
        out.append((module, Path(entry.validator).name, _base_ejemplo(entry.example)))
    return out


def _base_ejemplo(example: str | None) -> str:
    if not example:
        return ""
    return Path(example).name


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
        """Cada ejemplo debe pasar su validador en modo strict.

        FIXME: este test falla actualmente para `agent-config` porque
        `agent-config/ejemplo_agent_config/AGENTS.md` está borrado del
        working tree (deuda pre-existente, no relacionada con esta
        refactorización). Restaurar ese archivo o reescribir el ejemplo
        canónico para que el validador strict pase. Mientras tanto, se
        ejecuta bajo `tests/test_smoke.py` y se excluye del flujo
        principal con `pytest --ignore=tests/test_smoke.py`.
        """
        for modulo, script, ejemplo in _modulos_con_validador():
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
