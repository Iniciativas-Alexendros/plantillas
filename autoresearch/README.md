# Autoresearch · Cuadernos de auto-investigación

> Módulo canon añadido en la reforma `canon-runtime alignment` (2026-05-23).
> Un **cuaderno de auto-investigación** es una nota estructurada que documenta
> una pregunta, las fuentes consultadas, los hallazgos y un veredicto accionable.
> Vive bajo `~/.claude/autoresearch/<slug>/<slug>.md` y se genera o actualiza
> típicamente por la skill `EVO_autoresearch`.

## Qué es

Un cuaderno de autoresearch encapsula tres cosas:

1. **Frontmatter canon** (`name`, `description`, `topic`, `sources`, `status`,
   `last_updated`, `confidence`) — metadatos indexables y consultables.
2. **Cuerpo estructurado** — cinco secciones obligatorias: `## Pregunta`,
   `## Fuentes`, `## Hallazgos`, `## Veredicto`, `## Pendientes`.
3. **Ciclo de vida controlado** — el campo `status` (`draft → review → published
   → archived`) y `confidence` (0.0–1.0) permiten conocer de un vistazo la
   madurez y fiabilidad del veredicto.

## Uso

### Crear un cuaderno nuevo

```bash
slug="mi-investigacion"
mkdir -p ~/.claude/autoresearch/${slug}
cp autoresearch/plantilla_autoresearch.md ~/.claude/autoresearch/${slug}/${slug}.md
# Editar el .md (sustituir placeholders MAYUSCULA-CON-GUION)
python autoresearch/validar_autoresearch.py ~/.claude/autoresearch/${slug}/${slug}.md --strict
```

### Validar un cuaderno existente

```bash
python autoresearch/validar_autoresearch.py autoresearch/ejemplo_autoresearch.md --strict
```

### Actualizar desde la skill EVO_autoresearch

La skill actualiza `## Hallazgos`, `## Veredicto` y los campos `confidence`,
`last_updated`, `sources` del frontmatter. El operador revisa y promueve
`status: draft` → `review` → `published` manualmente o vía hook.

## Statuses

| Status | Significado | `sources` mínimas |
|--------|-------------|-------------------|
| `draft` | Borrador inicial; puede no tener fuentes externas | 0 |
| `review` | En revisión por el operador; requiere fuentes verificadas | 1 |
| `published` | Veredicto estable y accionable | 1 |
| `archived` | Información superada o ya no relevante | 0 |

## Confidence

Escala continua 0.0–1.0:

- `0.0–0.3` — hipótesis sin fuentes sólidas.
- `0.4–0.6` — hallazgos preliminares, pendiente verificación.
- `0.7–0.85` — veredicto bien fundamentado con fuentes primarias.
- `0.9–1.0` — certeza alta; múltiples fuentes concordantes + experimentos.

## Validador

`validar_autoresearch.py` comprueba:

- **formato** — archivo existe y termina en `.md`.
- **frontmatter** — campos obligatorios presentes y YAML válido.
- **status** — pertenece a `{draft, review, published, archived}`.
- **confidence** — float en rango 0.0–1.0.
- **sources** — lista YAML; mínimo 1 en `review`/`published`; URLs con esquema
  `http(s)://` o rutas absolutas.
- **last_updated** — formato ISO-8601 (`YYYY-MM-DD`).
- **name_kebab** — kebab-case; downgradeado a WARNING en plantillas.
- **secciones** — presencia de `## Pregunta`, `## Fuentes`, `## Hallazgos`,
  `## Veredicto`, `## Pendientes`.
- **placeholders** — skipped en plantillas; ERROR en ejemplos con tokens
  `MAYUSCULA-CON-GUION` sin reemplazar.
- **coherencia_sources** — warning si alguna URL del frontmatter no aparece en
  la sección `## Fuentes`.
- **modo legado** — si se pasa un directorio, toma el primer `.md` y emite
  warning.

Usa `--strict` para tratar warnings como errores (recomendado en CI).

## Integración con skills

- **`EVO_autoresearch`** — genera o actualiza un cuaderno a partir de una
  pregunta. Actualiza frontmatter + secciones. Llama al validador antes de
  escribir el resultado final.
- **`EVO_recomendar-automatizacion`** — puede sugerir la apertura de un cuaderno
  cuando detecta una pregunta recurrente sin respuesta canónica.
- **`DATOS_analizar`** y **`PRODUCTO_investigar`** — pueden referenciar cuadernos
  publicados como fuente secundaria en lugar de re-investigar.

## Anti-patrones

- Escribir `status: published` con `confidence < 0.5` — el veredicto no está
  maduro; usar `review` hasta completar fuentes.
- Dejar placeholders `MAYUSCULA-CON-GUION` sin reemplazar en un cuaderno de
  estado `published` — el validador lo detectará como warning.
- Omitir URLs reales en el frontmatter `sources:` — hace inauditable el veredicto.
- Mezclar opinión con hallazgo en `## Hallazgos` — los hallazgos deben ser
  verificables; la opinión va en `## Veredicto`.
- Crear un cuaderno para cada búsqueda efímera — reservar para preguntas que
  se repetirán o que requieren decisiones arquitectónicas.

## Referencias

- Plantilla canon · `autoresearch/plantilla_autoresearch.md`
- Ejemplo funcional · `autoresearch/ejemplo_autoresearch.md`
- Skill `EVO_autoresearch` · `~/.claude/skills/EVO_autoresearch/SKILL.md`
- Memorias vivas · `~/.claude/projects/-var-home-soyalexendros/memory/MEMORY.md`
