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

                "instructions": (
                    "Compare los resultados obtenidos durante la práctica "
                    "experimental con los resultados de la simulación en "
                    "realidad aumentada."
                ),

                "comparison_fields": [

                    {
                        "id": "experimental_result",
                        "label": "Resultado experimental",
                        "type": "TEXT",
                        "required": True,
                    },

                    {
                        "id": "simulation_result",
                        "label": "Resultado de la simulación",
                        "type": "TEXT",
                        "required": True,
                    },

                    {
                        "id": "analysis",
                        "label": "Análisis de la comparación",
                        "type": "TEXT",
                        "required": True,
                    },

                ],

            }

        ]