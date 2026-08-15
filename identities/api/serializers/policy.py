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
            'can_view_organization',
            'can_view_pronouns',
            'can_view_location',
            'can_view_university',
            'can_view_website',
            'can_view_bio',
            'can_view_preferred_contact_way'
        ]
        read_only_fields = ['id']

    def validate(self, attrs):
        #account validation
        if 'account' in self.initial_data:
            raise serializers.ValidationError({
                "account": "This field cannot be set manually."
            })
        #uniqueness constriant validation
        user = self.context["request"].user
        #get context
        context = attrs.get(
            "context",
            self.instance.context if self.instance else None
        )
        #get requester type
        requester_type = attrs.get(
            "requester_type",
            self.instance.requester_type if self.instance else None
        )
        if context and requester_type:
            queryset = Policy.objects.filter(
                account=user,
                context=context,
                requester_type=requester_type
            )
            #exclude current object during updates
            if self.instance:
                queryset = queryset.exclude(
                    pk=self.instance.pk
                )
            #if it already exists
            if queryset.exists():
                raise serializers.ValidationError(
                    "A policy already exists for this context and requester type."
                )
        return attrs