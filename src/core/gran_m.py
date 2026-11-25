from fractions import Fraction


def _mostrar(numero):
    "esto es para mostrar fracciones de manera bonita basicamente"
    numero = Fraction(numero)
    return str(numero.numerator) if numero.denominator == 1 else f"{numero.numerator}/{numero.denominator}"


def resolver_gran_m(problema):

    columnas = []
    costos = []
    nombres = []
    filas = []
    lados = []
    base = []
    tipos = []
    artificiales = set()

    # Primero normalizan RHS negativos y se crean las columnas de decision.
    for j, variable in enumerate(problema.variables):
        if not variable.no_negativa:
            raise ValueError("Por ahora todas las variables deben ser no negativas.")
        nombres.append(variable.nombre)
        c = problema.funcion_objetivo.coeficientes[j]
        costos.append(c if problema.funcion_objetivo.sentido == "maximizar" else -c)

    for restriccion in problema.restricciones:
        fila = list(restriccion.coeficientes)
        rhs = restriccion.lado_derecho
        operador = restriccion.operador
        if rhs < 0:
            fila = [-valor for valor in fila]
            rhs = -rhs
            operador = {"<=": ">=", ">=": "<=", "=": "="}[operador]
        filas.append(fila)
        lados.append(rhs)
        tipos.append(operador)

    # Las columnas de decision se crean despues de normalizar cada fila.
    for j in range(len(problema.variables)):
        columnas.append([fila[j] for fila in filas])

    # Slack for <=; surplus and artificial for >=; artificial for =.
    base = [None] * len(filas)
    for i, operador in enumerate(tipos):
        if operador == "<=":
            columna = [Fraction(int(k == i)) for k in range(len(filas))]
            columnas.append(columna)
            nombres.append(f"S{i + 1}")
            costos.append((Fraction(0), Fraction(0)))
            base[i] = len(columnas) - 1
        else:
            if operador == ">=":
                columna = [Fraction(-int(k == i)) for k in range(len(filas))]
                columnas.append(columna)
                nombres.append(f"E{i + 1}")
                costos.append((Fraction(0), Fraction(0)))
            columna = [Fraction(int(k == i)) for k in range(len(filas))]
            columnas.append(columna)
            nombres.append(f"A{i + 1}")
            costos.append((Fraction(0), Fraction(-1)))
            base[i] = len(columnas) - 1
            artificiales.add(base[i])

    # Cada fila representa una ecuacion; se pivotea hasta que no haya mejora.
    tabla = []
    for i in range(len(filas)):
        fila = [columna[i] for columna in columnas]
        tabla.append([Fraction(v) for v in fila] + [Fraction(lados[i])])

    def costo_base(i):
        j = base[i]
        if isinstance(costos[j], tuple):
            return costos[j]
        return (costos[j], Fraction(0))

    max_iteraciones = max(100, 20 * (len(tabla) + len(columnas)))
    for _ in range(max_iteraciones):
        reducidos = []
        for j in range(len(columnas)):
            cb_a = sum((costo_base(i)[0] * tabla[i][j] for i in range(len(tabla))), Fraction(0))
            cb_m = sum((costo_base(i)[1] * tabla[i][j] for i in range(len(tabla))), Fraction(0))
            cj = costos[j] if isinstance(costos[j], tuple) else (costos[j], Fraction(0))
            reducidos.append((cj[0] - cb_a, cj[1] - cb_m))

        # M es simbolicamente mayor que cualquier numero: primero comparamos
        # su coeficiente y luego la parte normal.
        entra = next((j for j, c in enumerate(reducidos)
                      if c[1] > 0 or (c[1] == 0 and c[0] > 0)), None)
        if entra is None:
            break

        candidatos = [(tabla[i][-1] / tabla[i][entra], i)
                      for i in range(len(tabla)) if tabla[i][entra] > 0]
        if not candidatos:
            return {"estado": "no_acotado", "mensaje": "El problema tiene una solucion no acotada."}
        _, sale = min(candidatos)

        pivote = tabla[sale][entra]
        tabla[sale] = [v / pivote for v in tabla[sale]]
        for i in range(len(tabla)):
            if i != sale:
                factor = tabla[i][entra]
                tabla[i] = [tabla[i][j] - factor * tabla[sale][j] for j in range(len(columnas) + 1)]
        base[sale] = entra
    else:
        return {"estado": "error", "mensaje": "El metodo excedio el limite de iteraciones."}

    # Si una artificial sigue positiva, las restricciones son incompatibles.
    for i, j in enumerate(base):
        if j in artificiales and tabla[i][-1] != 0:
            return {"estado": "infactible", "mensaje": "El problema no tiene solucion factible."}

    valores = [Fraction(0) for _ in nombres]
    for i, j in enumerate(base):
        valores[j] = tabla[i][-1]
    variables = {nombre: _mostrar(valores[i]) for i, nombre in enumerate(nombres[:len(problema.variables)])}
    z = sum((c * valores[j] for j, c in enumerate(problema.funcion_objetivo.coeficientes)), Fraction(0))

    restricciones_resultado = []
    x = [valores[j] for j in range(len(problema.variables))]
    for i, r in enumerate(problema.restricciones):
        usado = sum((a * b for a, b in zip(r.coeficientes, x)), Fraction(0))
        diferencia = r.lado_derecho - usado
        holgura = diferencia if r.operador == "<=" else (-diferencia if r.operador == ">=" else Fraction(0))
        restricciones_resultado.append({
            "nombre": f"R{i + 1}", "usado": _mostrar(usado),
            "lado_derecho": _mostrar(r.lado_derecho), "holgura_exceso": _mostrar(holgura),
            "estado": "Activa" if holgura == 0 else "Con holgura/exceso"
        })

    return {"estado": "optimo", "mensaje": "Solucion optima encontrada.",
            "variables": variables, "z": _mostrar(z), "restricciones": restricciones_resultado}
