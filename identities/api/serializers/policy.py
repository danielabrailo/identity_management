from rest_framework import serializers
from identities.models import Policy


class PolicySerializer(serializers.ModelSerializer):
    context_name = serializers.CharField(source="context.name", read_only=True)
    requester_type_name = serializers.CharField(source="requester_type.name", read_only=True)

    class Meta:
        model = Policy
        fields = [
            'id',
            'context',
            'context_name',
            'requester_type',
            'requester_type_name',
            'can_view_display_name',
            'can_view_email',
            'can_view_phone',
            'can_view_job_title',
            'can_view_linkedin',
            'can_view_social_media',
            'can_view_nickname',
            'can_view_organization'
        ]
        read_only_fields = ['id']

    def validate(self, attrs):
        if 'account' in self.initial_data:
            raise serializers.ValidationError({
                "account": "This field cannot be set manually."
            })
        return attrs