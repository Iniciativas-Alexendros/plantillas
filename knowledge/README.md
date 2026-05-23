# Knowledge · Base de conocimiento autoritative de Claude Code

> Módulo canon añadido en la reforma `canon-runtime alignment` (2026-05-23).
> Un **artículo KB** es contenido verificado, con autoridad declarada, que
> otros agentes y skills pueden citar de forma estable. A diferencia de los
> cuadernos (notas de trabajo) y autoresearch (investigaciones exploratorias),
> un knowledge artifact vive cuando el contenido ya fue validado y se va a
> referenciar repetidamente.

## Qué es

Un artículo KB encapsula:

1. **Descriptor + contenido** (`<slug>.md`) — frontmatter canon con metadatos
   de autoridad + cuerpo estructurado en 5 secciones obligatorias.

El artículo vive en `~/.claude/knowledge/<slug>/<slug>.md` y es referenciable
desde skills, agentes y commands usando el slug como identificador estable.

## Cuándo crear un artículo KB

Crea un artículo KB (y no un cuaderno ni un autoresearch) cuando:

- El contenido ya fue verificado y no va a cambiar pronto.
- Otros agentes/skills lo citarán de forma explícita (ej. `related_skills:`).
- La información tiene una fuente authoritative (documentación oficial, RFC,
  especificación formal).
- Quieres que el contenido sea indexable y buscable con slug estable.

## Ciclo de vida · statuses

| Status      | Significado |
|-------------|-------------|
| `draft`     | Borrador inicial. Puede carecer de referencias. No citar todavía. |
| `review`    | Listo para revisión. Contenido completo, en espera de validación. |
| `published` | Verificado y citeable. Requiere al menos 1 reference en frontmatter. |
| `deprecated`| Obsoleto. El validador emite warning al validarlo. Considerar reemplazar. |

## Authority · niveles de confianza

| Authority    | Significado |
|--------------|-------------|
| `official`   | Basado directamente en documentación oficial de Anthropic, RFCs u otros estándares normativos. |
| `community`  | Derivado de prácticas consolidadas de la comunidad, no de fuentes primarias. |
| `inferred`   | Deducido por el operador a partir de observaciones; puede contener imprecisiones. |

## Crear un artículo KB nuevo

```bash
# 1. Copiar plantilla
cp knowledge/plantilla_knowledge.md ~/.claude/knowledge/<slug>/<slug>.md

# 2. Editar placeholders (en MAYÚSCULAS-CON-GUIONES)
#    - name: slug kebab-case
#    - domain: área de conocimiento (ej. claude-code-internals, devops, legal-rgpd)
#    - references: mínimo 1 si status == "published"
#    - Rellenar las 5 secciones obligatorias

# 3. Validar antes de publicar
python knowledge/validar_knowledge.py ~/.claude/knowledge/<slug>/<slug>.md --strict
```

## Validador

`validar_knowledge.py` comprueba:

- **formato**: el archivo existe y termina en `.md`.
- **frontmatter**: campos obligatorios `name`, `description`, `domain`,
  `references`, `status`, `last_updated`, `authority`.
- **status**: pertenece a `{draft, review, published, deprecated}`.
- **authority**: pertenece a `{official, community, inferred}`.
- **domain**: kebab-case obligatorio (minúsculas, dígitos, guiones).
- **references**: lista no vacía si `status == "published"` (ERROR);
  vacía en `draft` o `review` emite warning.
- **related_skills**: si presente, lista de identificadores válidos.
- **last_updated**: formato ISO-8601 (`YYYY-MM-DD`).
- **name_kebab**: warning en plantilla (placeholder); error en artículo real.
- **secciones**: `## Resumen`, `## Contenido`, `## Aplicación`,
  `## Limitaciones`, `## Referencias` — todas ERROR si faltan.
- **coherencia_referencias**: warning si la sección `## Referencias` no
  reproduce al menos el 50% de las referencias del frontmatter.
- **placeholders**: warning si el artículo (no plantilla) contiene
  placeholders sin rellenar.
- **deprecated_status**: warning explícito si `status == "deprecated"`.
- **modo legado**: si recibe un directorio, usa el primer `.md` y avisa.

## Integración con `COM_articulo-kb`

La skill `COM_articulo-kb` genera un borrador de artículo KB a partir de
una fuente de conocimiento (URL, documento, conversación). El artículo
resultante sigue este módulo como contrato de formato y se deposita en
`~/.claude/knowledge/<slug>/`.

## Diferencia con otros módulos

| Módulo         | Propósito | Mutabilidad | Autoridad |
|----------------|-----------|-------------|-----------|
| `knowledge/`   | Artículos KB citables, verificados | Baja (publicado = estable) | Declarada en frontmatter |
| `cuadernos/`   | Notas de trabajo del operador | Alta | Personal / informal |
| `autoresearch/`| Investigaciones exploratorias | Media | Inferred / en progreso |

## Anti-patrones

- Usar `knowledge/` para notas temporales (usar `cuadernos/`).
- Marcar como `published` sin references (el validador lo rechaza).
- Poner `authority: official` en contenido inferido sin fuente primaria.
- Crear slugs con mayúsculas o espacios (`domain` y `name` deben ser kebab-case).
- Omitir la sección `## Limitaciones` aunque el artículo no tenga ninguna
  (escribir `- Ninguna conocida a la fecha.` es válido).

## Referencias

- Plantilla canon · `knowledge/plantilla_knowledge.md`
- Ejemplo funcional · `knowledge/ejemplo_knowledge.md`
- Skill `COM_articulo-kb` · `~/.claude/skills/COM_articulo-kb/SKILL.md`
- Módulo `cuadernos/` · `cuadernos/README.md`
- Módulo `autoresearch/` · `autoresearch/README.md`
