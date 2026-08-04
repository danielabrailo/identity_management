from django.shortcuts import redirect, render
from accounts.forms import RegisterForm
from django.contrib.auth import login

#REGISTRATION FOR
def register(request):
    #register
    if request.method == "POST":
        form = RegisterForm(request.POST)
        #check for validation
        if form.is_valid():
            user = form.save()
            #automatically login user
            login(request, user)
            #redirect to dashboard
            return redirect("dashboard")
            
    else:
        form = RegisterForm()
    return render(
        request,
        "registration/register.html",
        {
            "form": form
        }
    )