# ~/.zshrc — XEK zsh wrapper (zinit + plugins + starship + atuin)
# Parte del bootstrap XEK-ENV v3.1 para Claude Code on the web.
# =========================================================================

ZINIT_HOME="${XDG_DATA_HOME:-$HOME/.local/share}/zinit/zinit.git"
[ ! -d "$ZINIT_HOME" ] && \
  git clone --depth 1 https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
source "$ZINIT_HOME/zinit.zsh"

# ─── Plugins (lazy, en orden óptimo) ─────────────────────────────────────
zinit ice depth=1 lucid
zinit light zsh-users/zsh-completions
zinit ice depth=1 lucid wait'0' atinit'zicompinit; zicdreplay'
zinit light zdharma-continuum/fast-syntax-highlighting
zinit ice depth=1 lucid wait'0' atload'_zsh_autosuggest_start'
zinit light zsh-users/zsh-autosuggestions
zinit ice depth=1 lucid wait'0'
zinit light zsh-users/zsh-history-substring-search
zinit ice depth=1 lucid wait'1'
zinit light Aloxaf/fzf-tab
zinit snippet OMZP::git
zinit snippet OMZP::sudo
zinit snippet OMZP::command-not-found
zinit snippet OMZP::extract

# ─── Historia ────────────────────────────────────────────────────────────
HISTSIZE=100000
SAVEHIST=200000
HISTFILE=~/.zsh_history
setopt SHARE_HISTORY HIST_IGNORE_DUPS HIST_IGNORE_ALL_DUPS HIST_IGNORE_SPACE \
       HIST_REDUCE_BLANKS INC_APPEND_HISTORY EXTENDED_HISTORY HIST_VERIFY

# ─── Opciones ────────────────────────────────────────────────────────────
setopt AUTO_CD AUTO_PUSHD PUSHD_IGNORE_DUPS PUSHD_SILENT CDABLE_VARS
setopt EXTENDED_GLOB GLOB_DOTS NUMERIC_GLOB_SORT
setopt INTERACTIVE_COMMENTS PROMPT_SUBST
setopt NO_BEEP

# ─── Keybindings (emacs por defecto; cambia a 'bindkey -v' para vi) ──────
bindkey -e
bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down
bindkey '^[[Z' reverse-menu-complete

# ─── fzf-tab tweaks ──────────────────────────────────────────────────────
zstyle ':completion:*' menu no
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
zstyle ':fzf-tab:complete:cd:*' fzf-preview 'eza --tree --level=2 --color=always $realpath 2>/dev/null'
zstyle ':fzf-tab:complete:*:*' fzf-preview 'bat --color=always --style=plain --line-range :100 $realpath 2>/dev/null'
zstyle ':fzf-tab:*' switch-group ',' '.'

# ─── Aliases (idénticos a bash) ──────────────────────────────────────────
alias ls='eza --group-directories-first --icons=auto'
alias ll='eza -l --git --header --time-style=long-iso'
alias la='eza -la --git'
alias lt='eza --tree --level=3 --git-ignore'
alias cat='bat --paging=never --style=plain'
alias less='bat --paging=always'
alias diff='delta'
alias grep='rg'
alias find='fd'
alias gs='git status -sb'
alias gd='git diff'
alias gl='git log --oneline --graph --decorate -20'
alias gp='git pull --ff-only'
alias gpu='git push -u origin HEAD'
alias py='ipython --no-banner --colors=Linux'
alias jl='jupyter lab --no-browser --ip=0.0.0.0 --port=8888'
alias venv='uv venv && source .venv/bin/activate'
alias xek-log='tail -f $XEK_LOG'
alias xek-tools='uv tool list'
alias xek-where='cd $XEK_PLANTILLAS'
alias xek-repos='cd $XEK_REPOS_HOME'
alias xek-versions='node --version; python3 --version; bun --version; go version; rustc --version'

# Red (local + VPS)
alias myip='curl -fsSL https://ifconfig.me; echo'
alias myip4='curl -fsSL -4 https://ifconfig.me; echo'
alias localip="ip -4 -o addr show scope global | awk '{print \$2, \$4}'"
alias ports='sudo ss -tulnp'
alias listen='ss -tlnp'
alias trace='mtr -rwbzc 10'
alias scan='nmap -sV -T4'
alias serve='python3 -m http.server'
alias bench='iperf3 -c'
alias bench-srv='iperf3 -s'
alias ssh-keep='autossh -M 0 -o ServerAliveInterval=30 -o ServerAliveCountMax=3'
alias tunl='ssh -N -L'
alias rtunl='ssh -N -R'

# Docker
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
alias dscan='trivy image'
alias dlint='hadolint'
alias dlayers='dive'

# ─── Integraciones ───────────────────────────────────────────────────────
command -v mise     >/dev/null && eval "$(mise activate zsh --shims)" 2>/dev/null
command -v starship >/dev/null && eval "$(starship init zsh)"
command -v zoxide   >/dev/null && eval "$(zoxide init zsh)" && alias cd=z
command -v atuin    >/dev/null && eval "$(atuin init zsh --disable-up-arrow)"
command -v direnv   >/dev/null && eval "$(direnv hook zsh)"

# ─── FZF (Ctrl-R, Ctrl-T, Alt-C) ─────────────────────────────────────────
[ -f /usr/share/doc/fzf/examples/key-bindings.zsh ] && source /usr/share/doc/fzf/examples/key-bindings.zsh
[ -f /usr/share/doc/fzf/examples/completion.zsh ]   && source /usr/share/doc/fzf/examples/completion.zsh
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border --info=inline'

[ -n "${XEK_VERSION:-}" ] && print -P "%F{green}▸%f XEK v$XEK_VERSION · %F{cyan}$(basename $PWD)%f"
