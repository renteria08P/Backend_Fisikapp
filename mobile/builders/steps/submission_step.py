class SubmissionStep:

    def __init__(self, assignment):

        self.assignment = assignment

    def build(self):

        return [

            {

                "id": "submission",

                "order": 11,

                "type": "SUBMISSION",

                "title": "Entrega del laboratorio",

                "required": True,

                "instructions": (
                    "Cuando haya completado todas las etapas del laboratorio, "
                    "envíe la información para su revisión."
                ),

                "submission": {

                    "endpoint": (
                        f"/api/mobile/simulation/"
                        f"{self.assignment.id}/results/"
                    ),

                    "method": "POST",

                    "confirmation_message": (
                        "¿Desea enviar el laboratorio?"
                    )

                }

            }

        ]