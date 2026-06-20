from django.urls import path
from .views import ContextListAPIView

urlpatterns = [
    path('contexts/', ContextListAPIView.as_view(), name='context-list'),
]