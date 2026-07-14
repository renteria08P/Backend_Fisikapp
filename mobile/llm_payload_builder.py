def to_iso(value):
    if not value:
        return None

    if hasattr(value, "isoformat"):
        return value.isoformat()

    return value


class LLMPayloadBuilder:

    def __init__(
        self,
        user,
        assignment,
        submission_data
    ):
        self.user = user
        self.assignment = assignment
        self.submission_data = submission_data

    def build(self):

        laboratorio = self.assignment.laboratorio
        plantilla = laboratorio.plantilla
        grupo = self.assignment.grupo

        return {
            "schema_version": "1.0",
            "evaluation_type": "LABORATORY_SUBMISSION",

            "student": {
                "id": self.user.id,
                "name": self.user.nombre,
                "email": self.user.correo,
            },

            "group": {
                "id": grupo.id,
                "name": grupo.nombre,
                "grade": grupo.grado,
                "jornada": grupo.jornada,
            },

            "assignment": {
                "id": self.assignment.id,
                "start_date": to_iso(self.assignment.fecha_inicio),
                "due_date": to_iso(self.assignment.fecha_fin),
                "status": self.assignment.estado,
            },

            "laboratory": {
                "id": laboratorio.id,
                "title": laboratorio.titulo,
                "category": (
                    plantilla.categoria.nombre
                    if plantilla.categoria
                    else None
                ),
                "summary": laboratorio.resumen,
                "introduction": laboratorio.introduccion,
                "theory": laboratorio.marco_teorico,
            },

            "submission": {
                "practice": self.submission_data.get(
                    "practice",
                    {}
                ),
                "simulation": self.submission_data.get(
                    "simulation",
                    {}
                ),
                "comparison": self.submission_data.get(
                    "comparison",
                    {}
                ),
                "questions": self.submission_data.get(
                    "questions",
                    []
                ),
                "report": self.submission_data.get(
                    "report",
                    {}
                ),
                "device": self.submission_data.get(
                    "device",
                    {}
                ),
            },

            "evaluation_instructions": {
                "language": "es",
                "expected_output": {
                    "score": "number from 0 to 100",
                    "feedback": "string",
                    "strengths": "array of strings",
                    "improvements": "array of strings",
                    "teacher_review_required": True
                },
                "criteria": [
                    "Comprensión del marco teórico.",
                    "Coherencia entre práctica, simulación y comparación.",
                    "Calidad de las respuestas a preguntas.",
                    "Claridad del informe.",
                    "Análisis de resultados y conclusiones."
                ]
            }
        }