from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from identities.models import ContextProfile, Policy

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