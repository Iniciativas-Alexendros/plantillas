"""Tests del generador de la SPA `dossier-bloque2.html`."""

import json
import re
from pathlib import Path

import pytest

from plantillas.catalog import load_catalog
from plantillas.generators.dossier import render_dossier


@pytest.fixture(scope="module")
def catalog():
    return load_catalog()


@pytest.fixture(scope="module")
def html(catalog) -> str:
    return render_dossier(Path(__file__).resolve().parents[1], catalog)


def test_render_minimal(html):
    """El HTML es self-contained y arranca con frontmatter-comentario."""
    assert html.startswith("<!doctype html>")
    assert "@name: dossier-bloque2" in html
    assert "@category: playbook" in html
    assert "@runtime: browser" in html


def test_no_external_cdn(html):
    """No debe cargar scripts ni CSS de CDNs externos."""
    external = re.findall(r'(?:src|href)="https?://(?!localhost)', html)
    assert not external, f"Recursos externos no permitidos: {external[:3]}"


def test_data_json_parses(html):
    """El bloque <script id="dossier-data"> parsea como JSON."""
    match = re.search(
        r'<script id="dossier-data" type="application/json">(.*?)</script>',
        html,
        re.DOTALL,
    )
    assert match, "Falta el bloque <script id=\"dossier-data\">"
    data = json.loads(match.group(1))
    assert "modules" in data
    assert "index_toc" in data
    assert "roadmap" in data
    assert "changelog" in data


def test_all_modules_present(html, catalog):
    """Todos los módulos canónicos del catálogo aparecen en el JSON embebido."""
    match = re.search(
        r'<script id="dossier-data" type="application/json">(.*?)</script>',
        html,
        re.DOTALL,
    )
    data = json.loads(match.group(1))
    module_ids = {m["id"] for m in data["modules"]}
    for cid in catalog.canonical_ids():
        assert cid in module_ids, f"Falta el módulo {cid!r} en el JSON de la SPA"


def test_index_toc_includes_docs(html):
    """El TOC incluye los docs transversales de docs/*.md."""
    match = re.search(
        r'<script id="dossier-data" type="application/json">(.*?)</script>',
        html,
        re.DOTALL,
    )
    data = json.loads(match.group(1))
    paths = {item["path"] for item in data["index_toc"]}
    assert "docs/cli.md" in paths
    assert "docs/validators.md" in paths


def test_dossier_size_under_200kb(html):
    """La SPA no debe inflarse más allá de 200KB sin motivo."""
    assert len(html) < 200_000, f"SPA demasiado grande: {len(html):,} bytes"


def test_theme_slider_present(html):
    """El slider sepia↔nocturno cumple el canon miniapps VAP."""
    assert 'id="theme-slider"' in html
    assert 'type="range"' in html
    assert 'data-theme="sepia"' in html
    assert 'data-theme="nocturno"' in html


def test_aria_tabs(html):
    """Los tabs usan roles ARIA correctos."""
    assert 'role="tablist"' in html
    assert 'role="tabpanel"' in html
    assert 'aria-selected="true"' in html


def test_generated_at_is_iso8601(html):
    """El timestamp de generación es ISO 8601."""
    match = re.search(
        r'<script id="dossier-data" type="application/json">(.*?)</script>',
        html,
        re.DOTALL,
    )
    data = json.loads(match.group(1))
    # El parser emite YYYY-MM-DD; el generador sobreescribe con ISO 8601 completo.
    assert re.match(r"\d{4}-\d{2}-\d{2}", data["generated_at"]), data["generated_at"]
    assert "T" in data["generated_at"], f"generated_at sin tiempo: {data['generated_at']}"


def test_determinism(catalog):
    """Dos invocaciones consecutivas producen el mismo output (excepto timestamp)."""
    import time
    html1 = render_dossier(Path(__file__).resolve().parents[1], catalog)
    time.sleep(1.1)  # cruza el segundo para que el timestamp cambie
    html2 = render_dossier(Path(__file__).resolve().parents[1], catalog)
    # El timestamp difiere; el resto del documento debe ser idéntico.
    h1_no_ts = re.sub(r'"generated_at": "[^"]+"', "", html1)
    h2_no_ts = re.sub(r'"generated_at": "[^"]+"', "", html2)
    assert h1_no_ts == h2_no_ts
