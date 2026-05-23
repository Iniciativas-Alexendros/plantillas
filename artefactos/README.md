# Plantilla canon · `artefactos/` · FLAT

> Estructura base de la carpeta `artefactos/` que cada cuaderno copia/extiende. Canon homogeneizado 2026-05-06: **sin subdirectorios**. Los archivos viven directamente en `artefactos/` y se versionan in-place o con sufijo `-YYYY-MM-DD` / `-vN`.

## Reglas

1. **PLANO**: archivos directamente en `artefactos/`, sin `control-mision/`, `dossiers/`, `diapos/`, etc.
2. **Versionado**:
   - Si el archivo es vivo (control-misión, dashboard): nombrar `<slug>-control-mision.html` y sobrescribir.
   - Si requiere histórico congelado por hito: renombrar la versión anterior a `<slug>-control-mision-YYYY-MM-DD.html` antes de sobrescribir.
   - Si es serie temporal (auditoría mensual, dossier periódico): siempre con sufijo de fecha o versión.
3. **Tipos** (orientativo, no obligatorio en el nombre):
   - `<tema>-control-mision.html` → HTML navegable cabecera del cuaderno.
   - `dossier-<tema>.md` o `dossier-<tema>-YYYY-MM-DD.md` → análisis / entregables markdown.
   - `diapos-<tema>-vN.html` → presentaciones interactivas / slides.
   - `auditoria-<tema>-YYYY-MM-DD.md` → reportes ad-hoc.

## Regla canon (CLAUDE.md §3)

`artefactos/` SÓLO existe en dos lugares:

1. `~/.claude/herramientas/plantillas/artefactos/` (esta plantilla, con solo `.gitkeep` + este README).
2. `~/.claude/cuadernos/<slug>/artefactos/` (instancias por cuaderno).

**Prohibido**:
- Crearlo en raíz `~/.claude/artefactos/` (eliminado 2026-04-27).
- Crear subdirectorios dentro salvo decisión explícita del operador con justificación en bitácora del cuaderno.
