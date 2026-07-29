from rest_framework import serializers
from identities.models import IdentityRequest

#read
class IdentityRequestSerializer(serializers.ModelSerializer):
    #who is the user requesting the identity
    requester_username = serializers.CharField(
        source="requester.username",
        read_only=True
    )
    #who is target user
    target_username = serializers.CharField(
        source="target_user.username",
        read_only=True
    )
    #what is the context
    context_name = serializers.CharField(
        source="context.name",
        read_only=True
    )
    #requester type assigned
    requester_type_name = serializers.CharField(
        source="requester_type.name",
        read_only=True
    )

    class Meta:
        model = IdentityRequest
        fields = [
            "id",
            "requester_username",
            "target_username",
            "context_name",
            "requester_type_name",
            "reason",
            "status",
            "created_at",
            "decided_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
            "decided_at",
        ]

#create
class IdentityRequestCreateSerializer(serializers.ModelSerializer):
    def validate_target_user(self, value):
        request = self.context["request"]
        #avoid requesting yourself
        if request.user == value:
            raise serializers.ValidationError(
                "You cannot request your own identity"
            )
        return value

    def validate(self, attrs):
        request = self.context["request"]
        #prevent duplicate requests
        exists = IdentityRequest.objects.filter(
            requester=request.user,
            target_user=attrs["target_user"],
            context=attrs["context"],
            status=IdentityRequest.Status.PENDING,
        ).exists()
        if exists:
            raise serializers.ValidationError(
                "A pending request already exists for this user"
            )
        return attrs

    class Meta:
        model = IdentityRequest
        fields = [
            "target_user",
            "context",
            "reason",
        ]

#decision serializer
class IdentityRequestDecisionSerializer(serializers.ModelSerializer):
    #decide the requester type
    class Meta:
        model = IdentityRequest
        fields = [
            "requester_type",
        ]