from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Context
from .serializers import ContextSerializer


class ContextListAPIView(ListAPIView):
    queryset = Context.objects.all()
    serializer_class = ContextSerializer