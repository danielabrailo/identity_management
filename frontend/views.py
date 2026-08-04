from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from identities.models import ContextProfile, Policy

def home(request):
    #if user is authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect("dashboard")
    #if not, to login screen
    return redirect("login")

@login_required
def dashboard(request):
    profile_count = ContextProfile.objects.filter(
        account=request.user
    ).count()
    policy_count = Policy.objects.filter(
        account=request.user
    ).count()

    profiles = ContextProfile.objects.filter(
        account=request.user
    )
    context_names = [
        profile.context.name
        for profile in profiles
    ]
    context_names = list(set(context_names))

    return render(
        request,
        "dashboard.html",
        {
            "profile_count": profile_count,
            "policy_count": policy_count,
            "contexts": context_names,
        },
    )

@login_required
def context_management(request):
    return render(request, "contexts.html")

@login_required
def policy_management(request):
    return render(request, "policies.html")

@login_required
def disclosure_preview(request):
    return render(
        request,
        "disclosure-preview.html"
    )

@login_required
def user_lookup(request):
    return render(request, "user-lookup.html")

@login_required
def incoming_requests(request):
    return render(request, "incoming_requests.html")