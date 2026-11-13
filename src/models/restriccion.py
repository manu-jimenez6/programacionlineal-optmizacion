from dataclasses import dataclass
from typing import Literal

from .numero import convertir_fraccion


@dataclass
class Restriccion:
    coeficientes: list
    operador: Literal["<=", ">=", "="]
    lado_derecho: object

    def __post_init__(self):
        if self.operador not in ("<=", ">=", "="):
            raise ValueError(
                "El operador debe ser '<=', '>=' o '='."
            )

        self.coeficientes = [
            convertir_fraccion(c)
            for c in self.coeficientes
        ]

        self.lado_derecho = convertir_fraccion(
            self.lado_derecho
        )