class PracticeStep:

    def __init__(self, laboratorio):
        self.laboratorio = laboratorio

    def build(self):

        practicas = self.laboratorio.practicas.all()

        print("TOTAL PRACTICAS:", practicas.count())

        if not practicas.exists():
            return []

        return [
            {
                "id": "practice",
                "order": 7,
                "type": "PRACTICE",
                "title": "Práctica",
                "required": True,
                "practices": [
                    {
                        "id": practica.id,
                        "name": practica.nombre_practica,
                        "objective": practica.objetivo,
                        "description": practica.descripcion,
                        "materials": practica.materiales,
                        "calculations": practica.calculos,
                        "concepts": [
                            {
                                "id": concepto.id,
                                "name": concepto.concepto,
                                "description": concepto.descripcion
                            }
                            for concepto in practica.conceptos.all()
                        ]
                    }
                    for practica in practicas
                ]
            }
        ]