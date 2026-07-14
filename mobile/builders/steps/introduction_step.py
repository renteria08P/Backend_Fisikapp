class IntroductionStep:

    def __init__(self, laboratorio):

        self.laboratorio = laboratorio

    def build(self):

        if not self.laboratorio.introduccion:

            return []

        return [

            {

                "id": "introduction",

                "order": 1,

                "type": "INTRODUCTION",

                "title": "Introducción",

                "required": True,

                "content": [

                    {

                        "type": "TEXT",

                        "value": self.laboratorio.introduccion

                    }

                ]

            }

        ]