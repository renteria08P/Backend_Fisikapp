class SimulationARStep:

    def __init__(self, assignment):

        self.assignment = assignment

    def build(self):

        laboratorio = self.assignment.laboratorio

        ar_config = getattr(
            laboratorio,
            "simulacion_ar_config",
            None
        )

        if not ar_config or not ar_config.enabled:
            return []

        return [
            {
                "id": "simulation_ar",
                "order": 8,
                "type": "SIMULATION_AR",
                "title": "Simulación AR",
                "required": True,
                "description": (
                    "Ejecuta la simulación AR asociada al laboratorio."
                ),
                "simulation_ref": {
                    "ar_id": ar_config.id,
                    "lab_key": ar_config.lab_key,
                    "unity_scene_name": ar_config.unity_scene_name,
                    "display_name": ar_config.display_name,
                    "config_endpoint": (
                        f"/api/mobile/ar/{ar_config.id}/"
                    )
                }
            }
        ]