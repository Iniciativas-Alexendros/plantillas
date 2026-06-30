from pathlib import Path

from plantillas.catalog import Module
from plantillas.registry import ValidationResult, ValidatorRegistry, discover_validators


def test_registry_register_and_run():
    registry = ValidatorRegistry()

    def dummy_validate(module: Module, root: Path) -> ValidationResult:
        return ValidationResult(module_id=module.id, ok=True, message="dummy")

    registry.register("test", dummy_validate)
    module = Module(id="test", name="Test", description="", path="test")
    result = registry.validate("test", module, Path("/tmp"))
    assert result.ok
    assert result.message == "dummy"


def test_registry_missing_validator():
    registry = ValidatorRegistry()
    module = Module(id="no-validator", name="None", description="", path="no-validator")
    result = registry.validate("no-validator", module, Path("/tmp"))
    assert result.ok
    assert result.message == "No validator configured"


def test_discover_validators_loads_agent_config():
    from plantillas.catalog import load_catalog

    catalog = load_catalog()
    registry = ValidatorRegistry()
    ids = discover_validators(registry, catalog)
    assert "agent-config" in ids
    assert "agent-config" in registry._funcs
