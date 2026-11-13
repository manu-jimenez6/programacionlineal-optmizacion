from fractions import Fraction


def convertir_fraccion(valor):
    """
    Convierte enteros, decimales, cadenas y fracciones
    a un objeto Fraction.
    """
    if isinstance(valor, Fraction):
        return valor

    try:
        return Fraction(str(valor))
    except (ValueError, ZeroDivisionError):
        raise ValueError(f"Coeficiente numérico inválido: {valor}")