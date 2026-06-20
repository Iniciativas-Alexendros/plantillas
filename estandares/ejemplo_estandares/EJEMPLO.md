# Homologación de `mi-repo-demo`

> Ejemplo funcional del módulo `estandares`. Muestra la checklist de homologación
> ya resuelta para un repo Next.js ficticio (`mi-repo-demo`) tras aplicar los 6
> estándares de `ESTANDARES.md` más la matriz CI. Sin placeholders: cada casilla
> lleva la nota de cómo quedó satisfecha.

---

## Datos del repo

- **Repo**: `mi-repo-demo`
- **Tipo**: web Next.js 15 (React 19, Tailwind), gestor `pnpm`.
- **Fecha de homologación**: 2026-06-20.

---

## Checklist de homologación

- [x] **1. CLAUDE.md con XML suave** — Creado en raíz con tags `proyecto`, `stack`,
  `estado`, `arquitectura`, `pendiente`, `notas`. Lo crítico (stack y estado) arriba;
  los comandos del bloque `stack` (`pnpm dev|build|test|lint`) existen en `package.json`.
  El estado marca «build✓ verificado / cobertura inferida».
- [x] **2. Frontmatter YAML para contenido catalogado** — Las entradas de `content/blog/`
  abren con `name` (kebab-case), `description` (una línea) y `version` (SemVer); validado
  con `pnpm run check:frontmatter`.
- [x] **3. Versionado y CHANGELOG** — `package.json` en `0.4.0` (SemVer); `CHANGELOG.md`
  estilo Keep a Changelog con sección `[Unreleased]`. El tag `v0.4.0` casa con el manifiesto.
- [x] **4. Calidad local: pre-commit homogéneo** — husky + lint-staged + commitlint
  (Conventional Commits) sobre ficheros staged; el hook corre `eslint --fix` y `prettier`
  solo en lo modificado, no en todo el repo.
- [x] **5. Bloque pendiente como TODO canónico** — Migrados 3 `// TODO` del código al
  bloque `pendiente` del `CLAUDE.md`, cada uno ligado a su fase (F2) y versión objetivo (0.5.0).
- [x] **6. .env.example + validación de entorno** — Publicado `.env.example` con placeholders
  (`DATABASE_URL=postgres://user:pass@host:5432/db`, sin secretos reales) y `check:env` que
  falla si falta `DATABASE_URL` o `STRIPE_SECRET_KEY`. Nombre canónico `.env.example`.
- [x] **Matriz CI mínima** — Workflow `ci.yml` con el gate de PR en orden: `pnpm typecheck`
  (`tsc --noEmit`) → `pnpm lint` (eslint) → `pnpm format:check` (prettier) → `pnpm test`
  (vitest) → `pnpm build` (next build). Todos en verde en el primer run.

---

## Omitidos (justificados)

- Ninguno: al ser un repo JS/TS con entorno y contenido catalogado, los 6 estándares y la
  matriz aplican. (En un repo Rust se omitiría el estándar 2 si no hubiera contenido catalogado,
  anotándolo aquí.)

---

## Referencias

- Catálogo: `../ESTANDARES.md`
- Keep a Changelog: <https://keepachangelog.com>
