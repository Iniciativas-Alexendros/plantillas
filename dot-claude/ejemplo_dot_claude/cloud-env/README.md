# `cloud-env/` — Configuración del entorno Claude Code on the web

Copia canónica y versionada de lo que se pega en el diálogo **"Actualizar
entorno en la nube"** (https://claude.ai/code → entornos).

| Archivo | Destino en el diálogo |
|---|---|
| `env-vars.env` | Campo **"Variables de entorno"** (formato `.env`) |
| `bootstrap.sh` | Campo **"Script de configuración"** |

## Cómo aplicarlo (manual)

1. Abre https://claude.ai/code y entra a tu entorno (p.ej. `Minado`).
2. **Acceso a la red**: Completo.
3. **Variables de entorno**: pega el contenido de `env-vars.env`.
4. **Script de configuración**: pega el contenido de `bootstrap.sh`.
5. *Guardar cambios*. Los cambios se aplican a sesiones **nuevas**.
6. Arranca una sesión nueva; el bootstrap escribe en `$XEK_LOG`.

## Política de secretos

El diálogo prohíbe explícitamente meter secretos. Tres canales válidos:

1. **MCPs autenticados** (preferido): GitHub, Hugging Face, Notion, Stripe,
   Figma, Vercel. Ya gestionados por Claude Code, sin acción local.
2. **age-cifrados** en `$XEK_SECRETS_DIR` (perms 700, gitignored).
3. **sops + age** para `secrets.yaml` versionables; clave en
   `$SOPS_AGE_KEY_FILE`.

## Tiers

| Tier | Defecto | Qué instala | Para qué |
|---|---|---|---|
| CORE | on | fd, bat, eza, delta, zoxide, sops, zstd, rsync, sqlite3, httpie | base imprescindible |
| PY | on | ipython + polars/pandas/numpy/httpx/pydantic/rich/typer/... | Python interactivo "potente" |
| SHELL | on | zsh + starship + atuin + zinit + plugins + rcfiles | shell de calidad bash/zsh |
| AI | on | huggingface_hub + llm + duckdb | flujos IA local |
| OFFICE | on | ffmpeg + imagemagick + webp | media |
| LEGAL | off | pandoc + poppler + qpdf + tesseract-ocr-spa | jurídico / documentos |
| WEB | on | corepack/pnpm (Node 22 ya viene) | frontend |

Encender/apagar un tier: cambia `XEK_TIER_<NOMBRE>=1|0` en el campo
**Variables de entorno** y reabre sesión.

## Verificación en sesión nueva

```bash
echo "$XEK_VERSION $LANG $TZ"
command -v fd bat delta eza sops starship atuin zsh ipython httpie sqlite3
uv tool list
ipython -c "import polars,pandas,numpy,httpx,pydantic,rich; print('ok')"
tail -15 "$XEK_LOG"
```

## Re-aplicación / regeneración

- Para forzar reinstalación de hoy: `rm "$XEK_STATE/bootstrap-$(date +%Y-%m-%d).stamp"`
  y reabre sesión.
- Para regenerar rcfiles: borra `~/.bashrc.d/xek.sh`, `~/.zshrc`,
  `~/.config/starship.toml` o `~/.ipython/profile_default/ipython_config.py`
  y reabre sesión (el `cp -n` los volverá a crear desde `rc/`).

## Versión

XEK-ENV **v3.1** — sucesor de OMNI-ENV v3.0-FINAL.
