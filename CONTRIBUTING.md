# Cómo contribuir al Sistema de Plantillas

Gracias por interesarte en mejorar este ecosistema. Este documento define cómo
añadir módulos, validadores, y mejoras al sistema.

---

## Antes de empezar

1. Lee `ROADMAP.md` para entender el plan y evitar duplicar trabajo.
2. Abre un issue describiendo el problema o la propuesta.
3. Si es una decisión arquitectónica, documenta la ADR en `docs/adr/`.
4. Instala los pre-commit hooks: `pip install pre-commit && pre-commit install`
5. (Bloque 2) Instala el paquete en modo editable: `uv pip install -e .` o `pip install -e .`

## Convenciones de commits y PRs

- **Título del PR**: sigue [Conventional Commits](https://www.conventionalcommits.org/):
  ```
  tipo(alcance)?: descripción
  ```
  Tipos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `ci`, `chore`
  Ejemplo: `feat(agentes): añade validador de subagentes`
- **Tamaño del PR**: máximo ~500 líneas cambiadas. Divide PRs grandes.
- **CHANGELOG**: si modificas módulos o validadores, actualiza `CHANGELOG.md`.
- **Archivos protegidos** (bloquean PR Guardian si los modificas): `INDEX.md`, `README.md`, `CONTRIBUTING.md`, `ROADMAP.md`, `CHANGELOG.md`, `INTEGRACION.md`, `CODE_OF_CONDUCT.md`, `claude-init`, `update.sh`, `validadores/base.py`. Si necesitas modificarlos, discútelo primero en un issue.
- **Configuración operativa** (modificable en PRs de lint/CI sin issue previo): `install.sh`, `.pre-commit-config.yaml`. Siguen exigiendo entrada en `CHANGELOG.md` y revisión.

## Checks automáticos (CI/CD)

Todo PR debe pasar:

1. **CI Global** (`ci-global.yml`): lint de YAML, JSON, Markdown, Python (`ruff`), Shell (`shellcheck`), y estructura del repo (`validar_repo.py`).
2. **Guardián de PRs** (`pr-guardian.yml`): título válido, tamaño razonable, archivos protegidos no tocados, CHANGELOG actualizado.
3. **Security Scan** (`security-scan.yml`): sin secrets, tokens ni archivos prohibidos en el repo.
4. **Validación de módulos** (`validar-todos.yml`): todos los ejemplos pasan `--strict`.
5. **Pre-commit hooks** (local): idénticos a CI para detectar problemas antes de pushear.

---

## Estructura de un módulo

Todo módulo sigue este patrón estricto:

```
<modulo>/
├── plantilla_<modulo>/          ← Playbook instructivo (qué poner)
│   └── [ARCHIVO_PRINCIPAL].md
├── ejemplo_<modulo>/            ← Referencia funcional (cómo se ve)
│   └── [archivos operativos]
├── validar_<modulo>.py          ← Validador usando el motor reusable
└── .github/
    └── workflows/
        └── validar-<modulo>.yml ← CI/CD del módulo
```

### Reglas de naming

- Directorio del módulo: `kebab-case` (ej: `agent-config`).
- Plantilla: `plantilla_<modulo>`.
- Ejemplo: `ejemplo_<modulo>`.
- Validador: `validar_<modulo>.py`.
- Entrada en `modules.yaml` (Bloque 2): `name`, `validator`, `example`, `template`, `type`.

---

## Cómo añadir un nuevo módulo

### 1. Crea la estructura

```bash
mkdir -p <modulo>/plantilla_<modulo> <modulo>/ejemplo_<modulo> <modulo>/.github/workflows
```

### 2. Crea el playbook instructivo

En `plantilla_<modulo>/[ARCHIVO].md`:

- Explica qué es este componente de Claude Code.
- Describe la estructura de archivos.
- Incluye placeholders `[ASÍ]` para personalizar.
- Referencia a docs oficiales de Anthropic/OpenAI/MCP.

### 3. Crea el ejemplo funcional

En `ejemplo_<modulo>/`:

- Elimina todos los placeholders del playbook.
- Rellena con contenido real y funcional.
- Debe pasar el validador con `--strict`.

### 4. Crea el validador

En `validar_<modulo>.py`:

```python
from plantillas.validators import BaseValidator, Check, registry, check_estructura

@registry.register("mi-modulo")
class MiModuloValidator(BaseValidator):
    def __init__(self, ruta, strict=False):
        super().__init__(ruta, strict)
        self.checks = [
            Check("estructura", self._check_estructura),
            # ... tus checks
        ]
    # ... métodos de check
```

> **Compatibilidad durante la transición:** los validadores actuales aún usan
> `sys.path.insert` para importar `validadores/` de la raíz. En el Bloque 2 se
> migran a imports absolutos del paquete instalado y se registran con el
> decorador `@registry.register("<modulo>")`.

Reglas del validador:

- Usa `BaseValidator` y los checks del motor reusable.
- Mínimo 3 checks: estructura, contenido, placeholders.
- Debe devolver código de salida 0 (OK) o 1 (fallo).
- Soporta `--strict` (warnings = errores).
- (Bloque 2) Regístralo en `src/plantillas/validators/registry.py` y añade el módulo a `modules.yaml`.

### 5. Crea el workflow CI/CD

En `.github/workflows/validar-<modulo>.yml`:

- Copia cualquier workflow existente y adapta paths.
- Debe descubrir ejemplos automáticamente.
- Ejecuta el validador con `--strict`.

### 6. Actualiza el sistema

- Añade el módulo a `INDEX.md` (tabla y estructura visual).
- Añade el módulo a `modules.yaml` (Bloque 2): fuente de verdad para CI, pre-commit y tests.
- Añade a `ROADMAP.md` si es parte de una fase activa.
- Ejecuta `python validar_<modulo>.py ejemplo_<modulo>/ --strict`.
- (Bloque 2) Ejecuta `plantillas validate <modulo> --strict`.
- Ejecuta el workflow central: actúa como smoke test.

---

## Convenciones de código

### Python (validadores)

- Python 3.12+.
- Nombres en español (el sistema es bilingüe español/inglés en output).
- Clases: `PascalCase`.
- Funciones/variables: `snake_case`.
- Imports absolutos del paquete `plantillas` (Bloque 2); `sys.path.insert` queda como legacy.

### Markdown

- Archivos en raíz de módulo: `MAYÚSCULAS.md`.
- Archivos en subdirectorios: `minúsculas.md`.
- Frontmatter YAML en archivos de manifest (`AGENT.md`, `SKILL.md`, etc.).

### YAML/JSON

- 2 espacios de indentación.
- Sin tabs.
- Comillas dobles para strings con caracteres especiales.

---

## Commits

Usamos Conventional Commits:

```
feat(agentes): añade validador de subagentes
fix(skills): corrige regex de placeholders
docs(hooks): actualiza referencias a docs oficiales
ci(global): añade composite action reusable
test(mcp): añade tests de integración
```

---

## Testing

Antes de enviar un PR:

```bash
# Validar tu módulo
python <modulo>/validar_<modulo>.py <modulo>/ejemplo_<modulo>/ --strict

# Validar todos los módulos (actual)
python validar_repo.py --strict

# Validar todos los módulos (Bloque 2)
plantillas validate --all --strict

# Smoke test: copiar plantilla y validar
cp -r plantilla_<modulo> /tmp/test-modulo
python validar_<modulo>.py /tmp/test-modulo --strict || true
```

---

## Contacto

- Issues: GitHub Issues
- Discusiones: GitHub Discussions
- Email: contacto@alexendros.me
