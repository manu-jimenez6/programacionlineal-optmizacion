from dataclasses import dataclass


@dataclass
class Variable:
    nombre: str
    no_negativa: bool = True

    def __post_init__(self):
        if not self.nombre.strip():
            raise ValueError("El nombre de la variable no puede estar vacío.")