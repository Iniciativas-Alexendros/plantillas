---
name: decision-single-file-plantillas
description: >
  Registro de la decisión de colapsar los módulos de plantillas de formato
  multi-directorio al formato single-file (.md). Consultar cuando surjan
  dudas sobre por qué los módulos ya no usan subdirectorios y por qué el
  validador global acepta ambos formatos durante la transición.
kind: decision
tags:
  - arquitectura
  - plantillas
  - canon-runtime
last_updated: 2026-05-23
status: active
---

## Contexto

El sistema de plantillas de Claude Code históricamente organizaba cada
artefacto en un subdirectorio: `plantilla_agente/AGENTE.md`,
`plantilla_agente/SKILL.md`, etc. Este formato multi-archivo era flexible
pero generaba fricción: copiar la plantilla implicaba copiar un árbol,
los validadores tenían que descubrir el archivo principal, y los ejemplos
funcionales aumentaban la profundidad de anidación innecesariamente.

En la reforma `canon-runtime alignment` (2026-05-23) se revisó si el
formato single-file era viable para todos los módulos.

## Contenido

La reforma analiza el ciclo de vida real de una plantilla en este sistema:

1. El operador ejecuta `claude-init --modulo X --nombre Y`.
2. El CLI copia el archivo `.md` (o el directorio) a `~/.claude/X/Y/`.
3. El validador del módulo (`validar_X.py`) verifica el resultado.
4. El validador global (`validar_repo.py`) verifica la estructura del repo.

En el formato multi-directorio, el paso 2 copia un árbol con frecuencia
de 3-5 archivos cuando el contenido real vive solo en el `.md` principal.
Los archivos satélite (SKILL.md, hooks auxiliares, etc.) son opcionales
en la gran mayoría de los casos de uso del operador.

La conclusión es adoptar single-file para todos los módulos nuevos y
mantener soporte legado en el validador global para módulos existentes.

## Decisión

Todos los módulos nuevos del sistema de plantillas adoptan el formato
**single-file** (`plantilla_{singular}.md` + `ejemplo_{singular}.md`)
en lugar de directorios `plantilla_{singular}/`. El validador global
acepta ambas formas durante la transición.

## Alternativas consideradas

1. **Mantener multi-directorio para todos** — Descartado porque aumenta
   la carga cognitiva del operador (cp de árbol) y dificulta el
   bootstrapping de módulos simples.

2. **Single-file solo para módulos simples, multi-dir para complejos** —
   Descartado porque introduce una bifurcación de convención que el
   operador tendría que recordar. La consistencia tiene más valor que
   la flexibilidad caso-a-caso.

3. **Multi-directorio con README como punto de entrada obligatorio** —
   Evaluado; el README solo movería el problema: el validador seguiría
   necesitando localizar el `.md` funcional dentro del directorio.

## Consecuencias

- Los módulos nuevos (miniapps, cuadernos, knowledge) nacen como
  single-file y no heredan la deuda del formato anterior.
- El validador global mantiene la rama `plantilla_dir.is_dir() or
  plantilla_md.is_file()` para no romper módulos existentes
  (agentes, skills, commands, hooks, mcp, plugins, repositorios).
- El script `claude-init` deberá actualizarse para copiar el `.md`
  directamente en lugar de clonar un directorio.
- La documentación de `CONTRIBUTING.md` y `INDEX.md` deben reflejar
  la nueva convención al actualizarse.

## Referencias

- Plantilla canon · `cuadernos/plantilla_cuadernos.md`
- Validador global · `validar_repo.py` (líneas ~83-96, `NOMBRE_SINGULAR`)
- Módulo miniapps como precedente · `miniapps/plantilla_miniapps.md`
- Skill `EVO_autoresearch` para exploración de alternativas técnicas
