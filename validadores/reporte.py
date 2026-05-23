"""
Formateo y reporte de resultados de validación.
"""

from typing import List

from .base import Nivel, Resultado


def reportar_resultados(resultados: List[Resultado], strict: bool = False) -> int:
    """
    Imprime resultados formateados y devuelve código de salida.

    Returns:
        0 si todo OK (o solo warnings en modo no-strict)
        1 si hay errores (o warnings en modo strict)
    """
    errores = [r for r in resultados if r.nivel == Nivel.ERROR]
    warnings = [r for r in resultados if r.nivel == Nivel.WARNING]
    ok = [r for r in resultados if r.nivel == Nivel.OK]

    if errores:
        print(f"❌ ERRORES ({len(errores)}):")
        for e in errores:
            archivo = f" ({e.archivo})" if e.archivo else ""
            print(f"   • [{e.check}]{archivo} — {e.mensaje}")
        print()

    if warnings:
        print(f"⚠️  WARNINGS ({len(warnings)}):")
        for w in warnings:
            archivo = f" ({w.archivo})" if w.archivo else ""
            print(f"   • [{w.check}]{archivo} — {w.mensaje}")
        print()

    if ok and not errores and not warnings:
        print(f"✅ {len(ok)} checks pasaron correctamente")

    if not errores and not warnings:
        print("✅ TODAS LAS VALIDACIONES PASARON")
        return 0

    if not errores:
        print("✅ Sin errores. Solo warnings (aceptables en modo no-strict)")
        if strict:
            print("❌ Modo strict activo: los warnings cuentan como fallo")
            return 1
        return 0

    print(f"❌ VALIDACIÓN FALLIDA: {len(errores)} errores")
    return 1
