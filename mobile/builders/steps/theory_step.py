class TheoryStep:

    def __init__(self, laboratorio):

        self.laboratorio = laboratorio

    def build(self):

        if not self.laboratorio.marco_teorico:
            return []

        return [

            {

                "id": "theory",

                "order": 2,

                "type": "THEORY",

                "title": "Marco teórico",

                "required": True,

                "content": [

                    {

                        "type": "TEXT",

                        "value": self.laboratorio.marco_teorico

                    }

                ]

            }

        ]