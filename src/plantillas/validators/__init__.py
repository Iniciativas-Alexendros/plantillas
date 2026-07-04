"""Validadores embebidos del paquete `plantillas`.

Cada submódulo expone una función `validate(module, root) -> ValidationResult`
que el `ValidatorRegistry` descubre automáticamente por convención.
"""

from .agent_config import validate as validate_agent_config

__all__ = ["validate_agent_config"]
