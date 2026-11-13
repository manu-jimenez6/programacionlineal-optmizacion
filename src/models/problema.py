from dataclasses import dataclass

from .variable import Variable
from .funcion_objetivo import FuncionObjetivo
from .restriccion import Restriccion


@dataclass
class Problema:
    variables: list[Variable]
    funcion_objetivo: FuncionObjetivo
    restricciones: list[Restriccion]

    def __post_init__(self):
        self.validar()

    def validar(self):
        cantidad_variables = len(self.variables)

        if cantidad_variables == 0:
            raise ValueError(
                "El problema debe tener al menos una variable."
            )

        if not isinstance(self.funcion_objetivo, FuncionObjetivo):
            raise TypeError("La función objetivo no es válida.")

        if len(self.funcion_objetivo.coeficientes) != cantidad_variables:
            raise ValueError(
                "La cantidad de coeficientes de la función objetivo "
                "no coincide con la cantidad de variables."
            )

        nombres = [v.nombre for v in self.variables]

        if len(nombres) != len(set(nombres)):
            raise ValueError("No puede haber variables con nombres repetidos.")

        for i, restriccion in enumerate(self.restricciones):
            if not isinstance(restriccion, Restriccion):
                raise TypeError(f"La restricción {i + 1} no es válida.")

            if len(restriccion.coeficientes) != cantidad_variables:
                raise ValueError(
                    f"La restricción {i + 1} tiene "
                    f"{len(restriccion.coeficientes)} coeficientes, "
                    f"pero hay {cantidad_variables} variables."
                )

        return True