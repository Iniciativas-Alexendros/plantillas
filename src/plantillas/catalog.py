"""Catálogo central de módulos, leído desde modules.yaml."""

from pathlib import Path
from typing import Any

import os

import yaml
from pydantic import BaseModel, Field, field_validator


class Module(BaseModel):
    """Entrada de un módulo en modules.yaml."""

    id: str
    name: str
    description: str
    type: str = Field(default="module")
    path: str
    validator: str | None = None
    example: str | None = None
    template: str | None = None
    tags: list[str] = Field(default_factory=list)
    init_command: str | None = None

    @field_validator("type")
    @classmethod
    def _valid_type(cls, value: str) -> str:
        allowed = {"module", "meta", "docs", "tool"}
        if value not in allowed:
            raise ValueError(f"type must be one of {allowed}")
        return value


class Catalog(BaseModel):
    """Catálogo completo de módulos."""

    version: str
    modules: list[Module]

    def by_id(self, module_id: str) -> Module | None:
        for module in self.modules:
            if module.id == module_id:
                return module
        return None

    def canonical_ids(self) -> list[str]:
        return [m.id for m in self.modules if m.type == "module"]


def _default_catalog_path() -> Path:
    candidates = [
        Path(os.environ["PLANTILLAS_CATALOG"]) if os.environ.get("PLANTILLAS_CATALOG") else None,
        Path.cwd() / "modules.yaml",
        Path(__file__).resolve().parents[2] / "modules.yaml",
    ]
    for candidate in candidates:
        if candidate is not None and candidate.exists():
            return candidate
    return Path(__file__).resolve().parents[2] / "modules.yaml"


def load_catalog(path: Path | None = None) -> Catalog:
    """Carga modules.yaml desde la ruta indicada, cwd o la raíz del repo."""

    if path is None:
        path = _default_catalog_path()

    if not path.exists():
        raise FileNotFoundError(f"modules.yaml not found at {path}")

    data: Any = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Catalog(**data)
