from rest_framework import serializers


class IdentityEvaluationSerializer(serializers.Serializer):
    context_id = serializers.IntegerField()
    requester_type_id = serializers.IntegerField()