
from plantillas.catalog import load_catalog


def test_load_catalog():
    catalog = load_catalog()
    assert catalog.version == "2.0.0-dev"
    assert len(catalog.modules) >= 12


def test_canonical_modules():
    catalog = load_catalog()
    ids = catalog.canonical_ids()
    assert "agent-config" in ids
    assert "agentes" in ids
    assert "repositorios" in ids


def test_by_id():
    catalog = load_catalog()
    mod = catalog.by_id("agent-config")
    assert mod is not None
    assert mod.path == "agent-config"
