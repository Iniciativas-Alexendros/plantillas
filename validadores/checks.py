"""
Checks individuales reutilizables.
Cada función devuelve una lista de Resultados.
"""

import json
import re
from pathlib import Path
from typing import List, Optional

from .base import BaseValidator, Nivel, Resultado

# Intentar importar yaml
try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ──────────────────────────────────────────────────────────────────────────
# Check: Frontmatter YAML
# ──────────────────────────────────────────────────────────────────────────


def check_yaml_frontmatter(
    validator: BaseValidator,
    archivo: Path,
    campos_requeridos: Optional[List[str]] = None,
) -> List[Resultado]:
    """Valida que un archivo .md tenga frontmatter YAML válido."""
    resultados: List[Resultado] = []
    rel = validator._rel(archivo)

    content = archivo.read_text(encoding="utf-8")
    if not content.startswith("---"):
        resultados.append(
            Resultado(Nivel.ERROR, "frontmatter", f"{rel} no comienza con '---'", rel)
        )
        return resultados

    parts = content.split("---", 2)
    if len(parts) < 3:
        resultados.append(
            Resultado(
                Nivel.ERROR, "frontmatter", f"{rel} tiene frontmatter malformado", rel
            )
        )
        return resultados

    yaml_text = parts[1].strip()
    if not yaml_text:
        resultados.append(
            Resultado(Nivel.ERROR, "frontmatter", f"{rel} tiene frontmatter vacío", rel)
        )
        return resultados

    if not HAS_YAML:
        resultados.append(
            Resultado(
                Nivel.WARNING,
                "frontmatter",
                f"{rel} no se puede validar (instala 'pyyaml')",
                rel,
            )
        )
        return resultados

    try:
        data = yaml.safe_load(yaml_text)
    except Exception as e:
        resultados.append(
            Resultado(Nivel.ERROR, "frontmatter", f"{rel} YAML inválido: {e}", rel)
        )
        return resultados

    if not isinstance(data, dict):
        resultados.append(
            Resultado(
                Nivel.ERROR,
                "frontmatter",
                f"{rel} frontmatter no es un diccionario",
                rel,
            )
        )
        return resultados

    # Validar campos requeridos
    if campos_requeridos:
        for campo in campos_requeridos:
            if campo not in data:
                resultados.append(
                    Resultado(
                        Nivel.ERROR,
                        "frontmatter",
                        f"{rel} falta campo obligatorio '{campo}'",
                        rel,
                    )
                )

    # Validar formato de 'name' si existe
    if "name" in data and isinstance(data["name"], str):
        if not re.match(r"^[a-z0-9-]+$", data["name"]):
            resultados.append(
                Resultado(
                    Nivel.WARNING,
                    "frontmatter",
                    f"{rel} 'name' debe ser kebab-case: '{data['name']}'",
                    rel,
                )
            )

    return resultados


# ──────────────────────────────────────────────────────────────────────────
# Check: JSON parseable
# ──────────────────────────────────────────────────────────────────────────


def check_json_parseable(
    validator: BaseValidator,
    archivo: Path,
) -> List[Resultado]:
    """Valida que un archivo JSON sea parseable."""
    resultados: List[Resultado] = []
    rel = validator._rel(archivo)

    try:
        json.loads(archivo.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        resultados.append(
            Resultado(Nivel.ERROR, "json", f"{rel} JSON inválido: {e}", rel)
        )
    return resultados


# ──────────────────────────────────────────────────────────────────────────
# Check: YAML parseable
# ──────────────────────────────────────────────────────────────────────────


def check_yaml_parseable(
    validator: BaseValidator,
    archivo: Path,
) -> List[Resultado]:
    """Valida que un archivo YAML sea parseable."""
    resultados: List[Resultado] = []
    rel = validator._rel(archivo)

    if not HAS_YAML:
        resultados.append(
            Resultado(
                Nivel.WARNING,
                "yaml",
                f"{rel} no se puede validar (instala 'pyyaml')",
                rel,
            )
        )
        return resultados

    try:
        yaml.safe_load(archivo.read_text(encoding="utf-8"))
    except Exception as e:
        resultados.append(
            Resultado(Nivel.ERROR, "yaml", f"{rel} YAML inválido: {e}", rel)
        )
    return resultados


# ──────────────────────────────────────────────────────────────────────────
# Check: Placeholders sin rellenar
# ──────────────────────────────────────────────────────────────────────────


def check_placeholders(
    validator: BaseValidator,
    archivos_ignorados: Optional[List[str]] = None,
    extensiones: tuple = (".md", ".json", ".yaml", ".yml", ".txt"),
    patrones_extra: Optional[List] = None,
) -> List[Resultado]:
    """Busca placeholders sin rellenar en archivos del módulo."""
    resultados: List[Resultado] = []
    ignorados = set(archivos_ignorados or [])
    patrones = list(validator.PLACEHOLDER_PATTERNS)
    if patrones_extra:
        patrones.extend(patrones_extra)

    for p in validator._archivos():
        if p.name in ignorados:
            continue
        if p.suffix not in extensiones:
            continue

        content = p.read_text(encoding="utf-8")
        rel = validator._rel(p)

        # Para .md, solo buscar fuera de codeblocks
        if p.suffix == ".md":
            searchable = validator._extraer_fuera_codeblock(content)
        else:
            searchable = content

        for pattern in patrones:
            matches = pattern.findall(searchable)
            if matches:
                unique = list(dict.fromkeys(matches))[:3]
                resultados.append(
                    Resultado(
                        Nivel.ERROR,
                        "placeholder",
                        f"{rel} contiene placeholders sin rellenar: {unique}",
                        rel,
                    )
                )
                break  # Un error por archivo es suficiente

    return resultados


# ──────────────────────────────────────────────────────────────────────────
# Check: Archivos vacíos
# ──────────────────────────────────────────────────────────────────────────


def check_archivos_vacios(
    validator: BaseValidator,
    min_bytes: int = 50,
    archivos_ignorados: Optional[List[str]] = None,
) -> List[Resultado]:
    """Detecta archivos sospechosamente pequeños."""
    resultados: List[Resultado] = []
    ignorados = set(archivos_ignorados or [])

    for p in validator._archivos():
        if ".git" in p.parts:
            continue
        if p.name in ignorados:
            continue
        if p.stat().st_size < min_bytes:
            rel = validator._rel(p)
            resultados.append(
                Resultado(
                    Nivel.WARNING,
                    "vacio",
                    f"{rel} tiene solo {p.stat().st_size} bytes (¿contenido pendiente?)",
                    rel,
                )
            )

    return resultados


# ──────────────────────────────────────────────────────────────────────────
# Check: Estructura de directorios
# ──────────────────────────────────────────────────────────────────────────


def check_estructura(
    validator: BaseValidator,
    dirs_requeridos: List[str],
    archivos_requeridos: List[str],
) -> List[Resultado]:
    """Valida que existan directorios y archivos obligatorios."""
    resultados: List[Resultado] = []

    for d in dirs_requeridos:
        p = validator.ruta / d
        if not p.is_dir():
            resultados.append(
                Resultado(
                    Nivel.ERROR, "estructura", f"Falta directorio obligatorio: {d}/"
                )
            )

    for f in archivos_requeridos:
        p = validator.ruta / f
        if not p.is_file():
            resultados.append(
                Resultado(Nivel.ERROR, "estructura", f"Falta archivo obligatorio: {f}")
            )

    return resultados


# ──────────────────────────────────────────────────────────────────────────
# Checks a nivel repositorio (reutilizables por validadores globales)
#
# Recorren todo el árbol bajo validator.ruta. _archivos() incluye .git, así
# que estos checks lo excluyen explícitamente para preservar el comportamiento.
# ──────────────────────────────────────────────────────────────────────────


def check_archivos_prohibidos(
    validator: BaseValidator,
    patrones_prohibidos: List[str],
) -> List[Resultado]:
    """Detecta archivos que nunca deben estar en el repo (nombre exacto o glob '*.ext')."""
    resultados: List[Resultado] = []
    for path in validator._archivos():
        if ".git" in path.parts:
            continue
        name = path.name
        for prohibido in patrones_prohibidos:
            if prohibido.startswith("*"):
                if name.endswith(prohibido.lstrip("*")):
                    resultados.append(
                        Resultado(
                            Nivel.ERROR,
                            "archivos_prohibidos",
                            f"Archivo prohibido detectado: {name}",
                            validator._rel(path),
                        )
                    )
            elif name == prohibido:
                resultados.append(
                    Resultado(
                        Nivel.ERROR,
                        "archivos_prohibidos",
                        f"Archivo prohibido detectado: {name}",
                        validator._rel(path),
                    )
                )
    return resultados


def check_tamanio_maximo(
    validator: BaseValidator,
    max_kb: float,
) -> List[Resultado]:
    """Ningún archivo debe superar max_kb kilobytes."""
    resultados: List[Resultado] = []
    for path in validator._archivos():
        if ".git" in path.parts:
            continue
        size_kb = path.stat().st_size / 1024
        if size_kb > max_kb:
            resultados.append(
                Resultado(
                    Nivel.ERROR,
                    "tamanio_archivos",
                    f"Archivo excede {max_kb}KB ({size_kb:.1f}KB): {path.name}",
                    validator._rel(path),
                )
            )
    return resultados


def check_merge_conflicts(
    validator: BaseValidator,
    max_bytes: int = 5 * 1024 * 1024,
) -> List[Resultado]:
    """Detecta marcadores de conflicto de merge no resueltos."""
    resultados: List[Resultado] = []
    for path in validator._archivos():
        if ".git" in path.parts:
            continue
        if path.stat().st_size > max_bytes:
            continue  # Ignorar archivos muy grandes
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if any(line.startswith("<<<<<<<") for line in text.splitlines()):
            resultados.append(
                Resultado(
                    Nivel.ERROR,
                    "merge_conflicts",
                    f"Marcadores de merge conflict no resueltos en: {path.name}",
                    validator._rel(path),
                )
            )
    return resultados


def check_secrets(
    validator: BaseValidator,
    patrones: "List[re.Pattern]",
    max_bytes: int = 2 * 1024 * 1024,
) -> List[Resultado]:
    """Heurística básica de detección de secrets en texto plano."""
    resultados: List[Resultado] = []
    for path in validator._archivos():
        if ".git" in path.parts:
            continue
        if path.stat().st_size > max_bytes:
            continue  # Ignorar binarios y archivos grandes
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern in patrones:
            matches = pattern.findall(text)
            if matches:
                resultados.append(
                    Resultado(
                        Nivel.ERROR,
                        "secrets_texto_plano",
                        f"Posible secret/token detectado en {path.name}: {matches[0][:20]}...",
                        validator._rel(path),
                    )
                )
                break  # Un hallazgo por archivo es suficiente
    return resultados


def check_gitignore_minimo(
    validator: BaseValidator,
    entradas: List[str],
) -> List[Resultado]:
    """Verifica que .gitignore (en validator.ruta) contenga exclusiones mínimas."""
    resultados: List[Resultado] = []
    gi = validator.ruta / ".gitignore"
    if not gi.is_file():
        resultados.append(
            Resultado(
                Nivel.ERROR, "gitignore", "Falta .gitignore en raíz", ".gitignore"
            )
        )
        return resultados

    content = gi.read_text(encoding="utf-8")
    for req in entradas:
        pattern = req.lstrip("/")
        if pattern not in content and f"/{pattern}" not in content:
            resultados.append(
                Resultado(
                    Nivel.WARNING,
                    "gitignore",
                    f".gitignore no excluye explícitamente: {req}",
                    ".gitignore",
                )
            )
    return resultados
