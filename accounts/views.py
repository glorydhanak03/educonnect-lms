from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

ROLE_MAP = {
    "student": "STUDENT",
    "faculty": "FACULTY",
    "parent": "PARENT",
}

def _normalize_role(url_role: str) -> str | None:
    if not url_role:
        return None
    return ROLE_MAP.get(url_role.strip().lower())

def _redirect_after_login(user) -> str:
    role = str(getattr(user, "role", "")).upper()

    # Admin should not use this flow
    if user.is_staff or user.is_superuser or role == "ADMIN":
        return "/admin/"

    if role == "STUDENT":
        return "/student/dashboard/"
    if role == "FACULTY":
        return "/faculty/dashboard/"
    if role == "PARENT":
        return "/parent/dashboard/"
    return "/"

def role_login(request: HttpRequest, role: str) -> HttpResponse:
    expected_role = _normalize_role(role)

    if expected_role is None:
        return redirect("/")

    # 👉 GET request
    if request.method != "POST":
        return render(request, "auth/login.html", {"page_role": role, "mode": "login"})

    # 👉 POST request
    email = (request.POST.get("email") or "").strip()
    password = request.POST.get("password") or ""

    user_obj = User.objects.filter(email=email).first()

    if user_obj:
        user = authenticate(request, username=user_obj.username, password=password)
    else:
        user = None

    if user is None:
        messages.error(request, "Invalid email or password")
        return render(request, "auth/login.html", {"page_role": role, "mode": "login"})

    # ✅ ROLE CHECK
    user_role = str(getattr(user, "role", "")).upper()

    if user.is_staff or user.is_superuser or user_role == "ADMIN":
        messages.error(request, "Admin must login from Admin Panel only.")
        return render(request, "auth/login.html", {"page_role": role, "mode": "login"})

    if user_role != expected_role:
        actual = user_role.title() if user_role else "Unknown"
        messages.error(request, f"This account is {actual}. Please use correct login page.")
        return render(request, "auth/login.html", {"page_role": role, "mode": "login"})

    # ✅ SESSION FIX (IMPORTANT)
    if request.user.is_authenticated:
        logout(request)

    request.session.flush()

    login(request, user)

    request.session.cycle_key()

    return redirect(_redirect_after_login(user))
           
        

    return render(request, "auth/login.html", {"page_role": role, "mode": "login"})


def role_register(request: HttpRequest, role: str) -> HttpResponse:
    expected_role = _normalize_role(role)
    if expected_role is None:
        return redirect("/")

    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        mobile = (request.POST.get("mobile") or "").strip()
        email = (request.POST.get("email") or "").strip().lower()
        password = request.POST.get("password") or ""

        if not (username and mobile and email and password):
            messages.error(request, "All fields are required.")
            return render(request, "auth/register.html", {"page_role": role, "mode": "register"})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please login.")
            return redirect(reverse("role_login", args=[role]))

        # Create user
        u = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        # optional fields if exist
        if hasattr(u, "mobile"):
            setattr(u, "mobile", mobile)
        if hasattr(u, "role"):
            setattr(u, "role", expected_role)
        u.save()

        login(request, u)
        return redirect(_redirect_after_login(u))

    return render(request, "auth/register.html", {"page_role": role, "mode": "register"})


@login_required
def user_logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("/")
