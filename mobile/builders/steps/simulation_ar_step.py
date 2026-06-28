class SimulationARStep:

    def __init__(self, assignment):

        self.assignment = assignment

    def build(self):

        laboratorio = self.assignment.laboratorio

        lab_key = laboratorio.plantilla.lab_key

        if not lab_key:
            return []

        return [

            {

                "id": "simulation_ar",

                "order": 8,

                "type": "SIMULATION_AR",

                "title": "Simulación AR",

                "required": True,

                "simulation_ref": {

                    "endpoint": (
                        f"/api/mobile/simulation/"
                        f"{self.assignment.id}/"
                    ),

                    "lab_key": lab_key

                }

            }

        ]