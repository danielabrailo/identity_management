from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from identities.models import ContextProfile
from identities.api.serializers.context_profile import ContextProfileSerializer
from django.shortcuts import get_object_or_404

class ContextProfileListCreateAPIView(ListCreateAPIView):
    serializer_class = ContextProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContextProfile.objects.filter(account=self.request.user)

    def perform_create(self, serializer):
        serializer.save(account=self.request.user) #security enforcement

class ContextProfileDetailAPIView(RetrieveAPIView):
    serializer_class = ContextProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContextProfile.objects.filter(account=self.request.user)