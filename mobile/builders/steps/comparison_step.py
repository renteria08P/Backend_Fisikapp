class ComparisonStep:

    def __init__(self, laboratorio):
        self.laboratorio = laboratorio

    def build(self):

        return [
            {
                "id": "comparison",
                "order": 9,
                "type": "COMPARISON",
                "title": "Comparación de resultados",
                "required": True,

                "comparison": {

                    "left_source": "experimental_practice",

                    "right_source": "simulation_ar",

                    "instructions": (
                        "Compare los resultados registrados durante la práctica "
                        "experimental con los obtenidos en la simulación AR."
                    ),

                    "fields": [
                        {
                            "id": "analysis",
                            "label": "Análisis de la comparación",
                            "type": "TEXT",
                            "required": True,
                        }

                    ]
                }
            }
        ]