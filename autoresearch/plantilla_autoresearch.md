---
name: NOMBRE-INVESTIGACION-KEBAB
description: >
  Una a tres líneas que describan la PREGUNTA o TEMA que investiga este
  cuaderno, y CUÁNDO consultarlo. El operador lo genera/actualiza con
  la skill EVO_autoresearch y lo revisa como fuente de verdad secundaria.
topic: PALABRAS-CLAVE-O-DOMINIO
sources:
  - "https://example.com/fuente-1"
  - "https://example.com/fuente-2"
status: draft
last_updated: 2026-05-23
confidence: 0.5
---

## Pregunta

> Enunciar aquí la pregunta de investigación en una sola oración, clara y
> accionable. Ej.: "¿Cuándo conviene usar prompt caching vs memory en la
> Claude API?"

PREGUNTA-PRINCIPAL-DE-INVESTIGACION.

## Fuentes

Lista de fuentes consultadas con título + URL. Deben coincidir con `sources:`
del frontmatter cuando `status` es `review` o `published`.

- [TITULO-FUENTE-1](https://example.com/fuente-1) — DESCRIPCION-BREVE
- [TITULO-FUENTE-2](https://example.com/fuente-2) — DESCRIPCION-BREVE

## Hallazgos

Puntos clave extraídos de las fuentes. Cada bullet es un hallazgo atómico
y verificable; no opiniones.

- HALLAZGO-1
- HALLAZGO-2
- HALLAZGO-3

## Veredicto

Síntesis accionable de los hallazgos. Responde directamente a la pregunta.
Refleja la confianza en `confidence:` del frontmatter.

VEREDICTO-PRINCIPAL. Confianza: 0.5.

## Pendientes

Preguntas abiertas, fuentes no consultadas o experimentos que validarían
el veredicto.

- [ ] PENDIENTE-1
- [ ] PENDIENTE-2
