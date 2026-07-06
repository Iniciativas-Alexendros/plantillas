"""Parsers de los documentos canon (INDEX, ROADMAP, CHANGELOG, docs/*).

Cada parser devuelve una estructura de datos serializable a JSON, que el
generador de la SPA embebe como `<script id="dossier-data" type="application/json">`.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

from plantillas.catalog import Catalog


@dataclass
class TOCItem:
    path: str
    title: str
    summary: str
    section: str = ""


@dataclass
class Phase:
    id: str
    title: str
    status: str  # ✅ 🔄 ⏳ 🚫 📦 🧱
    items: list[str] = field(default_factory=list)


@dataclass
class ChangelogEntry:
    version: str
    date: str
    items: list[str] = field(default_factory=list)


@dataclass
class Decision:
    id: str
    title: str
    body: str


@dataclass
class DossierData:
    generated_at: str
    catalog_version: str
    modules: list[dict]
    index_toc: list[dict]
    roadmap: list[dict]
    changelog: list[dict]
    decisions: list[dict]
    stats: dict


def _strip_markdown(text: str) -> str:
    """Quita formato básico: negritas, links, headings, código inline."""
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text.strip()


def _first_paragraph(text: str, max_chars: int = 280) -> str:
    """Primer párrafo no vacío de un markdown."""
    paragraphs = re.split(r"\n\s*\n", text)
    for p in paragraphs:
        p = p.strip()
        if not p or p.startswith("#"):
            continue
        clean = _strip_markdown(p)
        if len(clean) > max_chars:
            clean = clean[: max_chars - 1].rstrip() + "…"
        return clean
    return ""


def parse_index(path: Path) -> list[TOCItem]:
    """Extrae un TOC plano de INDEX.md (entradas `| [📋 Plantilla] | [path] |`).

    Estrategia laxa: parte el archivo por líneas, conserva las filas de
    tabla Markdown que contienen `[texto](./<ruta>)`, y deduplica por path.
    """
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    items: list[TOCItem] = []
    seen: set[str] = set()
    current_section = ""

    for line in text.splitlines():
        if line.startswith("## "):
            current_section = line[3:].strip()
            continue
        if line.startswith("### "):
            current_section = line[4:].strip()
            continue
        if "[`" in line and "`](" in line:
            # Formato: | [📋 Plantilla] | [`path`](./path) | descripción |
            match = re.search(r"\[`([^`]+)`\]\(\.\/([^)]+)\)", line)
            if match:
                rel = match.group(2)
                if rel in seen:
                    continue
                seen.add(rel)
                # descripción: tercer campo de la fila
                parts = [p.strip() for p in line.split("|")]
                desc = parts[3] if len(parts) >= 4 else ""
                items.append(
                    TOCItem(
                        path=rel,
                        title=match.group(1),
                        summary=_strip_markdown(desc),
                        section=current_section,
                    )
                )
    return items


def parse_roadmap(path: Path) -> list[Phase]:
    """Extrae fases del ROADMAP.md. Formato esperado: `## FASE X: ...`."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    phases: list[Phase] = []
    current: Phase | None = None

    for line in text.splitlines():
        m = re.match(r"^##\s+(FASE\s+\d+(?:\.\d+)?)\s*[:·\-—]?\s*(.+)$", line)
        if m:
            if current is not None:
                phases.append(current)
            current = Phase(
                id=m.group(1).strip(),
                title=m.group(2).strip(),
                status="⏳",
            )
            continue
        if current is None:
            continue
        if line.startswith("> **Estado**"):
            # `> **Estado**: ...`
            if "COMPLETADA" in line:
                current.status = "✅"
            elif "PROGRESO" in line:
                current.status = "🔄"
            elif "BLOQUE 2" in line or "Bloque 2" in line:
                current.status = "🧱"
        if re.match(r"^\s*-\s+\[", line):
            # `- [x] ...` o `- [ ] ...`
            current.items.append(_strip_markdown(line.strip()))

    if current is not None:
        phases.append(current)
    return phases


def parse_changelog(path: Path) -> list[ChangelogEntry]:
    """Extrae entradas del CHANGELOG.md. Formato: `## [VERSION] — TITLE`."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    entries: list[ChangelogEntry] = []
    current: ChangelogEntry | None = None

    for line in text.splitlines():
        m = re.match(r"^##\s+\[([^\]]+)\]\s+[—\-]\s+(.+)$", line)
        if m:
            if current is not None:
                entries.append(current)
            current = ChangelogEntry(
                version=m.group(1).strip(),
                date=m.group(2).strip(),
            )
            continue
        if current is None:
            continue
        if re.match(r"^\s*-\s+", line):
            current.items.append(_strip_markdown(line.strip()))

    if current is not None:
        entries.append(current)
    return entries


def parse_decisions(docs_dir: Path) -> list[Decision]:
    """Lee `docs/adr/000N-*.md` y devuelve decisiones indexadas."""
    if not docs_dir.exists():
        return []
    decisions: list[Decision] = []
    for adr_path in sorted(docs_dir.glob("*.md")):
        text = adr_path.read_text(encoding="utf-8")
        # Primer heading # ... = título
        title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else adr_path.stem
        # Body: todo entre el primer heading y el primer `## Contexto` o `## Estado`
        body = _first_paragraph(text)
        decisions.append(
            Decision(
                id=adr_path.stem,
                title=title,
                body=body,
            )
        )
    return decisions


def build_dossier_data(root: Path, catalog: Catalog) -> DossierData:
    """Compone el dataset completo que alimentará la SPA."""
    index_path = root / "INDEX.md"
    roadmap_path = root / "ROADMAP.md"
    changelog_path = root / "CHANGELOG.md"
    adr_dir = root / "docs" / "adr"

    index_toc = parse_index(index_path)
    # Complementa el TOC con los docs/ transversales
    for doc_path in sorted((root / "docs").glob("*.md")):
        if index_toc and any(
            item.path == f"docs/{doc_path.name}" for item in index_toc
        ):
            continue
        text = doc_path.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else doc_path.stem
        index_toc.append(
            TOCItem(
                path=f"docs/{doc_path.name}",
                title=title,
                summary=_first_paragraph(text),
                section="Documentación del Bloque 2",
            )
        )

    modules_data = [
        {
            "id": m.id,
            "name": m.name,
            "description": m.description,
            "type": m.type,
            "path": m.path,
            "validator": m.validator,
            "example": m.example,
            "tags": m.tags,
        }
        for m in catalog.modules
        if m.type == "module"
    ]

    return DossierData(
        generated_at=date.today().isoformat(),
        catalog_version=catalog.version,
        modules=modules_data,
        index_toc=[asdict(i) for i in index_toc],
        roadmap=[asdict(p) for p in parse_roadmap(roadmap_path)],
        changelog=[asdict(c) for c in parse_changelog(changelog_path)],
        decisions=[asdict(d) for d in parse_decisions(adr_dir)],
        stats={
            "modules_count": len(modules_data),
            "index_count": len(index_toc),
            "phases_count": len(parse_roadmap(roadmap_path)),
            "changelog_count": len(parse_changelog(changelog_path)),
            "decisions_count": len(parse_decisions(adr_dir)),
        },
    )
