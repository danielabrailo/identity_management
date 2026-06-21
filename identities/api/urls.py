from django.urls import path
from identities.api.views.context import ContextListAPIView
from identities.api.views.context_profile import (
    ContextProfileListCreateAPIView,
    ContextProfileDetailAPIView,
)
from identities.api.views.policy import (
    PolicyListCreateAPIView,
    PolicyDetailAPIView
)
from identities.api.views.identity_evaluation import IdentityEvaluationAPIView

urlpatterns = [
    path('contexts/', ContextListAPIView.as_view(), name='context-list'),
    path('context-profiles/', ContextProfileListCreateAPIView.as_view(), name='context-profile-list-create'),
    path('context-profiles/<int:pk>/', ContextProfileDetailAPIView.as_view(), name='context-profile-detail'),
    path('policies/', PolicyListCreateAPIView.as_view(), name='policy-list-create'),
    path('policies/<int:pk>/', PolicyDetailAPIView.as_view(), name='policy-detail'),
    path('context-profiles/evaluate/', IdentityEvaluationAPIView.as_view()),
]