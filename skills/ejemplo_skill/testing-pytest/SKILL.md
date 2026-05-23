---
name: testing-pytest
description: >
  Escribe, organiza y refactoriza tests con pytest.
  Usa cuando el usuario trabaje con código Python y necesite:
  crear tests, mejorar cobertura, parametrizar casos, o usar fixtures.
allowed-tools:
  - Read
  - Grep
  - Edit
  - Write
  - Bash
context:
  - pytest.ini
---

# Testing con pytest

## Cuándo usar

- El usuario pide "escribe tests para esto", "aumenta cobertura", etc.
- Se refactoriza código legacy y se necesitan tests de regresión.
- Se revisa un PR y los tests son insuficientes o frágiles.

## Reglas

### Estructura de tests

- Un archivo de test por módulo: `test_<modulo>.py`.
- Clases de test solo cuando agrupan lógicamente ≥3 métodos relacionados.
- Nombres de test descriptivos: `test_<función>_<escenario>_<resultado_esperado>`.

### Fixtures

- Usa `conftest.py` para fixtures compartidas.
- Scope mínimo necesario: `function` por defecto, `session` solo para bases de datos o servidores.
- Nunca uses `setup`/`teardown` de unittest; usa fixtures con `yield`.

### Parametrización

- Parametriza cuando ≥3 casos con la misma lógica pero diferentes entradas/resultados.
- Usa `ids` para que los nombres de los casos sean legibles en el reporte.

### Mocks

- Prefiere `unittest.mock` (o `pytest-mock`) sobre mocks manuales.
- Mock a nivel de función/método, no a nivel de clase entera.
- Verifica que el mock se llamó con los argumentos esperados (`assert_called_once_with`).

## Anti-patrones

1. **Tests que dependen del orden de ejecución**
   - Solución: Cada test debe ser independiente; usar fixtures para estado.

2. **Sleep en tests**
   - Solución: Usar `freezegun` para tiempo, `pytest-asyncio` para async.

3. **Assert genérico sin mensaje**
   - Solución: `assert resultado == esperado, f"Esperado {esperado}, got {resultado}"`

## Plantilla

```python
import pytest
from unittest.mock import Mock, patch

from mi_modulo import funcion_a_testear


class TestFuncionATestear:
    """Tests para funcion_a_testear."""

    @pytest.mark.parametrize(
        "entrada,esperado",
        [
            ("caso_1", "resultado_1"),
            ("caso_2", "resultado_2"),
        ],
        ids=["caso_simple", "caso_complejo"],
    )
    def test_funcion_caso_simple(self, entrada, esperado):
        resultado = funcion_a_testear(entrada)
        assert resultado == esperado

    @patch("mi_modulo.dependencia_externa")
    def test_funcion_con_mock(self, mock_dep):
        mock_dep.return_value = {"status": "ok"}
        resultado = funcion_a_testear("input")
        mock_dep.assert_called_once_with("input")
        assert resultado["status"] == "ok"
```

## Checklist

- [ ] ¿Cada test tiene una sola razón para fallar?
- [ ] ¿Las fixtures tienen el scope mínimo necesario?
- [ ] ¿Hay tests para casos límite (vacío, nulo, máximo)?
- [ ] ¿Los mocks verifican las llamadas, no solo el resultado?
