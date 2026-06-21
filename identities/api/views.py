from django.shortcuts import render
from rest_framework.generics import ListAPIView
from identities.models import Context
from .serializers import ContextSerializer
from rest_framework.permissions import IsAuthenticated


class ContextListAPIView(ListAPIView):
    queryset = Context.objects.all()
    serializer_class = ContextSerializer
    permission_classes = [IsAuthenticated]