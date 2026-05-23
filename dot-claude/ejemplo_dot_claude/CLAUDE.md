# 'OPUS NOSTRUM, ARMA PURA.'

## Introducción · Norma global Claude & Alexendros

Norma global para la administración de Claude en todos los hilos del usuario Alexendros.

<scope path-canonico="~/.claude/CLAUDE.md" os="EndeavourOS (Arch rolling)" de="GNOME Shell sobre Wayland" gestores="pacman+yay+flatpak" home="/home/alexendros" alcance="todos los hilos del usuario · gestiona todo el entorno salvo restricción explícita por sesión"/>

Stack online: Git (GitHub · Forgejo) · Despliegues (Vercel · Dokploy · Hostinger) · Finanzas (Stripe · Revolut) · Suite (Proton.me) · Comunicación (Notion) · Backups (Cloudflare R2) · Observabilidad (Sentry · GlitchTip).

## 1. Maestría · cómo decidir

Antes de responder: activa `/enrutador` para iniciar workflow seleccionador.

<maestrias>
  <maestria nombre="Claude" color-ansi="208" dominio="meta ~/.claude/ · skills · hooks · agentes · memoria · cuadernos"/>
  <maestria nombre="Ingeniero" color-ansi="141" dominio="código (TS/TSX/SH/CSS/HTML) · integraciones · infra · despliegue · tests · UI"/>
  <maestria nombre="Ejecutivo" color-ansi="78" dominio="finanzas · cartera · runway · decisiones de negocio"/>
</maestrias>

<pre-check secuencia="estricta">
  <paso n="1">elegir maestría aplicable</paso>
  <paso n="2">invocar skill aplicable vía tool `Skill` antes de la primera edición</paso>
  <paso n="3">elegir agente especializado si aplica</paso>
</pre-check>

## 2. Doctrinas Globales

- **sudouth**: Toda escalada usa `sudouth`. `sudo` directo está PROHIBIDO.
- **Secrets**: Solo en archivos `.env`. NUNCA en código.
- **git push**: NUNCA sin confirmación explícita del usuario.
- **Calidad**: Todo código nuevo lleva tests. Revisión antes de merge.
- **Delegación**: Usar subagentes cuando sea posible. Contexto mínimo suficiente.
- **Tracking**: `TodoWrite` para progreso visible.

## 3. Integraciones

| Servicio | Uso | Config |
|---|---|---|
| GitHub | Repos, PRs, issues | `GITHUB_TOKEN` en env |
| Vercel | Deploy frontend | CLI autenticado |
| Dokploy | Deploy backend VPS | SSH + Docker |
| Stripe | Pagos | API keys en `.env` |
| Proton | Mail, Pass, Drive | Sesión web activa |
| Notion | Wiki, docs | Integration token |

### MCP Servers activos

Ver `mcp.json` para la configuración completa.

## 4. Árbol de directorios `.claude/`

```
~/.claude/
├── agents/          ← Agentes especializados (subagentes Claude Code)
├── skills/          ← Skills reutilizables (comandos slash)
├── commands/        ← Comandos slash personalizados adicionales
├── hooks/           ← Hooks de interceptación (PreToolUse, PostToolUse, etc.)
├── scripts/         ← Scripts de utilidad personal
├── plugins/         ← Plugins de extensión
├── mcp/             ← Configuración de servidores MCP
├── miniapps/        ← Mini-aplicaciones HTML/SPA autocontenidas
├── autoresearch/    ← Investigaciones automáticas persistentes
├── cuadernos/       ← Cuadernos de trabajo interactivos
├── knowledge/       ← Base de conocimiento (documentos de referencia)
├── artefactos/      ← Outputs entregados al operador (playgrounds, memos)
└── projects/        ← Memoria por proyecto (contexto persistente)
```

## 5. Rutas Importantes

| Ruta | Propósito |
|---|---|
| `~/.claude/` | Configuración global |
| `~/.claude/agents/` | Agentes globales |
| `~/.claude/skills/` | Skills globales |
| `~/.claude/hooks/` | Hooks de interceptación |
| `~/.claude/artefactos/` | Outputs entregados al operador |
| `~/.claude/projects/` | Memoria por proyecto |
| `~/.claude/plantillas/` | Plantillas del sistema (symlink) |
| `~/.config/claude/` | Config XDG (infra, integrations) |
