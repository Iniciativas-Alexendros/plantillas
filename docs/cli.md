# CLI `plantillas` — Bloque 2

> Estado: propuesto / en implementación. Los comandos aún no están disponibles
> en `main`; se activarán a medida que avancen las fases del Bloque 2.

## Instalación

```bash
uv pip install -e .
# o
pip install -e .
```

## Comandos

### `plantillas validate`

Ejecuta validadores sobre módulos.

```bash
# Validar todos los módulos canónicos
plantillas validate --all --strict

# Validar un módulo concreto
plantillas validate agentes --strict

# Salida JSON para CI
plantillas validate --all --format json

# Salida compatible con GitHub Actions (annotations)
plantillas validate --all --format github
```

### `plantillas sync`

Sincroniza la configuración cross-platform desde `plantilla_agent_config.yaml`.

```bash
# Generar artefactos en $HOME con backup
plantillas sync agent-config --home ~ --backup

# Dry-run: muestra diff sin escribir
plantillas sync agent-config --dry-run

# Generar solo el directorio de ejemplo
plantillas sync agent-config --target ejemplo_agent_config/
```

### `plantillas new`

Genera la estructura de un nuevo módulo a partir de un template base.

```bash
plantillas new agente --nombre mi-agente
plantillas new skill --nombre mi-skill
plantillas new hook --nombre mi-hook
plantillas new repositorio --nombre mi-repo
plantillas new modulo --nombre mi-modulo
```

### `plantillas config`

Consulta el catálogo de módulos.

```bash
plantillas config list
plantillas config get agentes
plantillas config check  # valida que modules.yaml sea consistente
```

## Códigos de salida

- `0`: todo OK.
- `1`: errores de validación o fallo de sync.
- `2`: error de uso / argumentos inválidos.
