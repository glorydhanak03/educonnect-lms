from student.models import Enquiry
from parent.models import ParentEnquiry
from django.db.models import Q
from itertools import chain
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.db.models import Q


def _faculty_name(request):
    name = (request.user.first_name or request.user.username or "Faculty")
    if "@" in name:
        name = name.split("@")[0]
    return name.strip().title()


@login_required
def dashboard(request):
    return render(request, "faculty/dashboard.html", {"display_name": _faculty_name(request)})


@login_required
def my_courses(request):
    return render(request, "faculty/my_courses.html", {"display_name": _faculty_name(request)})


@login_required
def live_class(request):
    return render(request, "faculty/live_class.html", {"display_name": _faculty_name(request)})


@login_required
def my_notes(request):
    return render(request, "faculty/my_notes.html", {"display_name": _faculty_name(request)})


@login_required
def quiz_exams(request):
    return render(request, "faculty/quiz_exams.html", {"display_name": _faculty_name(request)})


@login_required
def assignments(request):
    return render(request, "faculty/assignments.html", {"display_name": _faculty_name(request)})


@login_required
def study_material(request):
    return render(request, "faculty/study_material.html", {"display_name": _faculty_name(request)})


@login_required
def announcement(request):
    return render(request, "faculty/announcement.html", {"display_name": _faculty_name(request)})


@login_required
def students(request):
    return render(request, "faculty/students.html", {"display_name": _faculty_name(request)})


@login_required
def enquiry(request):

    search = request.GET.get("search")
    date = request.GET.get("date")

    # ================= STUDENT ENQUIRIES =================

    student_enquiries = Enquiry.objects.filter(send_to="faculty")

    if search:
        student_enquiries = student_enquiries.filter(
            Q(student_name__icontains=search) |
            Q(id__icontains=search)
        )

    if date:
        student_enquiries = student_enquiries.filter(date=date)

    student_paginator = Paginator(student_enquiries, 10)
    student_page = request.GET.get("student_page")
    student_page_obj = student_paginator.get_page(student_page)


    # ================= PARENT ENQUIRIES =================

    parent_enquiries = ParentEnquiry.objects.filter(send_to="faculty")

    if search:
        parent_enquiries = parent_enquiries.filter(
            Q(parent_name__icontains=search) |
            Q(child_name__icontains=search) |
            Q(id__icontains=search)
        )

    if date:
        parent_enquiries = parent_enquiries.filter(date=date)

    parent_paginator = Paginator(parent_enquiries, 10)
    parent_page = request.GET.get("parent_page")
    parent_page_obj = parent_paginator.get_page(parent_page)


    context = {
        "display_name": _faculty_name(request),
        "student_enquiries": student_page_obj,
        "parent_enquiries": parent_page_obj,
    }

    return render(request, "faculty/enquiry.html", context)


@login_required
def update_student_enquiry_status(request, enquiry_id):

    enquiry = get_object_or_404(Enquiry, id=enquiry_id)

    status = request.POST.get("status")

    if status:
        enquiry.status = status
        enquiry.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def update_parent_enquiry_status(request, enquiry_id):

    enquiry = get_object_or_404(ParentEnquiry, id=enquiry_id)

    status = request.POST.get("status")

    if status:
        enquiry.status = status
        enquiry.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




@login_required
def profile(request):
    return render(request, "faculty/profile.html", {"display_name": _faculty_name(request)})

