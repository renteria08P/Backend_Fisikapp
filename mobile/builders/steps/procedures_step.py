class ProceduresStep:

    def __init__(self, laboratorio):
        self.laboratorio = laboratorio

    def build(self):

        procedimientos = self.laboratorio.procedimientos.all()

        if not procedimientos.exists():
            return []

        return [
            {
                "id": "procedures",
                "order": 6,
                "type": "PROCEDURES",
                "title": "Procedimiento",
                "required": True,
                "steps": [
                    {
                        "number": procedimiento.paso_numero,
                        "description": procedimiento.descripcion,
                        "image": (
                            procedimiento.imagen.url
                            if procedimiento.imagen
                            else None
                        ),
                        "order": procedimiento.orden,
                    }
                    for procedimiento in procedimientos
                ]
            }
        ]
    