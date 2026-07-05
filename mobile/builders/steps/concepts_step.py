class ConceptsStep:

    def __init__(self, laboratorio):
        self.laboratorio = laboratorio

    def build(self):

        conceptos = self.laboratorio.conceptos_laboratorio.select_related(
            "concepto"
        ).prefetch_related(
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
                        "id": concepto.concepto.id,
                        "name": concepto.concepto.concepto,
                        "description": concepto.concepto.descripcion,
                        "example": concepto.concepto.ejemplo,
                        "type": concepto.concepto.tipo,
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