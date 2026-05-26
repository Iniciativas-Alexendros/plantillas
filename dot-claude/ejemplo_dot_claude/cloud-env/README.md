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

## Versiones runtime (XEK-ENV v3.2)

Gestionadas por **mise** (sucesor de asdf), instalado en `~/.local/bin/mise`,
con shims en `~/.local/share/mise/shims` (prepended al `PATH`).

| Runtime | Versión | Origen | Cambiar |
|---|---|---|---|
| Node | **24** | `mise use node@24` | `NODE_VERSION=` en env vars |
| Python | 3.13 | `mise use python@3.13` | `PYTHON_VERSION=` en env vars |
| Bun | latest | `bun upgrade --stable` en CORE | `BUN_AUTO_UPGRADE=0` para desactivar |
| Go | sistema | `/usr/local/go` (preinstalado) | per-repo vía `mise.toml` |
| Rust | sistema | `~/.cargo` (preinstalado) | `rustup update` manual |

Per-repo: añade `mise.toml` o `.tool-versions` para fijar otras versiones.

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
| CORE | on | fd, bat, eza, delta, zoxide, sops, zstd, rsync, sqlite3, httpie, direnv, jq, yq, bc + `bun upgrade` | base imprescindible |
| RUNTIMES | on | mise + Node 24 + Python 3.13 | runtimes modernos versionables |
| PY | on | ipython + polars/pandas/numpy/httpx/pydantic/rich/typer/... | Python interactivo "potente" |
| SHELL | on | zsh + starship + atuin + zinit + plugins + rcfiles | shell de calidad bash/zsh |
| AI | on | huggingface_hub + llm + duckdb | flujos IA local |
| OFFICE | on | ffmpeg + imagemagick + webp | media |
| **NET** | **on** | **mtr + iperf3 + nmap + tcpdump + ngrep + mosh + autossh + sshpass + nethogs + iftop + bmon + tmux + screen + rclone + restic + wireguard-tools + gping + bandwhich + croc** | **red local + VPS** |
| **DOCKER** | **on** | **docker-compose-plugin + docker-buildx-plugin + buildah + skopeo + lazydocker + dive + ctop + hadolint + trivy** | **dockerización** |
| LEGAL | off | pandoc + poppler + qpdf + tesseract-ocr-spa | jurídico / documentos |
| WEB | on | corepack + pnpm@latest + yarn@stable (sobre Node 24) | frontend |

Encender/apagar: cambia `XEK_TIER_<NOMBRE>=1|0` en el campo **Variables de
entorno** y reabre sesión.

## Aliases incluidos en los rcfiles (`rc/xek-bash.sh` y `rc/xek-zsh.zsh`)

### Red
| Alias | Comando | Para qué |
|---|---|---|
| `myip` / `myip4` / `myip6` | `curl ifconfig.me` | IP pública v4/v6 |
| `localip` | `ip -4 -o addr show scope global` | IPs locales |
| `ports` | `sudo ss -tulnp` | puertos en escucha (TCP+UDP) |
| `listen` | `ss -tlnp` | puertos TCP en escucha |
| `trace <host>` | `mtr -rwbzc 10 <host>` | trace + ping continuo |
| `scan <host>` | `nmap -sV -T4 <host>` | scan rápido con detección de servicios |
| `serve [port]` | `python3 -m http.server` | servidor HTTP estático |
| `bench <host>` / `bench-srv` | `iperf3` | benchmark de ancho de banda |
| `ssh-keep user@vps` | `autossh -M 0 -o ServerAliveInterval=30 …` | SSH persistente |
| `tunl 8080:localhost:80 user@vps` | `ssh -N -L` | túnel local |
| `rtunl 8080:localhost:80 user@vps` | `ssh -N -R` | túnel inverso |

### Docker
| Alias | Comando | Para qué |
|---|---|---|
| `d` / `dc` | `docker` / `docker compose` | base |
| `dps` / `dpsa` | `docker ps` con formato tabla | inventario |
| `dlogs <name>` | `docker logs -f --tail=100` | seguir logs |
| `dexec <name> sh` | `docker exec -it` | entrar al contenedor |
| `dprune` | `docker system prune -af --volumes` | limpiar todo |
| `dstop-all` / `drm-all` | parar/borrar todos | reset |
| `ld` | `lazydocker` | TUI completo |
| `dscan <image>` | `trivy image` | escaneo de vulnerabilidades |
| `dlint <Dockerfile>` | `hadolint` | linter de Dockerfiles |
| `dlayers <image>` | `dive` | inspector de capas |

### Generales
| Alias | Para qué |
|---|---|
| `ll` / `la` / `lt` | listado eza |
| `xek-versions` | imprime versiones de node/python/bun/go/rust |
| `xek-log` | tail -f del log del bootstrap |
| `xek-tools` | `uv tool list` |

## Verificación en sesión nueva

```bash
echo "$XEK_VERSION $LANG $TZ"                  # 3.2 es_ES.UTF-8 Europe/Madrid
node --version                                   # v24.x.x
python3 --version
mise ls                                          # tabla con node@24, python@3.13
command -v mtr iperf3 nmap tcpdump mosh tmux rclone wg
command -v docker-compose docker-buildx lazydocker dive ctop hadolint trivy buildah skopeo
uv tool list
tail -15 "$XEK_LOG"
```

## Re-aplicación / regeneración

- Para forzar reinstalación de hoy:
  `rm "$XEK_STATE/bootstrap-$(date +%Y-%m-%d).stamp"` y reabre sesión.
- Cambiar versión de Node: edita `NODE_VERSION=24` en el campo
  "Variables de entorno", borra el stamp del día y reabre sesión.
- Para regenerar rcfiles: borra `~/.bashrc.d/xek.sh`, `~/.zshrc`,
  `~/.config/starship.toml` o `~/.ipython/profile_default/ipython_config.py`
  y reabre sesión (el `cp -n` los volverá a crear desde `rc/`).

## Tiempo de bootstrap

| Tipo | Duración esperada |
|---|---|
| Frío (todos los tiers on, primera sesión del día) | 60–120 s |
| Caliente (stamp del día activo) | <5 s |

El download principal en frío es de `mise` + Node 24 (~50 MB) + tier DOCKER
(binarios de GitHub releases).

## Tools opcionales NO instaladas por defecto

Para flujos avanzados de red/VPS, añadir manualmente en el bootstrap si
las necesitas:

- **tailscale** — mesh VPN (`curl -fsSL https://tailscale.com/install.sh | sh`)
- **cloudflared** — Cloudflare Tunnel client
- **caddy** — reverse proxy con HTTPS automático
- **k9s** / **kubectl** / **helm** — Kubernetes
- **terraform** / **ansible** — IaC

## Versión

XEK-ENV **v3.2** — añade Node 24 (via mise), tiers NET y DOCKER.
Histórico: v3.0 (OMNI-ENV) → v3.1 (tiers + rcfiles) → v3.2 (runtimes + red + docker).
