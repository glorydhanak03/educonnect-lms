from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import StudentRegisterForm
from .models import StudentProfile, User
from core.models import GradeClass
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
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

    if request.method == "POST":
        username = (request.POST.get("email") or "").strip()
        password = request.POST.get("password") or ""

        user = authenticate(request, username=username, password=password)
        if user is None:
            try:
                user = authenticate(request, email=username, password=password)
            except TypeError:
                user = None

        if user is None:
            messages.error(request, "Invalid email or password")
            return render(request, "auth/login.html", {"page_role": role, "mode": "login"})

        # ✅ ROLE LOCK: block wrong role login
        user_role = str(getattr(user, "role", "")).upper()
        if user.is_staff or user.is_superuser or user_role == "ADMIN":
            messages.error(request, "Admin must login from Admin Panel only.")
            return render(request, "auth/login.html", {"page_role": role, "mode": "login"})

        if user_role != expected_role:
            # Example: student tried on faculty login
            nice = expected_role.title()
            actual = user_role.title() if user_role else "Unknown"
            messages.error(request, f"This account is {actual}. Please use {actual.lower()} login page.")
            return render(request, "auth/login.html", {"page_role": role, "mode": "login"})

        login(request, user)
        return redirect(_redirect_after_login(user))

    return render(request, "auth/login.html", {"page_role": role, "mode": "login"})


def role_register(request: HttpRequest, role: str) -> HttpResponse:
    expected_role = _normalize_role(role)
    if expected_role is None:
        return redirect("/")

    grade_classes = None
    if expected_role == "STUDENT":
        grade_classes = GradeClass.objects.filter(is_active=True)

    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        mobile = (request.POST.get("mobile") or "").strip()
        email = (request.POST.get("email") or "").strip().lower()
        password = request.POST.get("password") or ""
        grade_class_id = request.POST.get("grade_class")  # get selected class

        if expected_role == "STUDENT" and not grade_class_id:
            messages.error(request, "Please select a class!")
            return render(request, "auth/register.html", {
                "page_role": role,
                "grade_classes": grade_classes
            })

        if not (username and mobile and email and password):
            messages.error(request, "All fields are required.")
            return render(request, "auth/register.html", {
                "page_role": role,
                "grade_classes": grade_classes
            })

        u = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        if hasattr(u, "mobile"):
            setattr(u, "mobile", mobile)
        if hasattr(u, "role"):
            setattr(u, "role", expected_role)
        u.save()

        if expected_role == "STUDENT":
            StudentProfile.objects.create(user=u, grade_class_id=grade_class_id)

        login(request, u)
        return redirect(_redirect_after_login(u))

    return render(request, "auth/register.html", {
        "page_role": role,
        "grade_classes": grade_classes
    })


@login_required
def user_logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("/")


def student_register(request):
    grade_classes = GradeClass.objects.filter(is_active=True)

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        grade_class_id = request.POST.get("grade_class")

        if not (username and password and grade_class_id):
            messages.error(request, "All fields are required!")
        else:
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                contact_number=mobile,
                role="STUDENT"
            )

            # Create profile
            StudentProfile.objects.create(
                user=user,
                grade_class_id=grade_class_id
            )

            # Send email (important)
            send_welcome_email(email, username)

            login(request, user)

            messages.success(request, f"Welcome {username}, your account has been created!")

            return redirect("role_login", role="student")

    return render(request, "auth/register.html", {
        "page_role": "student",
        "grade_classes": grade_classes
    })


def send_welcome_email(user_email, username):
    print("EMAIL FUNCTION CALLED")
    subject = "Welcome to EduConnect"
    from_email = settings.EMAIL_HOST_USER
    to_email = [user_email]

    html_content = render_to_string(
        "email/welcome_email.html",
        {"username": username}
    )

    text_content = f"Hello {username}, Welcome to EduConnect!"

    email = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        to_email
    )

    email.attach_alternative(html_content, "text/html")

    try:
        email.send()
        print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Email sending failed:", e)