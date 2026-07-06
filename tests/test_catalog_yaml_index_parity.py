"""
Paridad `modules.yaml` ↔ `INDEX.md`.

Garantiza que todo módulo del catálogo canónico tiene al menos una
referencia en `INDEX.md` y viceversa. Detecta drift silencioso entre
el catálogo y la documentación.
"""

import re
from pathlib import Path

import pytest

from plantillas.catalog import load_catalog

PLANTILLAS = Path(__file__).resolve().parents[1]
INDEX = PLANTILLAS / "INDEX.md"


@pytest.fixture(scope="module")
def catalog():
    return load_catalog()


@pytest.fixture(scope="module")
def index_text() -> str:
    return INDEX.read_text(encoding="utf-8")


def _index_links_to_module(index_text: str, module_id: str) -> bool:
    """Devuelve True si INDEX.md enlaza o menciona el módulo."""
    if module_id in index_text:
        return True
    # Aliases: agents ↔ agentes, repo ↔ repositorios
    aliases = {
        "agentes": ["agents", "agentes", "agente"],
        "repositorios": ["repositorios", "repositorio"],
    }.get(module_id, [module_id])
    return any(alias in index_text for alias in aliases)


def test_index_exists():
    assert INDEX.exists(), f"Falta {INDEX}"


def test_every_canonical_module_in_index(catalog, index_text):
    missing = [
        mid
        for mid in catalog.canonical_ids()
        if not _index_links_to_module(index_text, mid)
    ]
    assert not missing, f"Módulos canónicos sin referencia en INDEX.md: {missing}"


def test_modules_listed_in_index_exist_in_catalog(catalog, index_text):
    """Cualquier enlace `./<modulo>/...` en INDEX debe corresponder a un módulo
    del catálogo (o a un sub-path estándar como `docs/`, `estandares/`)."""
    pattern = re.compile(r"\./([a-z][a-z0-9-]+)/")
    referenced = {match.group(1) for match in pattern.finditer(index_text)}
    canonical = set(catalog.canonical_ids())
    # Paths que NO son módulos pero aparecen en INDEX (legítimos):
    not_modules = {"docs", "estandares", "validadores"}  # transversales al catálogo
    unknown = referenced - canonical - not_modules
    assert not unknown, f"Paths en INDEX.md sin contraparte en modules.yaml: {unknown}"
