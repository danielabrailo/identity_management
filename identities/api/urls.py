from django.urls import path
from identities.api.views.context import ContextListAPIView
from identities.api.views.context_profile import ContextProfileListCreateAPIView

urlpatterns = [
    path('contexts/', ContextListAPIView.as_view(), name='context-list'),
    path('context-profiles/', ContextProfileListCreateAPIView.as_view(), name='context-profile-list-create'),
]