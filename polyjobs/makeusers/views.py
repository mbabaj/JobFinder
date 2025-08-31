from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        
        if User.objects.filter(username=username).exists():   
            return render(request, "signup.html", {"error": "Username already taken"})
        elif password != password1:
            return render(request, "signup.html", {"error": "Passwords do not match"})
        else:
            user = User(username=username)
            user.set_password(password)
            user.save()

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('scraper:job_list')
    
    return render(request, "signup.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("scraper:job_list")
        else:
             return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("scraper:job_list")

@login_required
def change_password_view(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        new_password1 = request.POST.get("new_password1")
        user = request.user

        # check current password
        if not user.check_password(current_password):
            return render(request, "change_password.html", {"error": "Current password is incorrect."})

        # check new passwords match
        if new_password != new_password1:
            return render(request, "change_password.html", {"error": "New passwords do not match."})

        # set new password
        user.set_password(new_password1)
        user.save()

        # keep the user logged in after password change
        update_session_auth_hash(request, user)

        return render(request, "change_password_succes.html", {"success": "Password changed successfully!"})

    return render(request, "change_password.html")