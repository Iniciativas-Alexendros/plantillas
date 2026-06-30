# Diagramas de arquitectura del Bloque 2

Vista gráfica del paquete `plantillas`, su catálogo y el flujo de validación.

## 1. Arquitectura general

```mermaid
flowchart TB
    subgraph Usuario
        U[CLI plantillas]
    end

    subgraph Paquete
        CLI[plantillas.cli]
        CAT[plantillas.catalog]
        REG[plantillas.registry]
        VAL[plantillas.validators.*]
    end

    subgraph Repo
        MY[modules.yaml]
        MOD[Módulos canónicos]
        LEG[validar_*.py legacy]
        VRP[validar_repo.py]
    end

    U --> CLI
    CLI --> CAT
    CLI --> REG
    CAT --> MY
    REG --> VAL
    REG --> LEG
    MY --> MOD
    MOD --> LEG
    VRP --> MY
    VRP --> MOD
```

## 2. Flujo de validación

```mermaid
sequenceDiagram
    actor U as Usuario
    participant CLI as plantillas.cli
    participant CAT as plantillas.catalog
    participant REG as plantillas.registry
    participant VAL as Validador embebido o legacy

    U->>CLI: plantillas validate [módulo]
    CLI->>CAT: load_catalog()
    CAT-->>CLI: Catalog
    CLI->>REG: discover_validators(catalog)
    REG->>REG: Intentar importar plantillas.validators.<id>
    alt Embebido disponible
        REG-->>CLI: Función registrada
    else Solo legacy
        REG-->>CLI: Script registrado
    end
    CLI->>REG: validate(module_id, module, root)
    REG->>VAL: Ejecutar validador
    VAL-->>REG: ValidationResult
    REG-->>CLI: ValidationResult
    CLI-->>U: ✅ / ❌ por módulo
```

## 3. Estructura del paquete

```mermaid
graph LR
    py[pyproject.toml] --> src[src/plantillas]
    src --> init[__init__.py]
    src --> main[__main__.py]
    src --> catalog[catalog.py]
    src --> cli[cli.py]
    src --> registry[registry.py]
    src --> validators[validators/]
    validators --> val_init[__init__.py]
    validators --> agent_config[agent_config.py]
    cli --> catalog
    cli --> registry
    registry --> catalog
    registry --> validators
```

## 4. Mapa de módulos

```markdown
- Sistema de Plantillas
  - Bloque 2
    - Paquete Python
      - CLI `plantillas`
      - Catálogo `modules.yaml`
      - Registry de validadores
    - Módulos canónicos
      - agent-config
      - agentes
      - artefactos
      - commands
      - estandares
      - hooks
      - mcp
      - miniapps
      - modulo
      - plugins
      - proyecto
      - repositorios
      - skills
    - Documentación
      - ADRs
      - CLI
      - modules-yaml
      - validators
```

## 5. Pipeline de calidad

```mermaid
flowchart LR
    A[push/PR] --> B[CI plantillas]
    B --> C[ruff check]
    B --> D[pytest]
    B --> E[plantillas validate]
    C --> F{¿todo verde?}
    D --> F
    E --> F
    F -->|sí| G[mergeable]
    F -->|no| H[revisar]
```
