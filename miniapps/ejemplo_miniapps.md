---
name: kpi-mensual
description: >
  Mini-app dashboard que muestra KPIs financieros mensuales (MRR, ARR,
  burn, runway) cargados desde un JSON inline. Se abre directamente en
  navegador sin servidor; útil para revisión rápida durante el cierre
  mensual de cuentas.
category: dashboard
runtime: browser
version: 0.1.0
last_updated: 2026-05-23
---

## Propósito

`kpi-mensual` es una mini-app single-file que renderiza 4 KPI cards
(MRR, ARR, burn, runway) + tabla mensual sortable + gráfica de líneas
ligera (Canvas API, sin librerías). Está pensada para que el operador
abra el HTML, revise el mes y cierre — no para uso prolongado.

## Cuándo usar

- Cierre mensual: revisar evolución vs mes anterior antes de tocar
  `EVENTOS.md` o registrar movimientos en `COM_finanzas`.
- Pre-junta con stakeholders: snapshot rápido para compartir.
- Tras importar `stripe-mensual.json` para validar antes de archivar.

## Cómo se usa

1. Generar `data/kpis-{YYYY-MM}.json` con los movimientos del mes.
2. Reemplazar el bloque `<script id="data" type="application/json">` del
   archivo HTML por el contenido del JSON.
3. Abrir el HTML en navegador (`xdg-open kpi-mensual.html`).
4. Usar el slider del header para alternar tema sepia ↔ nocturno.

## Datos esperados (esquema JSON)

```json
{
  "periodo": "2026-05",
  "kpis": {
    "mrr_eur": 3450,
    "arr_eur": 41400,
    "burn_eur": 2100,
    "runway_meses": 18
  },
  "delta_vs_anterior": {
    "mrr_eur": 320,
    "burn_eur": -150
  },
  "movimientos": [
    {"fecha": "2026-05-03", "concepto": "Stripe payout", "neto_eur": 845},
    {"fecha": "2026-05-15", "concepto": "Hostinger VPS", "neto_eur": -28}
  ]
}
```

## Estructura del HTML (resumen)

- `<header>` con título, categoría visible (`dashboard`) y `<input type=range>` para tema.
- `<nav>` con 3 tabs: `Resumen` · `Movimientos` · `Tendencia`.
- `<main>` con 1 `<section role=tabpanel>` por tab.
- `<footer>` con versión + fecha + enlace a `plantilla_miniapps`.

## Anti-patrones evitados

- No carga librerías externas; el chart se dibuja en `<canvas>` con la
  Canvas API nativa.
- No usa `localStorage` para datos sensibles; el JSON se reemplaza in-place.
- No tiene endpoints; es completamente offline-safe.

## Referencias

- Plantilla canon · `miniapps/plantilla_miniapps.md`
- Patrón VAP · `~/.claude/CLAUDE.md` §6 bis
- Skill `COM_finanzas` para registrar deltas tras revisar la mini-app
