from .assignment_builder import AssignmentBuilder
from .resource_builder import ResourceBuilder

from .steps.introduction_step import IntroductionStep
from .steps.theory_step import TheoryStep
from .steps.objectives_step import ObjectivesStep
from .steps.concepts_step import ConceptsStep
from .steps.formulas_step import FormulasStep
from .steps.procedures_step import ProceduresStep
from .steps.practice_step import PracticeStep
from .steps.simulation_ar_step import SimulationARStep
from .steps.comparison_step import ComparisonStep
from .steps.report_step import ReportStep
from .steps.submission_step import SubmissionStep


class MobileResourceBuilder:

    def __init__(self, assignment):

        self.assignment = assignment

    def build(self):

        laboratorio = self.assignment.laboratorio

        steps = [

            *IntroductionStep(laboratorio).build(),
            *TheoryStep(laboratorio).build(),
            *ObjectivesStep(laboratorio).build(),
            *ConceptsStep(laboratorio).build(),
            *FormulasStep(laboratorio).build(),
            *ProceduresStep(laboratorio).build(),
            *PracticeStep(laboratorio).build(),
            *SimulationARStep(self.assignment).build(),
            *ComparisonStep(laboratorio).build(),
            *ReportStep(laboratorio).build(),
            *SubmissionStep(self.assignment).build(),

        ]

        # Recalcular el orden de los steps existentes
        for index, step in enumerate(steps, start=1):
            step["order"] = index

        return {

            "assignment": AssignmentBuilder(
                self.assignment
            ).build(),

            "resource": ResourceBuilder(
                laboratorio
            ).build(),

            "steps": steps,

        }