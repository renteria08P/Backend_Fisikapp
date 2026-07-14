from rest_framework import serializers


class ImpactPointSerializer(serializers.Serializer):

    x = serializers.FloatField()

    y = serializers.FloatField()

    z = serializers.FloatField()


class TargetPointSerializer(serializers.Serializer):

    x = serializers.FloatField()

    y = serializers.FloatField()

    z = serializers.FloatField()


class AttemptSerializer(serializers.Serializer):

    attempt = serializers.IntegerField()

    hit = serializers.BooleanField()

    power = serializers.FloatField()

    angle = serializers.FloatField()

    impactDistanceToTarget = serializers.FloatField()

    impactHorizontalDistance = serializers.FloatField()

    impactHeightDifference = serializers.FloatField()

    impactType = serializers.CharField()

    impactPoint = ImpactPointSerializer()

    targetPoint = TargetPointSerializer()

    createdAt = serializers.DateTimeField()


class SummarySerializer(serializers.Serializer):

    bestAttempt = serializers.IntegerField()

    bestDistanceToTarget = serializers.FloatField()

    averageDistanceToTarget = serializers.FloatField()

    successfulAttempts = serializers.IntegerField()

    failedAttempts = serializers.IntegerField()


class DeviceSerializer(serializers.Serializer):

    platform = serializers.CharField()

    arProvider = serializers.CharField()

    unityVersion = serializers.CharField()


class SimulationResultSerializer(serializers.Serializer):

    runId = serializers.CharField()

    completed = serializers.BooleanField()

    resultStatus = serializers.CharField()

    exitReason = serializers.CharField()

    startedAt = serializers.DateTimeField()

    finishedAt = serializers.DateTimeField()

    attempts = AttemptSerializer(
        many=True
    )

    summary = SummarySerializer()

    device = DeviceSerializer()