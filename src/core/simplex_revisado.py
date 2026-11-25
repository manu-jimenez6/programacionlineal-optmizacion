"""Simplex revisado exacto usando dos fases y aritmética racional.

En cada iteración se calcula B^-1 desde la base actual. No se mantiene ni se
actualiza un tableau completo como en Gran M.
"""
from fractions import Fraction


def _mostrar(numero):
    numero = Fraction(numero)
    return str(numero.numerator) if numero.denominator == 1 else f"{numero.numerator}/{numero.denominator}"


def _inversa(matriz):
    """Invierte una matriz cuadrada mediante eliminación Gauss-Jordan."""
    n = len(matriz)
    aumentada = [list(map(Fraction, fila)) + [Fraction(int(i == j)) for j in range(n)]
                 for i, fila in enumerate(matriz)]
    for columna in range(n):
        pivote = next((fila for fila in range(columna, n)
                       if aumentada[fila][columna] != 0), None)
        if pivote is None:
            raise ValueError("La base del Simplex revisado es singular.")
        aumentada[columna], aumentada[pivote] = aumentada[pivote], aumentada[columna]
        valor = aumentada[columna][columna]
        aumentada[columna] = [x / valor for x in aumentada[columna]]
        for fila in range(n):
            if fila == columna:
                continue
            factor = aumentada[fila][columna]
            aumentada[fila] = [aumentada[fila][j] - factor * aumentada[columna][j]
                               for j in range(2 * n)]
    return [fila[n:] for fila in aumentada]


def _producto(matriz, vector):
    return [sum((a * b for a, b in zip(fila, vector)), Fraction(0)) for fila in matriz]


def _optimizar(columnas, rhs, costos, base, permitidas, max_iteraciones):
    """Maximiza c*x desde una base factible y devuelve valores y estado."""
    for _ in range(max_iteraciones):
        b = [[columnas[j][i] for j in base] for i in range(len(rhs))]
        inversa = _inversa(b)
        x_base = _producto(inversa, rhs)
        costos_base = [costos[j] for j in base]
        # y = c_B^T B^-1
        y = [sum((costos_base[i] * inversa[i][j] for i in range(len(base))), Fraction(0))
             for j in range(len(rhs))]

        entra = None
        for j in permitidas:
            if j in base:
                continue
            reducido = costos[j] - sum((y[i] * columnas[j][i] for i in range(len(rhs))), Fraction(0))
            if reducido > 0:
                entra = j
                break
        if entra is None:
            return "optimo", base, x_base

        direccion = _producto(inversa, columnas[entra])
        razones = [(x_base[i] / direccion[i], i) for i in range(len(rhs)) if direccion[i] > 0]
        if not razones:
            return "no_acotado", base, x_base
        _, fila_sale = min(razones)
        base[fila_sale] = entra
    return "error", base, []


def resolver_simplex_revisado(problema):
    """Resuelve un problema lineal usando Simplex revisado de dos fases."""
    if not problema.restricciones:
        return {"estado": "no_acotado", "mensaje": "Se requiere al menos una restricción para formar una base inicial."}
    if any(not variable.no_negativa for variable in problema.variables):
        raise ValueError("Por ahora todas las variables deben ser no negativas.")

    m = len(problema.restricciones)
    n = len(problema.variables)
    filas, rhs, operadores = [], [], []
    for restriccion in problema.restricciones:
        fila, lado, operador = list(restriccion.coeficientes), restriccion.lado_derecho, restriccion.operador
        if lado < 0:
            fila = [-x for x in fila]
            lado = -lado
            operador = {"<=": ">=", ">=": "<=", "=": "="}[operador]
        filas.append(fila)
        rhs.append(lado)
        operadores.append(operador)

    nombres = [v.nombre for v in problema.variables]
    columnas = [[filas[i][j] for i in range(m)] for j in range(n)]
    base, artificiales = [None] * m, set()
    for i, operador in enumerate(operadores):
        if operador == "<=":
            columna = [Fraction(int(k == i)) for k in range(m)]
            columnas.append(columna)
            nombres.append(f"S{i + 1}")
            base[i] = len(columnas) - 1
        else:
            if operador == ">=":
                columnas.append([Fraction(-int(k == i)) for k in range(m)])
                nombres.append(f"E{i + 1}")
            columnas.append([Fraction(int(k == i)) for k in range(m)])
            nombres.append(f"A{i + 1}")
            base[i] = len(columnas) - 1
            artificiales.add(base[i])

    limite = max(100, 20 * (m + len(columnas)))
    # Fase I: maximizar -suma(artificiales), para encontrar una base factible.
    costos_fase1 = [Fraction(0)] * len(columnas)
    for j in artificiales:
        costos_fase1[j] = Fraction(-1)
    estado, base, x_base = _optimizar(
        columnas, rhs, costos_fase1, base, range(len(columnas)), limite
    )
    if estado == "error":
        return {"estado": "error", "mensaje": "El método excedió el límite de iteraciones en la fase I."}
    if estado == "no_acotado":
        return {"estado": "error", "mensaje": "No se pudo completar la fase I del método."}
    valor_fase1 = sum((costos_fase1[j] * x_base[i] for i, j in enumerate(base)), Fraction(0))
    if valor_fase1 != 0:
        return {"estado": "infactible", "mensaje": "El problema no tiene solución factible."}

    sentido = problema.funcion_objetivo.sentido
    costos = [Fraction(0)] * len(columnas)
    for j, c in enumerate(problema.funcion_objetivo.coeficientes):
        costos[j] = c if sentido == "maximizar" else -c
    permitidas = [j for j in range(len(columnas)) if j not in artificiales]
    estado, base, x_base = _optimizar(columnas, rhs, costos, base, permitidas, limite)
    if estado == "error":
        return {"estado": "error", "mensaje": "El método excedió el límite de iteraciones en la fase II."}
    if estado == "no_acotado":
        return {"estado": "no_acotado", "mensaje": "El problema tiene una solución no acotada."}

    valores = [Fraction(0)] * len(columnas)
    for i, j in enumerate(base):
        valores[j] = x_base[i]
    variables = {nombres[j]: _mostrar(valores[j]) for j in range(n)}
    z = sum((c * valores[j] for j, c in enumerate(problema.funcion_objetivo.coeficientes)), Fraction(0))

    detalles = []
    for i, restriccion in enumerate(problema.restricciones):
        usado = sum((a * valores[j] for j, a in enumerate(restriccion.coeficientes)), Fraction(0))
        diferencia = restriccion.lado_derecho - usado
        holgura = diferencia if restriccion.operador == "<=" else (
            -diferencia if restriccion.operador == ">=" else Fraction(0)
        )
        detalles.append({
            "nombre": f"R{i + 1}", "usado": _mostrar(usado),
            "lado_derecho": _mostrar(restriccion.lado_derecho),
            "holgura_exceso": _mostrar(holgura),
            "estado": "Activa" if holgura == 0 else "Con holgura/exceso",
        })
    return {
        "estado": "optimo", "mensaje": "Solución óptima encontrada con Simplex revisado.",
        "variables": variables, "z": _mostrar(z), "restricciones": detalles,
    }
