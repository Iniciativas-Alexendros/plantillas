# Estándares

> **Propósito**: módulo canónico de estándares del portfolio. Reúne en `ESTANDARES.md`
> la metodología común (CLAUDE.md, frontmatter, versionado, pre-commit, .env.example,
> matriz CI) que el resto de repos de `~/repositorios/` adoptan para cohesionar formato,
> calidad y operación. A diferencia de los demás módulos no se copia: se consulta y se
> aplica sobre cada repo.

---

## Paso a paso

1. **Abre `ESTANDARES.md`** y recorre sus 6 secciones más la matriz CI mínima.
2. **Por cada estándar**, comprueba el repo objetivo contra su criterio.
3. **Aplica o justifica**: lo que no aplique al tipo de repo se omite explícitamente
   (anótalo), no se ignora en silencio.
4. **Registra el resultado** como checklist de homologación (ver
   `ejemplo_estandares/EJEMPLO.md`).
5. **Cierra abriendo el trabajo pendiente** en el bloque pendiente del `CLAUDE.md`
   del repo homologado.

---

## Estructura resultante

```
estandares/
├── ESTANDARES.md              ← Catálogo canónico (los 6 estándares + matriz CI)
├── ejemplo_estandares/
│   └── EJEMPLO.md             ← Homologación resuelta de un repo de muestra
└── validar_estandares.py      ← Validador con --strict
```

---

## Reglas

- El módulo es autovalidado: su propio directorio es el ejemplo que el validador comprueba.
- `validar_estandares.py` debe pasar `--strict` sobre `estandares/`.
- `ESTANDARES.md` es la fuente única; no se duplica su contenido en otros repos, se referencia.
- Toda homologación deja rastro auditable (checklist marcada, no marcadores en código).

---

## Referencias

- **CONTRIBUTING.md** de este repo: guía de contribución.
- **Motor de validación**: `../validadores/`
- Conventional Commits: <https://www.conventionalcommits.org>
- Keep a Changelog: <https://keepachangelog.com>
