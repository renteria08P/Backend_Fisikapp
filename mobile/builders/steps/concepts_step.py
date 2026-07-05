class ConceptsStep:

    def __init__(self, laboratorio):
        self.laboratorio = laboratorio

    def build(self):

        conceptos = self.laboratorio.conceptos_laboratorio.prefetch_related(
            "recursos"
        )

        if not conceptos.exists():
            return []

        return [
            {
                "id": "concepts",
                "order": 4,
                "type": "CONCEPTS",
                "title": "Conceptos básicos",
                "required": True,
                "concepts": [
                    {
                        "id": concepto.id,
                        "name": concepto.concepto,
                        "description": concepto.descripcion,
                        "example": concepto.ejemplo,
                        "type": concepto.tipo,
                        "resources": [
                            {
                                "id": recurso.id,
                                "name": recurso.nombre,
                                "url": recurso.url,
                            }
                            for recurso in concepto.recursos.all()
                        ]
                    }
                    for concepto in conceptos
                ]
            }
        ]