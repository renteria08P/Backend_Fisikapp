from django.db import transaction
from entregas.models import (
    Entrega,
    ResultadoSimulacion,
    IntentoSimulacion,
)

import json
from django.core.serializers.json import DjangoJSONEncoder



class ResultBuilder:

    def __init__(self, inscripcion, data):

        self.inscripcion = inscripcion
        self.data = data

    @transaction.atomic
    def build(self):

        entrega, _ = Entrega.objects.update_or_create(
            inscripcion=self.inscripcion,
            defaults={
                "tipo_reporte": "SIMULACION",
                "estado": "ENVIADA",
            }
        )

        print("STARTED:", self.data["startedAt"])
        print("TYPE:", type(self.data["startedAt"]))

        print("FINISHED:", self.data["finishedAt"])
        print("TYPE:", type(self.data["finishedAt"]))

        print("CREATED:", self.data["attempts"][0]["createdAt"])
        print("TYPE:", type(self.data["attempts"][0]["createdAt"]))

        resultado, _ = ResultadoSimulacion.objects.update_or_create(
            

        entrega=entrega,

        defaults={

            "run_id": self.data["runId"],

            "completed": self.data["completed"],

            "result_status": self.data["resultStatus"],

            "exit_reason": self.data["exitReason"],

            "best_attempt": self.data["summary"]["bestAttempt"],

            "best_distance": self.data["summary"]["bestDistanceToTarget"],

            "average_distance": self.data["summary"]["averageDistanceToTarget"],

            "successful_attempts": self.data["summary"]["successfulAttempts"],

            "failed_attempts": self.data["summary"]["failedAttempts"],

            "started_at": self.data["startedAt"],

            "finished_at": self.data["finishedAt"],

            "platform": self.data["device"]["platform"],

            "ar_provider": self.data["device"]["arProvider"],

            "unity_version": self.data["device"]["unityVersion"],
            "raw_result": json.loads(
                json.dumps(
                    self.data,
                    cls=DjangoJSONEncoder
                )
            ),

        }

    )

        for intento in self.data["attempts"]:

            IntentoSimulacion.objects.create(

                resultado=resultado,

                numero=intento["attempt"],

                hit=intento["hit"],

                power=intento["power"],

                angle=intento["angle"],

                impact_distance=intento["impactDistanceToTarget"],

                impact_horizontal_distance=intento["impactHorizontalDistance"],

                impact_distance_to_target=intento["impactDistanceToTarget"],

                impact_height=intento["impactHeightDifference"],

                impact_type=intento["impactType"],

                impact_x=intento["impactPoint"]["x"],

                impact_y=intento["impactPoint"]["y"],

                impact_z=intento["impactPoint"]["z"],

                target_x=intento["targetPoint"]["x"],

                target_y=intento["targetPoint"]["y"],

                target_z=intento["targetPoint"]["z"],

                created_at=intento["createdAt"]

            )

        return resultado