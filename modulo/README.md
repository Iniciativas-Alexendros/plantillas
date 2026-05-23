# Módulo

> **Propósito**: Base para crear nuevos módulos en el sistema de plantillas.
> Copia este directorio y renombra según el patrón establecido.

---

## Paso a paso

1. **Renombra el directorio**: `modulo` → `<nombre-del-modulo>`.
2. **Renombra subdirectorios**:
   - `ejemplo_modulo/` → `ejemplo_<modulo>/`
3. **Edita `MODULO.md`**: playbook instructivo del nuevo componente.
4. **Edita `ejemplo_modulo/EJEMPLO.md`**: referencia funcional.
5. **Crea `validar_modulo.py`**: usa el motor reusable.
6. **Crea `.github/workflows/validar-modulo.yml`**: CI/CD.
7. **Actualiza `INDEX.md`** y `ROADMAP.md`.

---

## Estructura resultante

```
<modulo>/
├── plantilla_<modulo>/
│   └── [ARCHIVO_PRINCIPAL].md
├── ejemplo_<modulo>/
│   └── [archivos operativos]
├── validar_<modulo>.py
└── .github/
    └── workflows/
        └── validar-<modulo>.yml
```

## Reglas

- Nombre del módulo: `kebab-case`.
- Validador debe pasar `--strict` sobre el ejemplo.
- Todo archivo de plantilla debe tener placeholders claros.
- Referencia a docs oficiales en el playbook.

---

## Referencias

- **CONTRIBUTING.md**: guía completa de contribución.
- **Motor de validación**: `../validadores/`
