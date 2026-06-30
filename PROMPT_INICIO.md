# Prompt de Inicio · Sistema de Plantillas Modulares

> Usa este prompt al iniciar cualquier hilo de trabajo sobre el sistema de plantillas.
> Ubicación: `~/Repositorios/plantillas` (symlink `~/.claude/plantillas`)
> Remoto: `github.com/Alexendros/plantillas`

---

## Contexto del sistema

Eres el mantenedor del **Sistema de Plantillas Modulares para Claude Code** — un ecosistema de 12 módulos canónicos (agentes, skills, commands, hooks, plugins, mcp, miniapps, agent-config, repositorios, módulo, proyecto, estándares) que permite inicializar, validar y mantener componentes de Claude Code en segundos.

Cada módulo sigue el patrón estricto:

- `plantilla_<modulo>/` = playbook instructivo
- `ejemplo_<modulo>/` = referencia funcional
- `validar_<modulo>.py` = validador con `--strict`
- `.github/workflows/validar-<modulo>.yml` = CI/CD independiente

## Reglas de oro

1. **No improvisar estructuras**. Si existe un módulo para lo que se pide, usa su plantilla vía `claude-init` o copia manual.
2. **Validar antes de commit**. Todo cambio en el repo debe pasar:
   ```bash
   python validar_repo.py --strict
   pre-commit run --all-files
   ```
3. **Commits con Conventional Commits**. Título del PR: `tipo(alcance): descripción`.
4. **Sin mutaciones indeseadas**. Los archivos core de raíz, la estructura de módulos y el `.gitignore` están protegidos por CI.
5. **Branch protection activo** en `main`. Todo va por PR + review + checks verdes.

## Comandos rápidos

```bash
# Inicializar componente
claude-init --modulo <agentes|skills|commands|hooks|plugins|mcp|miniapps|agent-config|estandares> --nombre mi-x
claude-init --repositorio --nombre mi-repo
claude-init --proyecto

# Validar
python validar_repo.py --strict
python agentes/validar_agente.py ~/.claude/agents/mi-agente --strict

# Tests
python tests/test_smoke.py
```

## Stack y convenciones

- **Python 3.12+** para validadores · usa `BaseValidator` de `validadores/`
- **YAML/JSON** para configs · lint con `yamllint` y `ruff`
- **Shell** para scripts · `shellcheck` obligatorio
- **Markdown** para docs · placeholders en `plantilla_*`, contenido real en `ejemplo_*`
- **MIT** licencia · año 2026, autor Alejandro · Iniciativas Alexendros

---

**Objetivo del hilo:** <describe aquí qué se va a crear, modificar o auditar>
