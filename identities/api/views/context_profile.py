from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from identities.models import ContextProfile
from identities.api.serializers.context_profile import ContextProfileSerializer


class ContextProfileListAPIView(ListAPIView):
    serializer_class = ContextProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContextProfile.objects.filter(account=self.request.user)