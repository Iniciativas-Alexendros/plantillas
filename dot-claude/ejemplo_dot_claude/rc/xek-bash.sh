# shellcheck shell=bash
# ~/.bashrc.d/xek.sh — XEK bash wrapper (sourced from ~/.bashrc)
# Parte del bootstrap XEK-ENV v3.1 para Claude Code on the web.
[ -z "${PS1:-}" ] && return

# ─── Historial ────────────────────────────────────────────────────────────
HISTSIZE=100000
HISTFILESIZE=200000
HISTCONTROL=ignoredups:erasedups:ignorespace
HISTIGNORE='ls:cd:cd -:pwd:exit:date:clear:* --help'
HISTTIMEFORMAT='%F %T '
shopt -s histappend cmdhist autocd cdspell dirspell globstar checkwinsize nocaseglob

# ─── Aliases (modernizados con CORE tools) ───────────────────────────────
alias ls='eza --group-directories-first --icons=auto'
alias ll='eza -l --git --header --time-style=long-iso'
alias la='eza -la --git'
alias lt='eza --tree --level=3 --git-ignore'
alias cat='bat --paging=never --style=plain'
alias less='bat --paging=always'
alias diff='delta'
alias grep='rg'
alias find='fd'
alias df='df -h'
alias du='du -h'
alias free='free -h'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# ─── Git ─────────────────────────────────────────────────────────────────
alias gs='git status -sb'
alias gd='git diff'
alias gdc='git diff --cached'
alias gl='git log --oneline --graph --decorate -20'
alias gla='git log --oneline --graph --decorate --all -30'
alias gp='git pull --ff-only'
alias gpu='git push -u origin HEAD'
alias gco='git checkout'
alias gcb='git checkout -b'
alias gcm='git commit -m'

# ─── XEK shortcuts ───────────────────────────────────────────────────────
alias xek-log='tail -f $XEK_LOG'
alias xek-tools='uv tool list'
alias xek-where='cd $XEK_PLANTILLAS'
alias xek-repos='cd $XEK_REPOS_HOME'
alias xek-versions='node --version; python3 --version; bun --version; go version; rustc --version'

# ─── Red (local + VPS) ───────────────────────────────────────────────────
alias myip='curl -fsSL https://ifconfig.me; echo'
alias myip4='curl -fsSL -4 https://ifconfig.me; echo'
alias myip6='curl -fsSL -6 https://ifconfig.me 2>/dev/null; echo'
localip() { ip -4 -o addr show scope global | awk '{print $2, $4}'; }
alias ports='sudo ss -tulnp'
alias listen='ss -tlnp'
alias trace='mtr -rwbzc 10'
alias scan='nmap -sV -T4'
alias serve='python3 -m http.server'
alias bench='iperf3 -c'
alias bench-srv='iperf3 -s'
alias ssh-keep='autossh -M 0 -o ServerAliveInterval=30 -o ServerAliveCountMax=3'
alias tunl='ssh -N -L'        # uso: tunl 8080:localhost:80 user@vps
alias rtunl='ssh -N -R'       # reverse tunnel

# ─── Docker ──────────────────────────────────────────────────────────────
alias d='docker'
alias dc='docker compose'
alias dps='docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}"'
alias dpsa='docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"'
alias dlogs='docker logs -f --tail=100'
alias dimg='docker images'
alias dexec='docker exec -it'
alias dprune='docker system prune -af --volumes'
alias dstop-all='docker stop $(docker ps -q) 2>/dev/null'
alias drm-all='docker rm $(docker ps -aq) 2>/dev/null'
alias ld='lazydocker'
alias dscan='trivy image'                 # uso: dscan nginx:latest
alias dlint='hadolint'                    # uso: dlint Dockerfile
alias dlayers='dive'                      # uso: dlayers nginx:latest

# ─── Python ──────────────────────────────────────────────────────────────
alias py='ipython --no-banner --colors=Linux'
alias jl='jupyter lab --no-browser --ip=0.0.0.0 --port=8888'
alias venv='uv venv && source .venv/bin/activate'
alias activate='source .venv/bin/activate'

# ─── Integraciones ───────────────────────────────────────────────────────
command -v mise     >/dev/null && eval "$(mise activate bash --shims)" 2>/dev/null
command -v starship >/dev/null && eval "$(starship init bash)"
command -v zoxide   >/dev/null && eval "$(zoxide init bash)" && alias cd=z
command -v atuin    >/dev/null && eval "$(atuin init bash --disable-up-arrow)"
command -v direnv   >/dev/null && eval "$(direnv hook bash)"

# ─── FZF (Ctrl-R historia, Ctrl-T archivos, Alt-C dir) ───────────────────
[ -f /usr/share/doc/fzf/examples/key-bindings.bash ] && \
  source /usr/share/doc/fzf/examples/key-bindings.bash
[ -f /usr/share/doc/fzf/examples/completion.bash ] && \
  source /usr/share/doc/fzf/examples/completion.bash
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_ALT_C_COMMAND='fd --type d --hidden --follow --exclude .git'
export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border --info=inline'

# ─── Banner mínimo al entrar ─────────────────────────────────────────────
[ -n "${XEK_VERSION:-}" ] && echo "▸ XEK v$XEK_VERSION · $(date +%H:%M) · $(basename "$PWD")"
