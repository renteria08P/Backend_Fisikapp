class FormulasStep:

    def __init__(self, laboratorio):
        self.laboratorio = laboratorio

    def build(self):

        print("LABORATORIO:", self.laboratorio.id)

        formulas = self.laboratorio.formulas.all()

        print("TOTAL FORMULAS:", formulas.count())

        print(list(formulas.values()))

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