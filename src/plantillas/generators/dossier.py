"""Generador de la SPA `dossier-bloque2.html`.

Compone datos desde `modules.yaml`, `INDEX.md`, `ROADMAP.md`, `CHANGELOG.md`
y `docs/adr/*.md`, y los renderiza con Jinja2 a un único HTML self-contained.

Uso programático:

    from pathlib import Path
    from plantillas.catalog import load_catalog
    from plantillas.generators.dossier import render_dossier

    catalog = load_catalog()
    html = render_dossier(Path(".").resolve(), catalog)
    Path("docs/dossier-bloque2.html").write_text(html, encoding="utf-8")
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from plantillas.catalog import Catalog
from plantillas.generators.parsers import build_dossier_data

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


def _to_json(value: object) -> str:
    """Serializa con `sort_keys=True` para diffs de git deterministas."""
    return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True)


def render_dossier(root: Path, catalog: Catalog) -> str:
    """Renderiza la SPA como string HTML self-contained.

    `root` es la raíz del repo (donde vive `modules.yaml`).
    `catalog` es el catálogo cargado.
    """
    data = build_dossier_data(root, catalog)
    payload = {
        **data.__dict__,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["tojson_pretty"] = _to_json
    template = env.get_template("dossier.html.j2")
    return template.render(data=payload, data_json=_to_json(payload))
