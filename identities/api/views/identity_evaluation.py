from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from identities.models import ContextProfile, Policy
from identities.api.serializers.identity_evaluation import IdentityEvaluationSerializer
from identities.services.policy_evaluator import PolicyEvaluator

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

        filtered_profile = PolicyEvaluator.evaluate(
            profile,
            policy
        )

        return Response(filtered_profile)