from rest_framework.generics import ListAPIView
from identities.models import RequesterType
from identities.api.serializers.requester_type import RequesterTypeSerializer

class RequesterTypeListAPIView(ListAPIView):
    queryset = RequesterType.objects.all()
    serializer_class = RequesterTypeSerializer