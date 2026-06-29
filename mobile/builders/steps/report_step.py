class ReportStep:

    def __init__(self, laboratorio):

        self.laboratorio = laboratorio

    def build(self):
        practicas = self.laboratorio.practicas.exists()

        lab_key = self.laboratorio.plantilla.lab_key is not None


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
                    "en los resultados obtenidos."
                ),

                "include_practice": practicas,

                "include_simulation": lab_key,

                "include_comparison": practicas and lab_key,

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