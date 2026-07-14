class QuestionsStep:

    def __init__(self, laboratorio):

        self.laboratorio = laboratorio

    def build(self):

        preguntas = self.laboratorio.preguntas.all()

        if not preguntas.exists():
            return []

        return [
            {
                "id": "questions",
                "order": 10,
                "type": "QUESTIONS",
                "title": "Preguntas del laboratorio",
                "required": True,
                "description": (
                    "Responde las preguntas asociadas al desarrollo del laboratorio."
                ),
                "questions": [
                    {
                        "id": pregunta.id,
                        "key": pregunta.key,
                        "question_type": pregunta.tipo,
                        "title": pregunta.titulo,
                        "prompt": pregunta.enunciado,
                        "input_type": pregunta.input_type,
                        "required": pregunta.required,
                        "order": pregunta.order,
                        "options": pregunta.options,
                        "evaluation_hint": pregunta.evaluation_hint,
                    }
                    for pregunta in preguntas
                ]
            }
        ]