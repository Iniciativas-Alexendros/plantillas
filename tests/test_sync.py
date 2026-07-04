"""Tests para el módulo `plantillas.sync`."""

from pathlib import Path

import pytest

from plantillas.catalog import Catalog, Module
from plantillas.sync import (
    SYNCABLE_MODULE_IDS,
    execute_sync,
    resolve_module_id,
)


def _make_catalog() -> Catalog:
    return Catalog(
        version="test",
        modules=[
            Module(
                id="skills",
                name="Skills",
                description="",
                type="module",
                path="skills",
            ),
            Module(
                id="agentes",
                name="Agentes",
                description="",
                type="module",
                path="agentes",
            ),
            Module(
                id="commands",
                name="Commands",
                description="",
                type="module",
                path="commands",
            ),
        ],
    )


def test_resolve_module_id_canonical():
    assert resolve_module_id("skills") == "skills"
    assert resolve_module_id("agents") == "agentes"
    assert resolve_module_id("agentes") == "agentes"


def test_resolve_module_id_unknown():
    with pytest.raises(ValueError):
        resolve_module_id("no-existe")


def test_status_reports_drift(tmp_path: Path, monkeypatch):
    # Layout: <tmp>/.config/opencode/skills/<instance>/
    home = tmp_path
    (home / ".config/opencode/skills/orphan").mkdir(parents=True)
    (home / ".config/opencode/skills/orphan/SKILL.md").write_text("# orphan")

    # Layout: <tmp>/plantillas/skills/<existing>/
    root = tmp_path / "plantillas"
    (root / "skills/existing").mkdir(parents=True)
    (root / "skills/existing/SKILL.md").write_text("# existing")

    monkeypatch.setenv("HOME", str(home))
    report = execute_sync(
        module_id="skills",
        target="opencode",
        direction="status",
        catalog=_make_catalog(),
        root=root,
    )

    assert report.ok
    assert len(report.drifted) == 1
    assert report.drifted[0].name == "orphan"
    assert report.promoted == []


def test_push_copies_instances(tmp_path: Path, monkeypatch):
    home = tmp_path
    (home / ".config/opencode/skills").mkdir(parents=True)

    root = tmp_path / "plantillas"
    src = root / "skills/mi-skill"
    src.mkdir(parents=True)
    (src / "SKILL.md").write_text("---\nname: mi-skill\n---\n")

    monkeypatch.setenv("HOME", str(home))
    report = execute_sync(
        module_id="skills",
        target="opencode",
        direction="push",
        catalog=_make_catalog(),
        root=root,
        assume_yes=True,
    )

    assert report.ok
    assert (home / ".config/opencode/skills/mi-skill/SKILL.md").exists()
    assert len(report.promoted) == 1


def test_push_skips_existing_without_yes(tmp_path: Path, monkeypatch):
    home = tmp_path
    (home / ".config/opencode/skills/mi-skill").mkdir(parents=True)
    (home / ".config/opencode/skills/mi-skill/SKILL.md").write_text("old")

    root = tmp_path / "plantillas"
    src = root / "skills/mi-skill"
    src.mkdir(parents=True)
    (src / "SKILL.md").write_text("new")

    monkeypatch.setenv("HOME", str(home))
    report = execute_sync(
        module_id="skills",
        target="opencode",
        direction="push",
        catalog=_make_catalog(),
        root=root,
        assume_yes=False,
    )

    assert report.ok
    assert len(report.skipped) == 1
    assert (home / ".config/opencode/skills/mi-skill/SKILL.md").read_text() == "old"


def test_pull_imports_drift(tmp_path: Path, monkeypatch):
    home = tmp_path
    (home / ".config/opencode/skills/orphan").mkdir(parents=True)
    (home / ".config/opencode/skills/orphan/SKILL.md").write_text("# drift")

    root = tmp_path / "plantillas"
    (root / "skills").mkdir(parents=True)

    monkeypatch.setenv("HOME", str(home))
    report = execute_sync(
        module_id="skills",
        target="opencode",
        direction="pull",
        catalog=_make_catalog(),
        root=root,
        assume_yes=True,
    )

    assert report.ok
    assert (root / "skills/_imported/orphan/SKILL.md").exists()
    assert len(report.promoted) == 1


def test_agents_alias_resolves_to_agentes():
    assert resolve_module_id("agents") == "agentes"
    assert "agentes" in SYNCABLE_MODULE_IDS
