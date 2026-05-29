# CLAUDE.md · Playbook de contenido

> **Propósito**: Este es el archivo más importante de todo el ecosistema `.claude/`.
> Claude Code lo lee al inicio de **cada sesión** y aplica sus instrucciones
> como contexto persistente. Es la "constitución" de tu entorno.
>
> **Qué hacer**: Desarrolla cada sección con contenido específico de TU
> entorno, stack tecnológico, y preferencias personales. Elimina estas
> instrucciones al final.
>
> **Referencia**: https://code.claude.com/docs/en/memory.md

---

## SECCIÓN 1: Identidad y Alcance

### Qué desarrollar aquí

Define quién eres tú (el usuario), qué hace Claude en tu entorno, y cuál es
el alcance de sus operaciones.

```markdown
# [Tagline personal o de proyecto]

## Introducción · Norma global

Norma global para la administración de Claude en todos los hilos del usuario [tu nombre].

<scope
  path-canonico="[ruta al .claude/]"
  os="[tu SO: EndeavourOS / Ubuntu / macOS / etc.]"
  de="[tu entorno de escritorio]"
  gestores="[gestores de paquetes: pacman+yay / apt / brew]"
  home="[tu home directory]"
  alcance="[qué gestiona Claude: todo el entorno / solo proyectos / etc.]"
/>

Stack online: [lista de herramientas y servicios que usas].
```

#### Campos obligatorios:

| Campo | Qué poner | Ejemplo |
|---|---|---|
| **Tagline** | Frase de identidad | `'OPUS NOSTRUM, ARMA PURA.'` |
| **SO** | Sistema operativo y versión | `EndeavourOS (Arch rolling)` |
| **DE** | Entorno de escritorio | `GNOME Shell sobre Wayland` |
| **Gestores** | Gestores de paquetes disponibles | `pacman+yay+flatpak` |
| **Home** | Ruta del home directory | `/home/alexendros` |
| **Stack** | Herramientas online que usas | `Git · Vercel · Stripe · Proton` |

---

## SECCIÓN 2: Maestrías / Roles

### Qué desarrollar aquí

Define las "maestrías" o roles que Claude puede asumir. Esto ayuda al
enrutamiento de tareas y a mantener consistencia de comportamiento.

```markdown
## 1. Maestría · cómo decidir

Antes de responder: activa `[comando de enrutamiento]` para iniciar workflow seleccionador.

<maestrias>
  <maestria nombre="[Nombre]" color-ansi="[código]" dominio="[descripción]"/>
  <maestria nombre="[Nombre]" color-ansi="[código]" dominio="[descripción]"/>
</maestrias>

<pre-check secuencia="estricta">
  <paso n="1">elegir maestría aplicable</paso>
  <paso n="2">invocar skill aplicable vía tool `Skill`</paso>
  <paso n="3">elegir agente especializado si aplica</paso>
</pre-check>
```

#### Ejemplo de maestrías:

| Maestría | Color | Dominio |
|---|---|---|
| Claude | 208 (naranja) | Meta: skills, hooks, agentes, memoria |
| Ingeniero | 141 (morado) | Código, infra, despliegue, tests |
| Ejecutivo | 78 (verde) | Finanzas, cartera, decisiones de negocio |
| Legal | 196 (rojo) | Compliance, contratos, normativa |

---

## SECCIÓN 3: Doctrinas y Reglas Globales

### Qué desarrollar aquí

Reglas que aplican a **todas** las sesiones, independientemente del proyecto.

```markdown
## 2. Doctrinas Globales

### Seguridad
- Toda escalada usa `sudouth` (NO `sudo` directo).
- Secrets solo en archivos `.env` (nunca en código).
- Prohibido `git push` sin confirmación explícita.

### Calidad
- Todo código nuevo lleva tests.
- Revisión de código antes de merge.
- Documentación actualizada con cada cambio significativo.

### Workflow
- Usar `TodoWrite` para tracking visible.
- Delegar a subagentes cuando sea posible.
- Compartir contexto mínimo pero suficiente.
```

---

## SECCIÓN 4: Integraciones y Configuración

### Qué desarrollar aquí

Puntos de integración con tu stack tecnológico.

```markdown
## 3. Integraciones

| Servicio | Uso | Configuración |
|---|---|---|
| [Servicio 1] | [Para qué lo usas] | [Cómo se configura] |
| [Servicio 2] | [Para qué lo usas] | [Cómo se configura] |

### MCP Servers activos
Ver `mcp.json` para la configuración completa.

### Skills globales
Ver `skills/` para el catálogo completo.
```

---

## SECCIÓN 5: Árbol de directorios `.claude/`

El ecosistema `.claude/` sigue un árbol plano. Cada directorio tiene un propósito
semántico claro:

```
~/.claude/
├── agents/          ← Agentes especializados (subagentes Claude Code)
├── skills/          ← Skills reutilizables (auto-activables por descripción)
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

### Rutas importantes

| Ruta | Propósito |
|---|---|
| `~/.claude/CLAUDE.md` | Norma global (este archivo) |
| `~/.claude/settings.json` | Permisos, hooks, env |
| `~/.claude/mcp.json` | Servidores MCP globales |
| `~/.claude/agents/` | Agentes especializados |
| `~/.claude/skills/` | Skills globales |
| `~/.claude/projects/` | Memoria por proyecto |

---

## REFERENCIAS

- **Claude Code: Memory & CLAUDE.md**: https://code.claude.com/docs/en/memory.md
- **Claude Code: CLAUDE.md Best Practices**: https://code.claude.com/docs/en/best-practices.md
- **Claude Code: Context Window**: https://code.claude.com/docs/en/context-window.md
