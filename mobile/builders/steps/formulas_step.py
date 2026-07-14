class FormulasStep:

    def __init__(self, laboratorio):
        self.laboratorio = laboratorio

    def build(self):

        formulas = self.laboratorio.formulas.all()

        if not formulas.exists():
            return []

        return [
            {
                "id": "formulas",
                "order": 5,
                "type": "FORMULAS",
                "title": "Fórmulas",
                "required": True,
                "formulas": [
                    {
                        "id": formula.id,
                        "name": formula.nombre,
                        "expression": formula.expresion,
                        "description": formula.descripcion
                    }
                    for formula in formulas
                ]
            }
        ]