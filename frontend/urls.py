from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from frontend.views import dashboard, context_management, policy_management, disclosure_preview, user_lookup, incoming_requests, home

urlpatterns = [
    path("", home, name="home"),
    path(
        'login/',
        LoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(next_page='login'),
        name='logout'
    ),
    path(
        'dashboard/',
        dashboard,
        name='dashboard'
    ),
    path('contexts/', 
        context_management, 
        name='contexts'
    ),
    path("policies/", 
        policy_management, 
        name="policies"),
    path(
        "disclosure-preview/",
        disclosure_preview,
        name="disclosure-preview"
    ),
    path("user-lookup/", 
        user_lookup, 
        name="user-lookup"
    ),
    path("incoming-requests/", 
        incoming_requests, 
        name="incoming-requests"
    )
]