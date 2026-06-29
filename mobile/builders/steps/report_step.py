class ReportStep:

    def __init__(self, laboratorio):

        self.laboratorio = laboratorio

    def build(self):

        return [

            {

                "id": "report",

                "order": 10,

                "type": "REPORT",

                "title": "Informe de laboratorio",

                "required": True,

                "report": {

                    "instructions": (
                        "Complete el informe final del laboratorio con base "
                        "en los resultados obtenidos durante la práctica "
                        "experimental y la simulación."
                    ),

                    "include_practice": True,

                    "include_simulation": True,

                    "include_comparison": True,

                    "sections": [

                        {
                            "id": "results",
                            "label": "Resultados obtenidos",
                            "type": "TEXT",
                            "required": True,
                        },

                        {
                            "id": "analysis",
                            "label": "Análisis",
                            "type": "TEXT",
                            "required": True,
                        },

                        {
                            "id": "conclusions",
                            "label": "Conclusiones",
                            "type": "TEXT",
                            "required": True,
                        }

                    ]

                }

            }

        ]