class AssignmentBuilder:

    def __init__(self, assignment):
        self.assignment = assignment

    def build(self):

        return {

            "assignment_id": self.assignment.id,

            "group_id": self.assignment.grupo.id,

            "group_name": self.assignment.grupo.nombre,

            "start_date": self.assignment.fecha_inicio,

            "due_date": self.assignment.fecha_fin,

            "status": self.assignment.estado

        }