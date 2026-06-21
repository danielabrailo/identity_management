from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from identities.models import Policy
from identities.api.serializers.policy import PolicySerializer


class PolicyListCreateAPIView(ListCreateAPIView):
    serializer_class = PolicySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Policy.objects.filter(account=self.request.user)

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)

class PolicyDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PolicySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Policy.objects.filter(account=self.request.user)