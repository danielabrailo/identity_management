from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from identities.models import ContextProfile, Policy, IdentityRequest
from identities.api.serializers.identity_evaluation import IdentityEvaluationSerializer
from identities.services.policy_evaluator import PolicyEvaluator

class IdentityEvaluationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = IdentityEvaluationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #get the request
        request_id = serializer.validated_data["request_id"]
        #find the correct reuqest that has been approved
        identity_request = get_object_or_404(
            IdentityRequest,
            id=request_id,
            requester=request.user,
            status=IdentityRequest.Status.APPROVED,
        )
        if identity_request.requester_type is None:
            return Response(
                {"error": "Approved request has no requester type assigned"},
                status=400,
            )
        #get the correct data from the identity request
        target_user_id = identity_request.target_user.id
        context_id = identity_request.context.id
        requester_type_id = identity_request.requester_type.id
        #find profile
        profile = ContextProfile.objects.filter(
            account_id=target_user_id,
            context_id=context_id
        ).first()
        if not profile:
            return Response(
                {"error": "No profile found"},
                status=404
            )
        #find policy for this account, context and according to requester type
        policy = Policy.objects.filter(
            account_id=target_user_id,
            context_id=context_id,
            requester_type_id=requester_type_id
        ).first()
        if not policy:
            return Response(
                {"error": "No policy found"},
                status=404
            )
        #finally get the correct profile data
        filtered_profile = PolicyEvaluator.evaluate(
            profile,
            policy
        )
        return Response(filtered_profile)