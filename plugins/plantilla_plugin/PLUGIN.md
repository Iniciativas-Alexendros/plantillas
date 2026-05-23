# PLUGIN.md · Playbook de contenido

> **Propósito**: Los plugins empaquetan agentes, skills, hooks, y MCP servers
> en unidades distribuibles. Un plugin puede instalarse en cualquier proyecto
> o entorno Claude Code para añadir capacidades completas.
>
> **Qué hacer**: Define la estructura del plugin, sus componentes, y cómo
> se distribuye. Elimina estas instrucciones.

---

## INSTRUCCIONES: Estructura del plugin

```
[nombre-del-plugin]/
├── plugin.json           ← Manifest del plugin (metadata + dependencias)
├── README.md             ← Documentación de uso
│
├── agents/               ← Agentes incluidos en el plugin
│   └── [agente].md
│
├── skills/               ← Skills incluidas en el plugin
│   └── [skill]/
│       └── SKILL.md
│
├── hooks/                ← Hooks incluidos en el plugin
│   └── [hook].yaml
│
├── mcp/                  ← MCP servers incluidos en el plugin
│   └── [server]/
│       └── server.py     # o server.ts
│
└── scripts/              ← Scripts de instalación/utilidad
    └── install.sh
```

---

## INSTRUCCIONES: Manifest (plugin.json)

```json
{
  "name": "[nombre-del-plugin]",
  "version": "1.0.0",
  "description": "[Descripción del plugin]",
  "author": "[Tu nombre]",
  "license": "MIT",
  "components": {
    "agents": ["[agente1]", "[agente2]"],
    "skills": ["[skill1]", "[skill2]"],
    "hooks": ["[hook1]"],
    "mcpServers": ["[server1]"]
  },
  "dependencies": {
    "plugins": ["[plugin-requerido]"],
    "mcpServers": ["[mcp-requerido]"]
  },
  "install": {
    "command": "[comando de instalación]",
    "postInstall": "[comando post-instalación]"
  }
}
```

---

## INSTRUCCIONES: Distribución

### Opción 1: Marketplace interno

Publica en un marketplace privado para tu organización:

```bash
# Empaquetar
zip -r mi-plugin.zip mi-plugin/

# Publicar a marketplace
curl -X POST https://tu-marketplace.com/api/plugins \
  -F "file=@mi-plugin.zip" \
  -F "manifest=@mi-plugin/plugin.json"
```

### Opción 2: GitHub Releases

```bash
# Tag y release
git tag v1.0.0
git push origin v1.0.0
# Crear release en GitHub con el zip adjunto
```

### Opción 3: Instalación local

```bash
# Copiar directamente
cp -r mi-plugin ~/.claude/plugins/

# O via symlink para desarrollo
ln -s $(pwd)/mi-plugin ~/.claude/plugins/mi-plugin
```

---

## REFERENCIAS

- **Claude Code: Plugins**: https://code.claude.com/docs/en/plugins.md
- **Claude Code: Plugin Reference**: https://code.claude.com/docs/en/plugins-reference.md
- **Claude Code: Plugin Marketplaces**: https://code.claude.com/docs/en/plugin-marketplaces.md
