from rest_framework import serializers
from identities.models import Policy


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = [
            'id',
            'context',
            'requester_type',
            'can_view_display_name',
            'can_view_email',
            'can_view_phone',
            'can_view_job_title',
            'can_view_linkedin',
            'can_view_social_media',
        ]
        read_only_fields = ['id']

    def validate(self, attrs):
        if 'account' in self.initial_data:
            raise serializers.ValidationError({
                "account": "This field cannot be set manually."
            })
        return attrs