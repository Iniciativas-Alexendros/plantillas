# Cuadernos · Notas estructuradas del operador

> Módulo canon añadido en la reforma `canon-runtime alignment` (2026-05-23).
> Un **cuaderno** es una nota estructurada con anclaje semántico: idea,
> log, decisión o playbook. A diferencia de `autoresearch/` (cuya finalidad
> es investigar fuentes externas), los cuadernos capturan pensamiento propio
> del operador, decisiones de proyecto o procedimientos repetibles.
> Viven en `~/.claude/cuadernos/<slug>/<slug>.md`.

## Qué es

Un cuaderno encapsula pensamiento estructurado en tres bloques:

1. **Frontmatter** (`name`, `description`, `kind`, `tags`, `last_updated`, `status`).
2. **Secciones obligatorias** (`## Contexto`, `## Contenido`, `## Referencias`).
3. **Secciones recomendadas** según el `kind` elegido.

Para encajar en el canon, el `.md` cumple el formato de `plantilla_cuadernos.md`
y supera `validar_cuadernos.py`.

## Uso

### Crear un cuaderno nuevo

```bash
cp cuadernos/plantilla_cuadernos.md ~/.claude/cuadernos/<slug>/<slug>.md
# Editar el .md: rellenar placeholders, elegir kind, añadir secciones
python cuadernos/validar_cuadernos.py ~/.claude/cuadernos/<slug>/<slug>.md --strict
```

### Kinds permitidos

| Kind       | Propósito                                          | Secciones recomendadas adicionales                              |
| ---------- | -------------------------------------------------- | --------------------------------------------------------------- |
| `idea`     | Captura una idea o hipótesis en desarrollo         | `## Hipótesis`, `## Próximos pasos`                             |
| `log`      | Registro cronológico de eventos o avances          | `## Eventos` (con timestamps)                                   |
| `decision` | Documenta una decisión y su razonamiento           | `## Decisión`, `## Alternativas consideradas`, `## Consecuencias` |
| `playbook` | Procedimiento repetible paso a paso                | `## Pasos`, `## Cuándo aplicar`                                 |

### Statuses permitidos

- `draft` — cuaderno en construcción, puede tener lagunas.
- `active` — cuaderno vigente, consultable en producción.
- `archived` — cuaderno obsoleto, se mantiene por trazabilidad.

## Frontmatter mínimo

```yaml
---
name: nombre-cuaderno-kebab
description: >
  1-3 líneas resumiendo qué captura este cuaderno.
kind: decision
tags:
  - arquitectura
last_updated: 2026-05-23
status: active
---
```

- `name`: kebab-case obligatorio en cuadernos activos.
- `tags`: lista no vacía, cada elemento kebab-case.
- `last_updated`: formato ISO-8601 `YYYY-MM-DD`.

## Validador

`validar_cuadernos.py` comprueba:

- **Formato**: el archivo existe y termina en `.md`.
- **Frontmatter**: campos obligatorios `name`, `description`, `kind`, `tags`,
  `last_updated`, `status`.
- **Kind**: pertenece a `{idea, log, decision, playbook}` (ERROR si inválido).
- **Status**: pertenece a `{draft, active, archived}` (ERROR si inválido).
- **Tags**: lista no vacía; cada elemento string kebab-case (ERROR si inválido).
- **last_updated**: formato ISO-8601 `YYYY-MM-DD` (ERROR si inválido).
- **name_kebab**: `name` es kebab-case (WARNING en plantilla, ERROR en ejemplo).
- **Secciones obligatorias**: `## Contexto`, `## Contenido`, `## Referencias`
  (ERROR si faltan).
- **Secciones recomendadas**: según `kind` (WARNING si faltan).
- **Placeholders**: detecta texto sin rellenar (WARNING en archivos que no son
  plantillas).
- **Modo legado**: si recibe un directorio, usa el primer `.md` encontrado
  y emite warning para guiar al operador hacia la convención single-file.

## Integración con skills

- **`EVO_autoresearch`**: cuando una sesión de investigación concluye con
  una decisión, el operador puede materializar el razonamiento como cuaderno
  `kind: decision` para preservarlo fuera de la conversación.
- **`COM_coautoria`**: en proyectos de co-autoría, los cuadernos `kind: log`
  funcionan como bitácora compartida de hitos y acuerdos.
- **`PRODUCTO_roadmap`**: las decisiones de producto documentadas como
  cuadernos `kind: decision` se pueden referenciar desde el roadmap.
- **`DEV_arquitectura`**: las decisiones técnicas relevantes (ADR) encajan
  naturalmente como cuadernos `kind: decision`.

## Anti-patrones

- Usar cuadernos para guardar salidas brutas de `EVO_autoresearch` sin
  estructurar — para eso están los artefactos en `artefactos/dossiers/`.
- Duplicar información que ya vive en el CLAUDE.md del proyecto; los
  cuadernos capturan el *razonamiento*, no la configuración.
- Crear un cuaderno `kind: playbook` con pasos vagos o no accionables.
- Mezclar múltiples decisiones no relacionadas en un solo cuaderno.
- Dejar `status: draft` indefinidamente en cuadernos que se usan como
  referencia activa.

## Referencias

- Plantilla canon · `plantilla_cuadernos.md`
- Ejemplo funcional · `ejemplo_cuadernos.md`
- Skill `EVO_autoresearch` · `~/.claude/skills/EVO_autoresearch/SKILL.md`
- Skill `COM_coautoria` · `~/.claude/skills/COM_coautoria/SKILL.md`
- Validador global · `validar_repo.py`
