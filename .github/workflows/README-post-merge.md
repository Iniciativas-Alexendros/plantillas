# Plantilla Post-Merge · Pipelines 2026-05

Capa transversal de workflows que se ejecutan **después de un merge a `main`** en cualquier repo del operador. Reutilizable cross-repo vía `uses: Alexendros/plantillas/.github/workflows/_lib-post-merge.yml@v1`.

## Objetivos

- **Flexible/generalista** — sirve TS/Next.js, Rust, Python, Markdown-only, Docker, monorepo.
- **Informativa y rigurosa** — linters punta + supply-chain attestations.
- **"Máxima info en fallo, no bloqueo fatal"** — `continue-on-error: true` en linters, errores agregados con contexto.

## Adopción mínima (3 pasos)

1. **Activar permisos del repo**: Settings → Actions → Workflow permissions = "Read and write", marca "Allow GitHub Actions to create and approve PRs". Asegúrate de que Issues están habilitados.
2. **Copiar el caller**: copia `repositorios/ejemplo_repositorio/.github/workflows/post-merge.yml` a `.github/workflows/post-merge.yml` de tu repo.
3. **Merge a main**. Observa la pestaña Actions → "post-merge".

Eso es todo. El orquestador detecta el stack y activa solo los gates relevantes.

## Inputs del orquestador

| Input | Default | Descripción |
|---|---|---|
| `enable_linters` | `true` | actionlint+zizmor, ruff, eslint/biome, cargo-deny+clippy, hadolint, shellcheck, markdownlint, lychee, gitleaks, osv-scanner. |
| `enable_sbom` | `true` | syft → CycloneDX SBOM, sube como artifact. |
| `enable_attest` | `true` | `actions/attest-build-provenance@v2`. Cero secrets · OIDC nativo. |
| `enable_release` | `false` | release-please (opt-in). Solo repos publicables. |
| `release_type` | `""` (auto) | Override: `node`, `rust`, `python`, `simple`, `manifest`. |
| `streak_threshold_open` | `2` | Runs consecutivos fallidos necesarios para abrir issue auto. |
| `streak_threshold_close` | `3` | Runs verde-consecutivos para cerrar issue auto. |

## Stacks soportados

`detect-stack` clasifica por presencia de archivos (sin clonar deps):

| Stack | Detección | Linters extra activados |
|---|---|---|
| TypeScript/JS | `package.json` + `tsconfig*.json` o keywords | Biome (preferido si `biome.json`) o ESLint |
| Rust | `Cargo.toml` (raíz o workspace) | cargo-deny, clippy |
| Python | `pyproject.toml`, `setup.cfg`, `requirements*.txt` | Ruff |
| Docker | `Dockerfile*`, `compose*.y?ml` | hadolint |
| Markdown | cualquier `*.md` | markdownlint-cli2, lychee |
| Shell | `*.sh`, `*.bash` | shellcheck |
| Monorepo | `pnpm-workspace.yaml`, workspaces, `release-please-config.json` | release-please `manifest` mode |

Comunes (siempre activos): actionlint, zizmor (security audit de workflows), yamllint, gitleaks, osv-scanner.

## release-please flexible

- Sin config: el wrapper usa `release_type` autodetectado por detect-stack.
- Con `release-please-config.json` + `.release-please-manifest.json`: respeta tu config (modo `manifest`).
- Override manual: pasa `release_type: <node|rust|python|simple|manifest>` al caller.
- **Opt-in obligatorio**: `enable_release: true` en el caller. Default `false` para proteger repos no-publicables (xek-cluster, controlink-operator).

## Notificación de fallos (4 capas)

1. **reviewdog inline** (`reporter: github-check`, `level: warning`, `fail_on_error: false`) — anotaciones en el código modificado. Funciona aunque el trigger sea `push`.
2. **`$GITHUB_STEP_SUMMARY`** rico en cada `_lib-*` reusable.
3. **Sticky commit-comment** en el commit de merge (marker `<!-- bot:post-merge-sticky -->`, idempotente). SIEMPRE se publica.
4. **Issue auto sticky** SOLO si `prev_fail >= streak_threshold_open` (default 2 runs consecutivos fallidos). Anti-flake. Auto-cierre tras `streak_threshold_close` verdes consecutivos.

## Tecnología punta 2026

- **`actions/attest-build-provenance@v2`** — SLSA v1 build provenance L3, OIDC nativo GitHub, cero secrets.
- **`anchore/sbom-action`** — syft → CycloneDX, formato estándar (también soporta SPDX).
- **`google/osv-scanner-action`** — vulnerabilidades cross-language (TS/Python/Rust/Go/Maven lockfiles).
- **`zizmor`** — auditor de seguridad para GitHub Actions workflows (detecta script-injection, expresiones inseguras, etc.).
- **`reviewdog`** — anotaciones inline cross-linter unificadas.
- **`googleapis/release-please-action@v4`** — release automation generalista.

## Cómo desactivar un linter en tu repo

No expuesto explícitamente en inputs (sería puerta a discrepancia). Patrones aceptados:

- **Ignorar warnings de markdownlint**: añade `.markdownlint.yaml` con tu config.
- **Ignorar lychee**: añade `.lycheeignore`.
- **Ignorar gitleaks**: añade `.gitleaksignore`.
- **Ignorar osv-scanner**: añade `osv-scanner.toml`.
- **Ruff**: configura en `pyproject.toml` `[tool.ruff]`.
- **ESLint/Biome**: tu propia config gana.

Si necesitas SKIP completo de un linter, abre issue en `Alexendros/plantillas` proponiendo nuevo input.

## Troubleshooting

| Síntoma | Causa probable | Fix |
|---|---|---|
| "Resource not accessible by integration" en sticky-comment | Workflow permissions restrictivos en el repo consumidor | Settings → Actions → Workflow permissions = Read and write |
| Issue auto no se abre tras fallo | Solo 1 fallo (anti-flake). Necesita `>= streak_threshold_open` consecutivos | Espera al siguiente run, o baja threshold a 1 si lo necesitas |
| release-please no abre PR | Commits no siguen Conventional Commits | Usa `feat:`, `fix:`, `chore:` etc. |
| attest falla con "missing id-token" | Permisos del caller no incluyen `id-token: write` | Añade a permissions del caller |

## Versionado

- `@main` — tracking continuo, recibe cambios al instante (recomendado solo en plantillas mismo · dogfood).
- `@v1` — tag movible mayor; cambios compatibles. Recomendado para repos consumidores.
- `@<sha>` — pin determinístico; bump manual.

## Fuera de scope

- Deploys bespoke (Vercel/Fly/k8s/Dokploy) — siguen en workflows propios del repo.
- Firma cosign keyless de imágenes Docker (planificado `_lib-image-sign.yml`).
- Migración Dependabot → Renovate (decisión separada).
- Métricas DORA / dashboards externos.
