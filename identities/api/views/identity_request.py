from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from identities.models import IdentityRequest
from identities.api.serializers.identity_request import (
    IdentityRequestDecisionSerializer,
    IdentityRequestSerializer,
    IdentityRequestCreateSerializer,
)

class IdentityRequestListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    #return received requests
    def get_queryset(self):
        return IdentityRequest.objects.filter(
            target_user=self.request.user
        )
    #get serializaer according to HTTP methos
    def get_serializer_class(self):
        #POST
        if self.request.method == "POST":
            return IdentityRequestCreateSerializer
        #GET
        return IdentityRequestSerializer
    #save requester
    def perform_create(self, serializer):
        serializer.save(
            requester=self.request.user
        )

class IdentityRequestApproveAPIView(APIView):
    permission_classes = [IsAuthenticated]
    #patch
    def patch(self, request, pk):
        #get the identity request
        identity_request = get_object_or_404(
            IdentityRequest,
            pk=pk,
            #permissions check
            target_user=request.user,
        )
        #check the status to avoid duplicating them
        if identity_request.status != IdentityRequest.Status.PENDING:
            return Response(
                {"error": "This request has already been decided."},
                status=400,
            )
        #validate request
        serializer = IdentityRequestDecisionSerializer(
            identity_request,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        #update request
        identity_request.requester_type = serializer.validated_data["requester_type"]
        identity_request.status = IdentityRequest.Status.APPROVED
        identity_request.decided_at = timezone.now()
        identity_request.save()
        #return updated response with 200 OK
        return Response(IdentityRequestSerializer(identity_request).data, status=status.HTTP_200_OK)