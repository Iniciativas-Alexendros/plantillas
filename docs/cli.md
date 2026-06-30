# CLI `plantillas`

La CLI unificada del Bloque 2 orquesta validación, sincronización y creación de módulos.

## Instalación

```bash
pip install -e .
# o, en entorno virtual:
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

El punto de entrada es `plantillas`.

## Comandos

### `plantillas validate [MODULE]`

Valida un módulo o todos los módulos canónicos registrados en `modules.yaml`.

```bash
plantillas validate
plantillas validate agentes
plantillas validate --no-strict
```

### `plantillas config`

Muestra la versión del catálogo y la lista de módulos canónicos.

```bash
plantillas config
```

### `plantillas version`

Muestra la versión del paquete.

```bash
plantillas version
```

### `plantillas sync <MODULE>` *(en desarrollo)*

Sincroniza un módulo desde su fuente canónica. El caso de uso principal es `plantillas sync agent-config`, que regenerará los artefactos de configuración cross-platform.

### `plantillas new <NAME> --type <TYPE>` *(en desarrollo)*

Crea un nuevo módulo a partir de la plantilla base.

## Códigos de salida

| Código | Significado |
|--------|-------------|
| 0 | Éxito |
| 1 | Error de validación o módulo desconocido |
| 2 | Error interno no controlado |

## Tests

La CLI se testea con `typer.testing.CliRunner`:

```bash
pytest tests/test_cli.py -v
```
