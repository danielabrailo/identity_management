from rest_framework import serializers


class IdentityEvaluationSerializer(serializers.Serializer):
    request_id = serializers.IntegerField()