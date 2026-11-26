"""Datos de ejemplo para la vista de iteraciones del método Simplex.

La lógica matemática de trazado de iteraciones aún no está implementada.
Estos métodos exponen una estructura estable para que la UI pueda renderizarla.
"""


class PasoAPaso:
    def generar_gran_m(self, datos_problema):
        """Devuelve iteraciones simuladas con el formato de la tabla Gran M."""
        return {
            "metodo": "gran_m",
            "columnas": ["Base", "Cb", "X1", "X2", "S1", "S2", "S3", "A1", "RHS"],
            "iteraciones": [
                {
                    "numero": 0,
                    "justificacion": "Tabla inicial: se parte de las variables de holgura.",
                    "filas": [
                        {"Base": "S1", "Cb": "0", "X1": "2", "X2": "1", "S1": "1", "S2": "0", "S3": "0", "A1": "0", "RHS": "100"},
                        {"Base": "S2", "Cb": "0", "X1": "1", "X2": "2", "S1": "0", "S2": "1", "S3": "0", "A1": "0", "RHS": "80"},
                        {"Base": "S3", "Cb": "0", "X1": "1", "X2": "1", "S1": "0", "S2": "0", "S3": "1", "A1": "0", "RHS": "60"},
                    ],
                },
                {
                    "numero": 1,
                    "justificacion": "Entra X2, Sale S2. Se realiza el pivote sobre la segunda restricción.",
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
            "columnas": ["Variables Básicas", "B⁻¹", "Costos Reducidos", "RHS"],
            "iteraciones": [
                {
                    "numero": 0,
                    "justificacion": "Base inicial: se evalúan los costos reducidos.",
                    "filas": [
                        {"Variables Básicas": "S1", "B⁻¹": "[1, 0, 0]", "Costos Reducidos": "0", "RHS": "100"},
                        {"Variables Básicas": "S2", "B⁻¹": "[0, 1, 0]", "Costos Reducidos": "0", "RHS": "80"},
                        {"Variables Básicas": "S3", "B⁻¹": "[0, 0, 1]", "Costos Reducidos": "0", "RHS": "60"},
                    ],
                },
                {
                    "numero": 1,
                    "justificacion": "Entra X2, Sale S2. Se actualiza la base y la matriz B⁻¹.",
                    "filas": [
                        {"Variables Básicas": "S1", "B⁻¹": "[1, -1/2, 0]", "Costos Reducidos": "0", "RHS": "60"},
                        {"Variables Básicas": "X2", "B⁻¹": "[0, 1/2, 0]", "Costos Reducidos": "0", "RHS": "40"},
                        {"Variables Básicas": "S3", "B⁻¹": "[0, -1/2, 1]", "Costos Reducidos": "0", "RHS": "20"},
                    ],
                },
            ],
        }
