from rest_framework import serializers
from identities.models import Context


class ContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Context
        fields = ['id', 'name', 'description']