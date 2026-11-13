from dataclasses import dataclass
from typing import Literal

from .numero import convertir_fraccion


@dataclass
class FuncionObjetivo:
    sentido: Literal["maximizar", "minimizar"]
    coeficientes: list

    def __post_init__(self):
        if self.sentido not in ("maximizar", "minimizar"):
            raise ValueError(
                "El sentido debe ser 'maximizar' o 'minimizar'."
            )

        self.coeficientes = [
            convertir_fraccion(c)
            for c in self.coeficientes
        ]