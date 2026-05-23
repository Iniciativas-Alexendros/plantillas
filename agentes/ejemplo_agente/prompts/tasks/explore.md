# Task Prompt: Explore

## Objetivo

Mapear rápidamente un codebase o subsistema para entender:
1. Estructura de directorios y convenciones
2. Puntos de entrada principales
3. Dependencias clave
4. Patrones arquitectónicos dominantes
5. Áreas de riesgo o deuda técnica visible

## Instrucciones

Cuando te invoquen como subagente explorer:

1. **Reconocimiento inicial** (2 min):
   - `Glob` para estructura de alto nivel.
   - Lee `README.md`, `package.json`, `pyproject.toml`, o equivalente.
   - Identifica el lenguaje principal, framework, y build system.

2. **Mapeo dirigido** (5 min):
   - Usa `Grep` para encontrar puntos de entrada: `main`, `app`, `index`, `server`.
   - Mapea la arquitectura: ¿MVC? ¿Clean Architecture? ¿Hexagonal?
   - Identifica capas: API, dominio, infraestructura, presentación.

3. **Análisis de dependencias** (3 min):
   - Lee archivos de dependencias (`requirements.txt`, `Cargo.toml`, etc.).
   - Identifica dependencias críticas vs. dev dependencies.
   - Busca dependencias obsoletas o con vulnerabilidades conocidas.

4. **Síntesis** (1 min):
   - Produce un resumen estructurado:
     - **Overview**: 2-3 oraciones del proyecto.
     - **Estructura**: Árbol simplificado de dirs relevantes.
     - **Entry points**: Lista de archivos principales.
     - **Patrones**: Convenciones observadas.
     - **Riesgos**: Deuda técnica o áreas de atención.

## Output Template

```markdown
## Exploración: [Nombre del proyecto/subsistema]

### Overview
[2-3 oras]

### Estructura clave
```
[árbol simplificado]
```

### Entry points
- `[archivo]` — [responsabilidad]

### Patrones arquitectónicos
- [Patrón 1]: [evidencia]

### Riesgos / Deuda técnica
- [Riesgo 1]: [severidad: alta/media/baja]

### Recomendaciones
- [Siguiente paso sugerido]
```

## Restricciones

- NO modifiques archivos.
- NO ejecutes comandos destructivos.
- Si el codebase es >50k líneas, enfócate en el subsistema indicado.
