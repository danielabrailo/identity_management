from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from frontend.views import dashboard
from frontend.views import context_management
from frontend.views import policy_management

urlpatterns = [
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
]