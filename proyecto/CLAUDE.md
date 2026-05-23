# [Nombre del Proyecto]

> Configuración local de Claude Code para este proyecto.

## Contexto

- **Stack**: [TS/React/Next.js | Python/Django | Rust | etc.]
- **Entorno**: [Local / Docker / Vercel / VPS]
- **Base de datos**: [PostgreSQL / Supabase / SQLite]
- **Tests**: [Vitest / pytest / cargo test]

## Reglas de trabajo

1. **Antes de editar**: lee `CONTRIBUTING.md` si existe.
2. **Commits**: Conventional Commits (`feat:`, `fix:`, `docs:`).
3. **Tests**: todo código nuevo lleva tests.
4. **Seguridad**: secrets solo en `.env`; nunca en código.
5. **Deploy**: nunca sin confirmación explícita del usuario.

## Estructura del proyecto

```
├── src/          ← Código fuente
├── tests/        ← Tests
├── docs/         ← Documentación
└── .github/      ← CI/CD
```

## Comandos útiles

```bash
# Tests
npm test

# Lint
npm run lint

# Build
npm run build
```

## Integraciones

| Servicio | Uso |
|---|---|
| [GitHub/Vercel/etc.] | [Propósito] |
