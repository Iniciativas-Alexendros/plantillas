# `rc/` — Wrappers de shell y profile de IPython

Archivos de configuración que el bootstrap **XEK-ENV v3.1**
(`cloud-env/bootstrap.sh`) pre-stagea en el `$HOME` de la sesión cuando el
tier `XEK_TIER_SHELL` o `XEK_TIER_PY` están activos.

| Origen (en este repo) | Destino en la sesión | Tier |
|---|---|---|
| `rc/xek-bash.sh` | `~/.bashrc.d/xek.sh` (sourced desde `~/.bashrc`) | SHELL |
| `rc/xek-zsh.zsh` | `~/.zshrc` | SHELL |
| `rc/starship.toml` | `~/.config/starship.toml` | SHELL |
| `rc/ipython_config.py` | `~/.ipython/profile_default/ipython_config.py` | PY |

## Política

- El bootstrap usa `cp -n` (no-clobber): **nunca** sobreescribe configuración
  existente en la sesión. Para regenerar, borra el destino y reabre sesión.
- Los wrappers comprueban que cada binario externo (`starship`, `atuin`,
  `zoxide`, `direnv`, `fzf`) exista antes de cargarlo; son seguros aunque
  el tier CORE no se haya completado.
- Aliases idénticos entre bash y zsh para mantener músculo de memoria.

## Cómo probar localmente

```bash
# Bash
cp dot-claude/ejemplo_dot_claude/rc/xek-bash.sh ~/.bashrc.d/xek.sh
echo '[ -f "$HOME/.bashrc.d/xek.sh" ] && source "$HOME/.bashrc.d/xek.sh"' >> ~/.bashrc
exec bash -l

# Zsh
cp dot-claude/ejemplo_dot_claude/rc/xek-zsh.zsh ~/.zshrc
cp dot-claude/ejemplo_dot_claude/rc/starship.toml ~/.config/starship.toml
zsh -l

# IPython
mkdir -p ~/.ipython/profile_default
cp dot-claude/ejemplo_dot_claude/rc/ipython_config.py ~/.ipython/profile_default/
ipython
```
