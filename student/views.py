from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def _student_name(request):
    name = (request.user.first_name or request.user.username or "Student")
    # if username is email, show part before @
    if "@" in name:
        name = name.split("@")[0]
    return name.strip().title()


@login_required
def dashboard(request):
    return render(request, "student/dashboard.html", {"display_name": _student_name(request)})


@login_required
def my_courses(request):
    return render(request, "student/my_courses.html", {"display_name": _student_name(request)})


@login_required
def explore_courses(request):
    return render(request, "student/explore_courses.html", {"display_name": _student_name(request)})


@login_required
def live_classes(request):
    return render(request, "student/live_classes.html", {"display_name": _student_name(request)})


@login_required
def assignments(request):
    return render(request, "student/assignments.html", {"display_name": _student_name(request)})


@login_required
def study_material(request):
    return render(request, "student/study_material.html", {"display_name": _student_name(request)})


@login_required
def quiz_exam(request):
    return render(request, "student/quiz_exam.html", {"display_name": _student_name(request)})


@login_required
def my_progress(request):
    return render(request, "student/my_progress.html", {"display_name": _student_name(request)})


@login_required
def payments(request):
    return render(request, "student/payments.html", {"display_name": _student_name(request)})


@login_required
def enquiry(request):
    return render(request, "student/enquiry.html", {"display_name": _student_name(request)})

@login_required
def announcement(request):
    return render(request, "student/announcement.html", {"display_name": _student_name(request)})


@login_required
def my_account(request):
    return render(request, "student/my_account.html", {"display_name": _student_name(request)})

