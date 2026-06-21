from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from identities.models import ContextProfile, Policy
from identities.api.serializers.identity_evaluation import IdentityEvaluationSerializer


class IdentityEvaluationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = IdentityEvaluationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        target_user_id = serializer.validated_data["target_user_id"]
        context_id = serializer.validated_data["context_id"]
        requester_type_id = serializer.validated_data["requester_type_id"]

        #first find profile
        profile = get_object_or_404(
            ContextProfile,
            account_id=target_user_id,
            context_id=context_id
        )
        #find policy for this account, context and according to requester type
        policy = get_object_or_404(
            Policy,
            account_id=target_user_id,
            context_id=context_id,
            requester_type_id=requester_type_id
        )

        data = {
            "display_name": profile.display_name if policy.can_view_display_name else None,
            "email": profile.email if policy.can_view_email else None,
            "phone": profile.phone if policy.can_view_phone else None,
            "job_title": profile.job_title if policy.can_view_job_title else None,
            "linkedin": profile.linkedin if policy.can_view_linkedin else None,
            "social_media": profile.social_media if policy.can_view_social_media else None,
        }

        return Response(data)