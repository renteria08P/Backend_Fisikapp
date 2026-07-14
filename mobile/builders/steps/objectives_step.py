from laboratorios.models import ObjetivoGeneral


class ObjectivesStep:

    def __init__(self, laboratorio):
        self.laboratorio = laboratorio

    def build(self):

        try:
            objetivo = self.laboratorio.objetivo_general
        except ObjetivoGeneral.DoesNotExist:
            return []

        if not objetivo.descripcion:
            return []

        return [
            {
                "id": "objectives",
                "order": 3,
                "type": "OBJECTIVES",
                "title": "Objetivos",
                "required": True,

                "general": {
                    "description": objetivo.descripcion
                },

                "specifics": [
                    {
                        "description": item.descripcion
                    }
                    for item in objetivo.objetivos_especificos.all()
                ]
            }
        ]