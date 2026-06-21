from rest_framework import serializers
from identities.models import ContextProfile


class ContextProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContextProfile
        fields = [
            'id',
            'context',
            'display_name',
            'email',
            'phone',
            'job_title',
            'linkedin',
            'nickname',
            'social_media',
            'organization',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']