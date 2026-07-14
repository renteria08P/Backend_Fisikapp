PARABOLIC_CONFIG = {
    "lab_key": "PARABOLIC-001",
    "unity_scene_name": "ParabolicMotionLab",
    "display_name": "Movimiento parabólico AR",
    "version": "1.0.0",
    "intro_title": "Práctica AR de movimiento parabólico",
    "intro_text": (
        "Ajusta el ángulo y la velocidad inicial para intentar "
        "alcanzar el objetivo. Observa cómo cambia la trayectoria "
        "del proyectil."
    ),
    "instructions": [
        "Ubica una superficie plana.",
        "Coloca el punto de lanzamiento.",
        "Ajusta velocidad y ángulo.",
        "Realiza el lanzamiento.",
        "Observa la distancia al objetivo."
    ],
    "max_attempts": 4,
    "allow_resume": True,
    "requires_camera": True,
    "options": {
        "language": "es",
        "show_projectile_camera_option": True,
        "show_trajectory_preview": True,
        "show_distance_indicators": True,
        "allow_audio": True
    },
    "parameters": {
        "gravity": -9.81,
        "gravity_unit": "m/s^2",
        "min_velocity": 1.0,
        "max_velocity": 20.0,
        "velocity_unit": "m/s",
        "min_angle": 0.1,
        "max_angle": 75,
        "angle_unit": "degrees"
    }
}

SIMULACIONES = {
    "PARABOLIC-001": PARABOLIC_CONFIG,
}