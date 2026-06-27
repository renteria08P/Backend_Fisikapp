class SimulationConfigBuilder:

    def __init__(self, assignment):

        self.assignment = assignment
        self.laboratorio = assignment.laboratorio

    def build(self):

        return {

            "lab_key": "PARABOLIC-001",

            "unity_scene_name": "ParabolicMotionLab",

            "display_name": "Movimiento Parabólico",

            "version": "1.0.0",

            "enabled": True,

            "intro_title": "Práctica AR de Movimiento Parabólico",

            "intro_text": self.laboratorio.resumen,

            "instructions": self.build_instructions(),

            "max_attempts": 4,

            "allow_resume": True,

            "requires_camera": True,

            "options": self.build_options(),

            "parameters": self.build_parameters()

        }

    def build_instructions(self):

        return [
            paso.descripcion
            for paso in self.laboratorio.procedimientos.all()
        ]

    def build_options(self):

        return {

            "language": "es",

            "show_projectile_camera_option": True,

            "show_trajectory_preview": True,

            "show_distance_indicators": True,

            "allow_audio": True

        }

    def build_parameters(self):

        return {

            "gravity": -9.81,

            "gravity_unit": "m/s²",

            "min_velocity": 1,

            "max_velocity": 20,

            "velocity_unit": "m/s",

            "min_angle": 0,

            "max_angle": 75,

            "angle_unit": "degrees"

        }