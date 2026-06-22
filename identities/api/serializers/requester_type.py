from rest_framework import serializers
from identities.models import RequesterType

class RequesterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequesterType
        fields = ["id", "name", "description"]