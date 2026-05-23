---
name: NOMBRE-MINIAPP-KEBAB
description: >
  Una a tres oraciones que describan QUÉ resuelve esta mini-app y
  CUÁNDO se usa. El operador la abre en navegador (single-file HTML)
  o la sirve estática, sin build-step.
category: dashboard
runtime: browser
version: 0.1.0
last_updated: 2026-05-23
---

## Propósito

> Qué problema concreto resuelve esta mini-app. Una mini-app es una SPA
> autocontenida (HTML single-file) tipo artifact de Claude.ai: vive en
> `~/.claude/miniapps/<slug>/index.html` o en `artefactos/playgrounds/`
> y se abre directamente en navegador.

PROBLEMA-CONCRETO que resuelve esta mini-app.

## Cuándo usar

- DISPARADOR-1: situación concreta en la que abrir la mini-app es la
  acción correcta.
- DISPARADOR-2: otra situación distinta.
- DISPARADOR-3 (opcional).

## Categorías válidas

`category:` debe ser una de:

- `dashboard` — vista de KPIs / métricas con datos cargados de archivo.
- `explorer` — navegación por estructura (árbol, tabla, diff).
- `tool` — herramienta interactiva (generador, calculadora, formulario).
- `playbook` — documento interactivo con tabs y prompt-dock.

## Runtime válido

`runtime:` debe ser uno de:

- `browser` — HTML single-file, sin servidor.
- `electron` — empaquetado como app de escritorio.
- `static` — multi-archivo servido por nginx / CDN.

## Estructura mínima esperada

Una mini-app `browser` cumple:

1. Single-file HTML (todo CSS y JS inline o data-uri).
2. Header con título + categoría + slider sepia ↔ nocturno (Patrón VAP).
3. Cuerpo con al menos 3 tabs SPA o 3 zonas funcionales.
4. Footer con `version` + `last_updated` + enlace a este `plantilla`.
5. Datos embebidos como JSON inline si la mini-app necesita estado.

## Anti-patrones

- Cargar JS externo desde CDN sin SRI hash.
- Requerir Node/npm/build-step.
- Modificar estado global del navegador sin localStorage prefijado.
- Embeber secretos o tokens en el HTML.

## Plantilla HTML reducida

```html
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>NOMBRE-MINIAPP-KEBAB</title>
  <style>
    /* tokens Vergina dual + slider sepia<->nocturno */
  </style>
</head>
<body>
  <header data-theme="sepia">
    <h1>NOMBRE-MINIAPP-KEBAB</h1>
    <input type="range" id="theme-slider" min="0" max="100" value="0">
  </header>
  <nav role="tablist">
    <button role="tab" aria-selected="true">Tab 1</button>
    <button role="tab">Tab 2</button>
    <button role="tab">Tab 3</button>
  </nav>
  <main>
    <section role="tabpanel">CONTENIDO-1</section>
  </main>
  <footer>v0.1.0 · 2026-05-23 · plantilla_miniapps</footer>
  <script>
    /* lógica mínima sin dependencias */
  </script>
</body>
</html>
```

## Referencias

- Patrón VAP (Vergina dual + slider) · `~/.claude/CLAUDE.md` §6 bis
- Skill `CREA_playground` · `~/.claude/skills/CREA_playground/SKILL.md`
- Especificación artefactos · `~/.claude/artefactos/README.md`
