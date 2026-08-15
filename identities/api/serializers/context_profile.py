from rest_framework import serializers
from identities.models import ContextProfile


class ContextProfileSerializer(serializers.ModelSerializer):
    context_name = serializers.CharField(source="context.name", read_only=True)
    def validate(self, attrs):
        user = self.context["request"].user
        # Use the new context if given otherwise keep the current one
        context = attrs.get(
            "context",
            self.instance.context if self.instance else None
        )
        if context:
            queryset = ContextProfile.objects.filter(
                account=user,
                context=context
            )
            #exclude the current object during updates
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError(
                    "A profile already exists for this context."
                )
        return attrs

    class Meta:
        model = ContextProfile
        fields = [
            'id',
            'context',
            'context_name',
            'display_name',
            'email',
            'phone',
            'job_title',
            'linkedin',
            'nickname',
            'social_media',
            'organization',
            'pronouns',
            'location',
            'university',
            'website',
            'bio',
            'preferred_contact_way',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']