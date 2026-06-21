from rest_framework import serializers


class IdentityEvaluationSerializer(serializers.Serializer):
    target_user_id = serializers.IntegerField()
    context_id = serializers.IntegerField()
    requester_type_id = serializers.IntegerField()