# Miniapps · SPA autocontenidas tipo Claude.ai artifact

> Módulo canon añadido en la reforma `canon-runtime alignment` (2026-05-23).
> Una **mini-app** es un artefacto HTML single-file (CSS y JS inline) que el
> operador abre directamente en navegador, sin build-step, sin servidor y sin
> dependencias externas no auditadas. Sustituye a los antiguos "playgrounds"
> sueltos en `artefactos/playgrounds/` cuando la mini-app es reutilizable y
> merece vivir bajo `~/.claude/miniapps/`.

## Qué es

Una mini-app encapsula tres cosas:

1. **Descriptor** (`<slug>.md`) — frontmatter canon + propósito + uso.
2. **HTML opcional** (`<slug>.html`) — la SPA en sí (cuando existe).
3. **Datos opcionales** (`<slug>.json` o inline) — estado que renderiza.

Para encajar en el canon, el `.md` cumple el formato de `plantilla_miniapps.md`
y supera `validar_miniapps.py`.

## Uso

### Crear una mini-app nueva

```bash
cp miniapps/plantilla_miniapps.md ~/.claude/miniapps/<slug>/<slug>.md
# Editar el .md (placeholders en MAYÚSCULAS-CON-GUIONES)
# (Opcional) Crear ~/.claude/miniapps/<slug>/<slug>.html
python miniapps/validar_miniapps.py ~/.claude/miniapps/<slug>/<slug>.md --strict
```

### Categorías permitidas

- `dashboard` — KPIs / métricas (ej.: `kpi-mensual`).
- `explorer` — navegación por estructura (árbol, tabla, diff).
- `tool` — herramienta interactiva (generador, calculadora).
- `playbook` — documento interactivo con tabs + prompt-dock.

### Runtimes permitidos

- `browser` — single-file HTML offline-safe (default).
- `electron` — empaquetado escritorio.
- `static` — multi-archivo servido por nginx / CDN.

## Validador

`validar_miniapps.py` comprueba:

- Frontmatter con campos `name`, `description`, `category`, `runtime`,
  `version`, `last_updated`.
- `category` y `runtime` dentro del set válido.
- `version` SemVer (X.Y.Z) y `last_updated` ISO-8601 (YYYY-MM-DD).
- `name` en kebab-case (warning en plantillas con placeholders).
- Secciones cuerpo `## Propósito` y `## Cuándo usar`.
- Si existe `<slug>.html` adjunto: JS externo sin SRI (warning) y
  detección heurística de secretos embebidos (error).

## Integración con otros módulos

- Cuando un **skill** entrega una visualización reutilizable, se materializa
  como mini-app y el skill referencia el slug.
- Los **playgrounds** efímeros viven en `artefactos/playgrounds/` y NO usan
  este módulo; solo se promueve a mini-app la versión estable.
- Los **dossiers** de mayor tamaño se quedan en `artefactos/dossiers/`.

## Anti-patrones

- Cargar `react` / `vue` / `tailwind` desde CDN sin SRI.
- Requerir `npm install` o build-step.
- Embeber secretos / tokens en el HTML.
- Usar `localStorage` con claves no prefijadas (riesgo de colisión).

## Referencias

- Plantilla canon · `plantilla_miniapps.md`
- Ejemplo funcional · `ejemplo_miniapps.md`
- Skill `CREA_playground` · `~/.claude/skills/CREA_playground/SKILL.md`
- Patrón VAP (Vergina + sepia↔nocturno) · `~/.claude/CLAUDE.md` §6 bis
