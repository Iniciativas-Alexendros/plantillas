# Motor de validación — Bloque 2

> Estado: propuesto / en implementación. El motor actual en `validadores/` se
> migrará a `src/plantillas/validators/`.

## Arquitectura

```
src/plantillas/validators/
├── __init__.py
├── base.py          # BaseValidator, Check, Resultado, Nivel
├── registry.py      # Registry con @register
├── checks.py        # Checks reutilizables
├── report.py        # Formateo de salida
└── modules/
    ├── agentes.py
    ├── skills.py
    ├── commands.py
    ├── hooks.py
    ├── mcp.py
    ├── plugins.py
    ├── miniapps.py
    ├── agent_config.py
    ├── repositorios.py
    ├── modulo.py
    ├── proyecto.py
    └── estandares.py
```

## Cómo crear un validador

```python
from pathlib import Path
from plantillas.validators import BaseValidator, Check, registry, check_estructura

@registry.register("mi-modulo")
class MiModuloValidator(BaseValidator):
    def __init__(self, ruta: Path, strict: bool = False):
        super().__init__(ruta, strict)
        self.checks = [
            Check("estructura", self._check_estructura),
            Check("contenido", self._check_contenido),
            Check("placeholders", self._check_placeholders),
        ]

    def _check_estructura(self):
        return check_estructura(self, {"required": ["README.md", "EJEMPLO.md"]})

    def _check_contenido(self):
        # ... lógica específica
        return []

    def _check_placeholders(self):
        # ... lógica específica
        return []
```

## Registry

```python
from plantillas.validators import registry

# Listar validadores registrados
print(registry.list_modules())

# Resolver validador
validator_cls = registry.get("agentes")
```

## Checks reutilizables

Disponibles en `plantillas.validators.checks`:

- `check_estructura`
- `check_archivos_vacios`
- `check_placeholders`
- `check_archivos_prohibidos`
- `check_tamanio_maximo`
- `check_merge_conflicts`
- `check_secrets`
- `check_gitignore_minimo`
- `check_yaml_frontmatter`
- `check_json_parseable`

## Salida de resultados

`BaseValidator.run()` devuelve una lista de `Resultado`. El reporteador soporta:

- `text`: salida humana para terminal.
- `json`: objeto JSON para CI.
- `github`: anotaciones de GitHub Actions.

## Wrappers de compatibilidad

Durante la transición, los scripts `validar_<modulo>.py` actuales se mantienen
como wrappers delgados que invocan `plantillas validate <modulo>`.
