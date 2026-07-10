from rest_framework import serializers


class MobileUnifiedSubmissionSerializer(serializers.Serializer):

    practice = serializers.JSONField(
        required=False,
        default=dict
    )

    simulation = serializers.JSONField(
        required=False,
        default=dict
    )

    comparison = serializers.JSONField(
        required=False,
        default=dict
    )

    questions = serializers.JSONField(
        required=False,
        default=list
    )

    report = serializers.JSONField(
        required=False,
        default=dict
    )

    device = serializers.JSONField(
        required=False,
        default=dict
    )

    def validate_questions(self, value):

        if not isinstance(value, list):
            raise serializers.ValidationError(
                "questions debe ser una lista."
            )

        return value

    def validate_practice(self, value):

        if value and not isinstance(value, dict):
            raise serializers.ValidationError(
                "practice debe ser un objeto JSON."
            )

        return value

    def validate_simulation(self, value):

        if value and not isinstance(value, dict):
            raise serializers.ValidationError(
                "simulation debe ser un objeto JSON."
            )

        return value

    def validate_comparison(self, value):

        if value and not isinstance(value, dict):
            raise serializers.ValidationError(
                "comparison debe ser un objeto JSON."
            )

        return value

    def validate_report(self, value):

        if value and not isinstance(value, dict):
            raise serializers.ValidationError(
                "report debe ser un objeto JSON."
            )

        return value

    def validate_device(self, value):

        if value and not isinstance(value, dict):
            raise serializers.ValidationError(
                "device debe ser un objeto JSON."
            )

        return value