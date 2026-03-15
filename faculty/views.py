from student.models import Enquiry
from parent.models import ParentEnquiry
from django.db.models import Q
from itertools import chain
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import FacultyAnnouncement
from admin_panel.models import AdminAnnouncement
from django.utils import timezone
from datetime import timedelta
from admin_panel.models import AdminGuideline
from admin_panel.models import EnquiryAction

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
    # === Existing POST logic for faculty announcement ===
    if request.method == "POST":
        title = request.POST.get("title")
        std_class = request.POST.get("std_class", "")
        subject = request.POST.get("subject", "")
        post_to = request.POST.get("post_to")
        announcement_text = request.POST.get("announcement")

        FacultyAnnouncement.objects.create(
            faculty=request.user,
            title=title,
            std_class=std_class,
            subject=subject,
            post_to=post_to,
            announcement=announcement_text
        )
        return redirect('/faculty/announcement/?status=posted')

    # === Existing GET logic for faculty announcements ===
    announcements = FacultyAnnouncement.objects.filter(faculty=request.user)

    search_query = request.GET.get("search", "").strip()
    filter_class = request.GET.get("class", "")
    filter_subject = request.GET.get("subject", "")
    filter_post_to = request.GET.get("post_to", "")

    if search_query:
        announcements = announcements.filter(title__icontains=search_query)
    if filter_class:
        announcements = announcements.filter(std_class=filter_class)
    if filter_subject:
        announcements = announcements.filter(subject=filter_subject)
    if filter_post_to:
        announcements = announcements.filter(post_to=filter_post_to)

    announcements = announcements.order_by('-created_at')

    # === NEW: Fetch Admin Announcements for Faculty ===
    admin_announcements = AdminAnnouncement.objects.filter(
        categories__contains=["Faculty"]
    ).order_by('-created_at')

    # Set display name for each admin announcement
    for ann in admin_announcements:
        ann.display_name = ann.sender.first_name or "Admin"
        ann.is_new = ann.created_at >= timezone.now() - timedelta(days=3)


    return render(request, "faculty/announcement.html", {
        "display_name": _faculty_name(request),
        "announcements": announcements,
        "admin_announcements": admin_announcements,  # pass to template
        "search_query": search_query,
        "filter_class": filter_class,
        "filter_subject": filter_subject,
        "filter_post_to": filter_post_to
    })

@login_required
def edit_announcement(request, ann_id):

    announcement = get_object_or_404(
        FacultyAnnouncement,
        id=ann_id,
        faculty=request.user
    )

    if request.method == "POST":

        announcement.title = request.POST.get("title")
        announcement.std_class = request.POST.get("std_class")
        announcement.subject = request.POST.get("subject")
        announcement.post_to = request.POST.get("post_to")
        announcement.announcement = request.POST.get("announcement")

        announcement.save()

        return redirect('/faculty/announcement/?status=updated')

    return redirect('/faculty/announcement/')

@login_required
def delete_announcement(request, ann_id):

    announcement = get_object_or_404(
        FacultyAnnouncement,
        id=ann_id,
        faculty=request.user
    )

    announcement.delete()

    return redirect('/faculty/announcement/?status=deleted')

@login_required
def students(request):
    return render(request, "faculty/students.html", {"display_name": _faculty_name(request)})



@login_required
def enquiry(request):
    search = request.GET.get("search", "")
    date = request.GET.get("date", "")

    # ================= STUDENT ENQUIRIES =================
    student_enquiries = Enquiry.objects.filter(send_to="faculty")
    if search:
        if search.isdigit():
            student_enquiries = student_enquiries.filter(
                Q(student_name__icontains=search) |
                Q(id=int(search))
            )
        else:
            student_enquiries = student_enquiries.filter(
                student_name__icontains=search
            )

    if date:
        student_enquiries = student_enquiries.filter(date=date)

    student_enquiries = student_enquiries.order_by("-id")
    student_paginator = Paginator(student_enquiries, 10)
    student_page = request.GET.get("student_page")
    student_page_obj = student_paginator.get_page(student_page)

    # ================= PARENT ENQUIRIES =================
    parent_enquiries = ParentEnquiry.objects.filter(send_to="faculty")
    if search:
        if search.isdigit():
            parent_enquiries = parent_enquiries.filter(
                Q(parent_name__icontains=search) |
                Q(child_name__icontains=search) |
                Q(id=int(search))
            )
        else:
            parent_enquiries = parent_enquiries.filter(
                Q(parent_name__icontains=search) |
                Q(child_name__icontains=search)
            )

    if date:
        parent_enquiries = parent_enquiries.filter(date=date)

    parent_enquiries = parent_enquiries.order_by("-id")
    parent_paginator = Paginator(parent_enquiries, 10)
    parent_page = request.GET.get("parent_page")
    parent_page_obj = parent_paginator.get_page(parent_page)  

    # ===== ATTACH SESSION FOR STUDENT ENQUIRIES =====
    for enquiry in student_page_obj:
        action = EnquiryAction.objects.filter(
           enquiry_id=enquiry.id,
           enquiry_type="student",
           action="approved",
        ).order_by("-created_at").first()

        enquiry.session = action


    # ===== ATTACH SESSION FOR PARENT ENQUIRIES =====
    for enquiry in parent_page_obj:
        action = EnquiryAction.objects.filter(
          enquiry_id=enquiry.id,
          enquiry_type="parent",
          action="approved",
        ).order_by("-created_at").first()

        enquiry.session = action

    guidelines = AdminGuideline.objects.filter(role="faculty").order_by("-created_at")

    context = {
        "display_name": _faculty_name(request),
        "student_enquiries": student_page_obj,
        "parent_enquiries": parent_page_obj,
        "search": search,
        "date": date,
        "guidelines": guidelines,
    }

    return render(request, "faculty/enquiry.html", context)

@login_required
def accept_enquiry(request, enquiry_id):

    enquiry = get_object_or_404(Enquiry, id=enquiry_id)

    enquiry.status = "in_progress"
    enquiry.save()

    return redirect("faculty_app:enquiry")


@login_required
def resolve_enquiry(request, enquiry_id):

    enquiry = get_object_or_404(Enquiry, id=enquiry_id)

    enquiry.status = "completed"
    enquiry.save()

    return redirect("faculty_app:enquiry")

def update_student_enquiry_status(request, enquiry_id):

    enquiry = get_object_or_404(Enquiry, id=enquiry_id)

    status = request.POST.get("status")
    meeting_link = request.POST.get("meeting_link")


    if status:
        enquiry.status = status
        enquiry.save()

        if status == "approved":

            EnquiryAction.objects.create(
                enquiry_id=enquiry.id,
                enquiry_type="student",
                action="approved",
                meeting_link=meeting_link
            )

    return redirect("faculty_enquiry")


def update_parent_enquiry_status(request, enquiry_id):

    enquiry = get_object_or_404(ParentEnquiry, id=enquiry_id)

    status = request.POST.get("status")
    meeting_link = request.POST.get("meeting_link")


    if status:
        enquiry.status = status
        enquiry.save()

        if status == "approved":

            EnquiryAction.objects.create(
                enquiry_id=enquiry.id,
                enquiry_type="parent",  
                action="approved",
                meeting_link= meeting_link
            )

    return redirect("faculty_enquiry")

@login_required
def complete_session(request, id, type):

    if type == "student":
        enquiry = Enquiry.objects.get(id=id)
    else:
        enquiry = ParentEnquiry.objects.get(id=id)

    enquiry.status = "completed"
    enquiry.save()

    EnquiryAction.objects.create(
        enquiry_id=id,
        enquiry_type=type,
        action="completed"
    )

    return redirect("faculty_enquiry")


@login_required
def profile(request):
    return render(request, "faculty/profile.html", {"display_name": _faculty_name(request)})

