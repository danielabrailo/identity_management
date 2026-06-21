from django.urls import path
from identities.api.views import ContextListAPIView

urlpatterns = [
    path('contexts/', ContextListAPIView.as_view(), name='context-list'),
]