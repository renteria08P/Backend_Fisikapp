class ResourceBuilder:

    def __init__(self, laboratorio):

        self.laboratorio = laboratorio

    def build(self):

        return {

            "id": self.laboratorio.id,

            "type": "LABORATORY",

            "title": self.laboratorio.titulo,

            "category": self.laboratorio.categoria.nombre,

            "teacher": self.laboratorio.profesor.nombre,

            "summary": self.laboratorio.resumen,

            "created_at": self.laboratorio.fecha_creacion,

            "generated_ai": self.laboratorio.generado_ia

        }