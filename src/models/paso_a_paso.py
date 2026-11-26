"""Datos de ejemplo para la vista de iteraciones del método Simplex.

La lógica matemática de trazado de iteraciones aún no está implementada.
Estos métodos exponen una estructura estable para que la UI pueda renderizarla.
"""

from fractions import Fraction


def _fraccion(valor):
    return valor if isinstance(valor, Fraction) else Fraction(str(valor))


def _texto_numero(valor):
    numero = _fraccion(valor)
    return str(numero.numerator) if numero.denominator == 1 else f"{numero.numerator}/{numero.denominator}"


def _expresion(terminos):
    """Arma una expresión con signos legibles a partir de (coeficiente, variable)."""
    partes = []
    for coeficiente, variable in terminos:
        valor = _fraccion(coeficiente)
        signo = (" - " if valor < 0 else " + ") if partes else ("-" if valor < 0 else "")
        magnitud = "" if abs(valor) == 1 else _texto_numero(abs(valor))
        partes.append(f"{signo}{magnitud}{variable}")
    return "".join(partes) if partes else "0"


def _generar_forma_estandar(datos_problema, metodo):
    variables = datos_problema.get("variables", [])
    objetivo = datos_problema.get("funcion_objetivo", {})
    restricciones = datos_problema.get("restricciones", [])
    sentido = objetivo.get("sentido", "maximizar")
    coeficientes_objetivo = objetivo.get("coeficientes", [])
    etiqueta_sentido = "Min" if sentido == "minimizar" else "Max"

    terminos_objetivo = [
        (coeficientes_objetivo[i], variable.get("nombre", f"X{i + 1}"))
        for i, variable in enumerate(variables)
        if i < len(coeficientes_objetivo)
    ]
    auxiliares = []
    artificiales = []
    filas = []
    for indice, restriccion in enumerate(restricciones, start=1):
        nombres = [variable.get("nombre", f"X{i + 1}") for i, variable in enumerate(variables)]
        coeficientes = list(restriccion.get("coeficientes", []))
        lado_derecho = _fraccion(restriccion.get("lado_derecho", 0))
        operador = restriccion.get("operador", "<=")
        if lado_derecho < 0:
            coeficientes = [-_fraccion(c) for c in coeficientes]
            lado_derecho = -lado_derecho
            operador = {"<=": ">=", "≥": ">=", ">=": "<=", "≤": "<=", "=": "="}.get(operador, operador)

        terminos = [
            (coeficientes[i], nombre)
            for i, nombre in enumerate(nombres)
            if i < len(coeficientes)
        ]
        if operador in ("<=", "≤"):
            auxiliar = f"S{indice}"
            terminos.append((1, auxiliar))
            auxiliares.append(auxiliar)
        elif operador in (">=", "≥"):
            exceso, artificial = f"E{indice}", f"A{indice}"
            terminos.extend([(-1, exceso), (1, artificial)])
            auxiliares.append(exceso)
            artificiales.append(artificial)
        else:
            artificial = f"A{indice}"
            terminos.append((1, artificial))
            artificiales.append(artificial)
        filas.append(f"{_expresion(terminos)} = {_texto_numero(lado_derecho)}")

    terminos_objetivo.extend((0, nombre) for nombre in auxiliares)
    forma = f"{etiqueta_sentido} Z = {_expresion(terminos_objetivo)}"
    if metodo == "gran_m" and artificiales:
        signo_penalizacion = "+" if sentido == "minimizar" else "-"
        forma += " " + " ".join(f"{signo_penalizacion} M {nombre}" for nombre in artificiales)
    if metodo == "simplex_revisado" and artificiales:
        forma += f"\nFase I: Min W = {_expresion((1, nombre) for nombre in artificiales)}"
    if filas:
        forma += "\n" + "\n".join(filas)
    return forma


class PasoAPaso:
    def generar_gran_m(self, datos_problema):
        """Devuelve iteraciones simuladas con el formato de la tabla Gran M."""
        return {
            "metodo": "gran_m",
            "forma_estandar": _generar_forma_estandar(datos_problema, "gran_m"),
            "columnas": ["Base", "Cb", "X1", "X2", "S1", "S2", "S3", "A1", "RHS"],
            "iteraciones": [
                {
                    "numero": 0,
                    "justificacion": "Tabla inicial: se parte de las variables de holgura.",
                    "prueba_razon_minima": "No aplica en la tabla inicial.",
                    "pivote": "No aplica en la tabla inicial.",
                    "filas": [
                        {"Base": "S1", "Cb": "0", "X1": "2", "X2": "1", "S1": "1", "S2": "0", "S3": "0", "A1": "0", "RHS": "100"},
                        {"Base": "S2", "Cb": "0", "X1": "1", "X2": "2", "S1": "0", "S2": "1", "S3": "0", "A1": "0", "RHS": "80"},
                        {"Base": "S3", "Cb": "0", "X1": "1", "X2": "1", "S1": "0", "S2": "0", "S3": "1", "A1": "0", "RHS": "60"},
                    ],
                },
                {
                    "numero": 1,
                    "justificacion": "Entra X2, Sale S2.",
                    "prueba_razon_minima": "min(100/1, 80/2, 60/1) = 40. El menor valor corresponde a S2, por lo tanto, S2 sale de la base.",
                    "pivote": "2",
                    "filas": [
                        {"Base": "S1", "Cb": "0", "X1": "3/2", "X2": "0", "S1": "1", "S2": "-1/2", "S3": "0", "A1": "0", "RHS": "60"},
                        {"Base": "X2", "Cb": "60", "X1": "1/2", "X2": "1", "S1": "0", "S2": "1/2", "S3": "0", "A1": "0", "RHS": "40"},
                        {"Base": "S3", "Cb": "0", "X1": "1/2", "X2": "0", "S1": "0", "S2": "-1/2", "S3": "1", "A1": "0", "RHS": "20"},
                    ],
                },
            ],
        }

    def generar_simplex_revisado(self, datos_problema):
        """Devuelve iteraciones simuladas con la forma de Simplex Revisado."""
        return {
            "metodo": "simplex_revisado",
            "forma_estandar": _generar_forma_estandar(datos_problema, "simplex_revisado"),
            "columnas": ["Variables Básicas", "B⁻¹", "Costos Reducidos", "RHS"],
            "iteraciones": [
                {
                    "numero": 0,
                    "justificacion": "Base inicial: se evalúan los costos reducidos.",
                    "prueba_razon_minima": "No aplica en la base inicial.",
                    "pivote": "No aplica en la base inicial.",
                    "filas": [
                        {"Variables Básicas": "S1", "B⁻¹": "[1, 0, 0]", "Costos Reducidos": "0", "RHS": "100"},
                        {"Variables Básicas": "S2", "B⁻¹": "[0, 1, 0]", "Costos Reducidos": "0", "RHS": "80"},
                        {"Variables Básicas": "S3", "B⁻¹": "[0, 0, 1]", "Costos Reducidos": "0", "RHS": "60"},
                    ],
                },
                {
                    "numero": 1,
                    "justificacion": "Entra X2, Sale S2. Se actualiza la base y la matriz B⁻¹.",
                    "prueba_razon_minima": "min(100/1, 80/2, 60/1) = 40. El menor valor corresponde a S2, por lo tanto, S2 sale de la base.",
                    "pivote": "2",
                    "filas": [
                        {"Variables Básicas": "S1", "B⁻¹": "[1, -1/2, 0]", "Costos Reducidos": "0", "RHS": "60"},
                        {"Variables Básicas": "X2", "B⁻¹": "[0, 1/2, 0]", "Costos Reducidos": "0", "RHS": "40"},
                        {"Variables Básicas": "S3", "B⁻¹": "[0, -1/2, 1]", "Costos Reducidos": "0", "RHS": "20"},
                    ],
                },
            ],
        }
