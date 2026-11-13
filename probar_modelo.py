
from fractions import Fraction

from src.models import (
    Variable,
    FuncionObjetivo,
    Restriccion,
    Problema
)


def ejecutar_prueba(nombre, funcion):
    """Ejecuta una prueba y muestra si pasó o falló."""
    print(f"\n{'=' * 55}")
    print(f"PRUEBA: {nombre}")
    print("=" * 55)

    try:
        funcion()
        print("RESULTADO: CORRECTO")
    except Exception as error:
        print(f"RESULTADO: ERROR DETECTADO")
        print(f"Tipo: {type(error).__name__}")
        print(f"Mensaje: {error}")


# =====================================================
# PRUEBA 1: CREAR UN PROBLEMA VÁLIDO DE MAXIMIZACIÓN
# =====================================================

def prueba_maximizacion():
    variables = [
        Variable("x1"),
        Variable("x2")
    ]

    objetivo = FuncionObjetivo(
        sentido="maximizar",
        coeficientes=[3, 5]
    )

    restricciones = [
        Restriccion([1, 2], "<=", 8),
        Restriccion([3, 1], ">=", 6)
    ]

    problema = Problema(
        variables,
        objetivo,
        restricciones
    )

    print("Sentido:", problema.funcion_objetivo.sentido)
    print("Variables:", [v.nombre for v in problema.variables])
    print("Función objetivo:", problema.funcion_objetivo.coeficientes)

    for i, r in enumerate(problema.restricciones):
        print(
            f"Restricción {i + 1}:",
            r.coeficientes,
            r.operador,
            r.lado_derecho
        )

    assert problema.validar() is True


# =====================================================
# PRUEBA 2: CREAR UN PROBLEMA VÁLIDO DE MINIMIZACIÓN
# =====================================================

def prueba_minimizacion():
    variables = [
        Variable("x1"),
        Variable("x2")
    ]

    objetivo = FuncionObjetivo(
        sentido="minimizar",
        coeficientes=[4, 7]
    )

    restricciones = [
        Restriccion([2, 1], ">=", 10),
        Restriccion([1, 3], ">=", 12)
    ]

    problema = Problema(
        variables,
        objetivo,
        restricciones
    )

    assert problema.funcion_objetivo.sentido == "minimizar"
    assert problema.validar() is True

    print("Problema de minimización creado correctamente.")


# =====================================================
# PRUEBA 3: SOPORTE DE ENTEROS, DECIMALES Y FRACCIONES
# =====================================================

def prueba_numeros():
    restriccion = Restriccion(
        coeficientes=[5, "2.5", "1/3"],
        operador="<=",
        lado_derecho="7/2"
    )

    print("Coeficientes:", restriccion.coeficientes)
    print("Lado derecho:", restriccion.lado_derecho)

    assert restriccion.coeficientes == [
        Fraction(5),
        Fraction(5, 2),
        Fraction(1, 3)
    ]

    assert restriccion.lado_derecho == Fraction(7, 2)

    print("Todos los números se convirtieron correctamente.")


# =====================================================
# PRUEBA 4: RECHAZAR SENTIDO DE OPTIMIZACIÓN INVÁLIDO
# =====================================================

def prueba_sentido_invalido():
    FuncionObjetivo(
        sentido="sumar",
        coeficientes=[3, 5]
    )


# =====================================================
# PRUEBA 5: RECHAZAR OPERADOR INVÁLIDO
# =====================================================

def prueba_operador_invalido():
    Restriccion(
        coeficientes=[1, 2],
        operador="!=",
        lado_derecho=10
    )


# =====================================================
# PRUEBA 6: RECHAZAR DIMENSIONES INCORRECTAS
# =====================================================

def prueba_dimensiones_incorrectas():
    variables = [
        Variable("x1"),
        Variable("x2")
    ]

    objetivo = FuncionObjetivo(
        sentido="maximizar",
        coeficientes=[3, 5]
    )

    restricciones = [
        Restriccion(
            coeficientes=[1, 2, 3],
            operador="<=",
            lado_derecho=10
        )
    ]

    # Debe fallar porque hay 3 coeficientes y 2 variables.
    Problema(
        variables,
        objetivo,
        restricciones
    )


# =====================================================
# PRUEBA 7: RECHAZAR PROBLEMA SIN VARIABLES
# =====================================================

def prueba_sin_variables():
    objetivo = FuncionObjetivo(
        sentido="maximizar",
        coeficientes=[]
    )

    Problema(
        variables=[],
        funcion_objetivo=objetivo,
        restricciones=[]
    )


# =====================================================
# PRUEBA 8: RECHAZAR VARIABLES CON NOMBRES REPETIDOS
# =====================================================

def prueba_variables_repetidas():
    variables = [
        Variable("x1"),
        Variable("x1")
    ]

    objetivo = FuncionObjetivo(
        sentido="maximizar",
        coeficientes=[3, 5]
    )

    Problema(
        variables,
        objetivo,
        []
    )


# =====================================================
# EJECUCIÓN DE TODAS LAS PRUEBAS
# =====================================================

if __name__ == "__main__":

    pruebas = [
        ("Maximización válida", prueba_maximizacion),
        ("Minimización válida", prueba_minimizacion),
        ("Enteros, decimales y fracciones", prueba_numeros),
        ("Sentido de optimización inválido", prueba_sentido_invalido),
        ("Operador inválido", prueba_operador_invalido),
        ("Dimensiones incorrectas", prueba_dimensiones_incorrectas),
        ("Problema sin variables", prueba_sin_variables),
        ("Variables repetidas", prueba_variables_repetidas)
    ]

    exitos = 0

    print("\nINICIANDO PRUEBAS DEL MODELO DE DATOS")

    for nombre, prueba in pruebas:
        try:
            prueba()
            print(f"\n[CORRECTO] {nombre}")
            exitos += 1

        except (ValueError, TypeError, AssertionError) as error:
            # Las pruebas inválidas deben generar ValueError o TypeError.
            if nombre in [
                "Sentido de optimización inválido",
                "Operador inválido",
                "Dimensiones incorrectas",
                "Problema sin variables",
                "Variables repetidas"
            ]:
                print(f"\n[CORRECTO] {nombre}: error esperado.")
                print(f"  {error}")
                exitos += 1
            else:
                print(f"\n[FALLÓ] {nombre}: {error}")

        except Exception as error:
            print(f"\n[FALLÓ] {nombre}: {error}")

    print("\n" + "=" * 55)
    print(f"RESULTADO FINAL: {exitos}/{len(pruebas)} pruebas superadas")
    print("=" * 55)
