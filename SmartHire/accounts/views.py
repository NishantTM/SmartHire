from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        # Basic validation
        if not username or not email or not password:
            messages.error(request, "Please fill in all required fields.")
            return render(request, "accounts/register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "accounts/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "accounts/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "accounts/register.html")

        if role not in [
            User.Role.JOB_SEEKER,
            User.Role.RECRUITER,
        ]:
            messages.error(request, "Please select a valid role.")
            return render(request, "accounts/register.html")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone,
            role=role,
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


@login_required
def dashboard_view(request):
    if request.user.role == User.Role.RECRUITER:
        return render(request, "accounts/recruiter_dashboard.html")

    if request.user.role == User.Role.ADMIN:
        return render(request, "accounts/admin_dashboard.html")

    return render(request, "accounts/job_seeker_dashboard.html")


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")