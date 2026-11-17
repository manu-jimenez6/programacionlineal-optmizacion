
from flask import Flask, jsonify, render_template, request

from src.models import FuncionObjetivo, Problema, Restriccion, Variable


app = Flask(
    __name__,
    template_folder="src/ui",
    static_folder="src/ui",
    static_url_path=""
)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/api/validar", methods=["POST"])
def validar_problema():

    try:
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict):
            return jsonify({
                "ok": False,
                "error": "No se recibieron datos válidos."
            }), 400

        # 1. Obtener las variables
        variables_datos = datos.get("variables")

        if not isinstance(variables_datos, list) or not variables_datos:
            raise ValueError("Debes ingresar al menos una variable.")

        variables = []

        for variable in variables_datos:
            if not isinstance(variable, dict):
                raise ValueError("El formato de una variable no es válido.")

            nombre = variable.get("nombre")

            if not isinstance(nombre, str) or not nombre.strip():
                raise ValueError("Hay una variable sin nombre.")

            no_negativa = variable.get("no_negativa", True)

            variables.append(
                Variable(
                    nombre=nombre,
                    no_negativa=no_negativa
                )
            )

        # 2. Construir la función objetivo
        objetivo_datos = datos.get("funcion_objetivo")

        if not isinstance(objetivo_datos, dict):
            raise ValueError("La función objetivo no es válida.")

        sentido = objetivo_datos.get("sentido")
        coeficientes_objetivo = objetivo_datos.get("coeficientes")

        if not isinstance(coeficientes_objetivo, list):
            raise ValueError("Faltan los coeficientes de la función objetivo.")

        objetivo = FuncionObjetivo(
            sentido=sentido,
            coeficientes=coeficientes_objetivo
        )

        # 3. Construir las restricciones
        restricciones_datos = datos.get("restricciones")

        if not isinstance(restricciones_datos, list):
            raise ValueError("Las restricciones deben enviarse como una lista.")

        restricciones = []

        for i, restriccion in enumerate(restricciones_datos):

            if not isinstance(restriccion, dict):
                raise ValueError(f"La restricción {i + 1} no es válida.")

            coeficientes = restriccion.get("coeficientes")
            operador = restriccion.get("operador")
            lado_derecho = restriccion.get("lado_derecho")

            if not isinstance(coeficientes, list):
                raise ValueError(
                    f"Faltan los coeficientes de la restricción {i + 1}."
                )

            if lado_derecho is None or str(lado_derecho).strip() == "":
                raise ValueError(
                    f"Falta el lado derecho de la restricción {i + 1}."
                )

            restricciones.append(
                Restriccion(
                    coeficientes=coeficientes,
                    operador=operador,
                    lado_derecho=lado_derecho
                )
            )

        # 4. Construir y validar el problema completo
        problema = Problema(
            variables=variables,
            funcion_objetivo=objetivo,
            restricciones=restricciones
        )

        return jsonify({
            "ok": True,
            "mensaje": "El problema fue recibido y validado correctamente.",
            "cantidad_variables": len(problema.variables),
            "cantidad_restricciones": len(problema.restricciones)
        })

    except (ValueError, TypeError, KeyError) as error:

        return jsonify({
            "ok": False,
            "error": str(error)
        }), 400


if __name__ == "__main__":
    app.run(debug=True)


