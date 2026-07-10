from rest_framework import serializers

from laboratorios.models import SimulacionAR


class MobileARConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = SimulacionAR

        fields = [
            "id",
            "lab_key",
            "unity_scene_name",
            "display_name",
            "version",
            "enabled",

            "intro_title",
            "intro_text",
            "instructions",

            "max_attempts",
            "allow_resume",
            "requires_camera",

            "formulas",
            "parameters",
            "options",
            "result_schema",
            "evaluation_context",
        ]