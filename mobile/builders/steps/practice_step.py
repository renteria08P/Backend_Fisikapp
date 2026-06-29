class PracticeStep:

    def __init__(self, laboratorio):
        self.laboratorio = laboratorio

    def build(self):

        practicas = self.laboratorio.practicas.all()

        if not practicas.exists():
            return []

        procedimientos = self.laboratorio.procedimientos.all()

        return [
            {
                "id": "experimental_practice",
                "order": 7,
                "type": "EXPERIMENTAL_PRACTICE",
                "title": "Práctica experimental",
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
                                "description": concepto.descripcion,
                            }
                            for concepto in practica.conceptos.all()
                        ],
                    }
                    for practica in practicas
                ],

                "procedure": [
                    {
                        "number": paso.paso_numero,
                        "description": paso.descripcion,
                        "image": (
                            paso.imagen.url
                            if paso.imagen
                            else None
                        ),
                        "order": paso.orden,
                    }
                    for paso in procedimientos
                ],

                "expected_inputs": [
                    {
                        "id": "observations",
                        "type": "TEXT",
                        "label": "Observaciones",
                        "required": True,
                    },

                    {
                        "id": "calculations",
                        "type": "TEXT",
                        "label": "Cálculos realizados",
                        "required": True,
                    },

                    {
                        "id": "conclusions",
                        "type": "TEXT",
                        "label": "Conclusiones",
                        "required": True,
                    },

                    {
                        "id": "evidences",
                        "type": "FILES",
                        "label": "Evidencias",
                        "required": False,
                        "allowed_types": [
                            "image/*",
                            "application/pdf",
                        ],
                        "multiple": True,
                    },

                ],
            }
        ]