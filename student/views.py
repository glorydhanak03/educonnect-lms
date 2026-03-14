from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Enquiry, Feedback
from django.db.models import Q
from admin_panel.models import AdminAnnouncement
from faculty.models import FacultyAnnouncement
from django.utils import timezone
from datetime import timedelta
from admin_panel.models import AdminGuideline
from accounts.models import StudentProfile
from admin_panel.models import EnquiryAction


def _student_name(request):
    name = (request.user.first_name or request.user.username or "Student")
    if "@" in name:
        name = name.split(
            "@")[0]
    return name.strip().title()


@login_required
def dashboard(request):
    return render(request, "student/dashboard.html", {
        "display_name": _student_name(request)
    })


@login_required
def enquiry(request):

    # ================= SAVE ENQUIRY =================
    if request.method == "POST" and "submit_enquiry" in request.POST:

        student_class = request.POST.get("student_class")
        send_to = request.POST.get("send_to")
        receiver_name = request.POST.get("receiver_name")
        course_name = request.POST.get("course_name") or "Not Specified"
        enquiry_type = request.POST.get("enquiry_type")
        date = request.POST.get("date")
        time_slot = request.POST.get("time_slot")
        message = request.POST.get("message")

        if not date or not time_slot:
            return redirect("/student/enquiry/?error=date_time_required")

        if not student_class or not send_to or not enquiry_type or not message:
            return redirect("/student/enquiry/?error=missing_fields")

        Enquiry.objects.create(
            student=request.user,
            student_name=_student_name(request),
            student_class=student_class,
            send_to=send_to,
            receiver_name=receiver_name,
            course_name=course_name,
            enquiry_type=enquiry_type,
            date=date,
            time_slot=time_slot,
            message=message,
        )

        return redirect("/student/enquiry/?enquiry=success")


    # ================= SAVE FEEDBACK =================
    if request.method == "POST" and "submit_feedback" in request.POST:

        enquiry_id = request.POST.get("enquiry_id")

        enquiry_obj = get_object_or_404(
            Enquiry,
            id=enquiry_id,
            student=request.user
        )

        if enquiry_obj.status.lower() not in ["completed", "closed"]:
            return redirect("/student/enquiry/?error=not_allowed")

        if hasattr(enquiry_obj, "feedback"):
            return redirect("/student/enquiry/?feedback=already")

        rating_value = request.POST.get("rating")
        rating_value = int(rating_value) if rating_value else None

        Feedback.objects.create(
            enquiry=enquiry_obj,
            rating=rating_value,
            comment=request.POST.get("comment"),
            attachment=request.FILES.get("attachment")
        )

        return redirect("/student/enquiry/?feedback=success")


    # ================= BASE QUERYSET =================
    enquiry_list = Enquiry.objects.filter(
        student=request.user
    ).order_by("-created_at")

    total_count = enquiry_list.count()

    pending_count = enquiry_list.filter(
           status__in=["pending", "in_progress", "approved", "rescheduled"]
    ).count()

    resolved_count = enquiry_list.filter(
       status__in=["completed", "rejected", "cancelled"]
    ).count()


    # ================= FILTER =================
    search_query = request.GET.get("search", "")
    status_filter = request.GET.get("status", "")

    if search_query:
        enquiry_list = enquiry_list.filter(
            Q(enquiry_type__icontains=search_query) |
            Q(receiver_name__icontains=search_query) |
            Q(course_name__icontains=search_query)
        )

    if status_filter:
        enquiry_list = enquiry_list.filter(status=status_filter)


    # ================= SESSION + FEEDBACK CHECK =================
    feedback_ids = set(
    Feedback.objects.filter(
        enquiry__student=request.user
    ).values_list("enquiry_id", flat=True)
    )

    for e in enquiry_list:
        action = EnquiryAction.objects.filter(
           enquiry_id=e.id,
           enquiry_type="student",
           action="approved",
        ).order_by("-created_at").first()

        if action:
            e.session_date = action.session_date
            e.session_time = action.session_time
            e.action_status = action.action
            e.meeting_link = action.meeting_link
            e.session = action

        else:
            e.session_date = None
            e.session_time = None
            e.action_status = None
            e.meeting_link = None
            e.session = None

        
    # ================= PAGINATION =================
    paginator = Paginator(enquiry_list, 5)
    page_number = request.GET.get("page")
    enquiries = paginator.get_page(page_number)


    for e in enquiries:
        e.feedback_exists = e.id in feedback_ids


    # ================= GUIDELINES =================
    guidelines = AdminGuideline.objects.filter(
        role="student"
    ).order_by("-created_at")


    context = {
        "display_name": _student_name(request),
        "enquiries": enquiries,
        "total_count": total_count,
        "pending_count": pending_count,
        "resolved_count": resolved_count,
        "search_query": search_query,
        "status_filter": status_filter,
        "guidelines": guidelines,
    }

    return render(request, "student/enquiry.html", context)

# ================= Other Pages =================

@login_required
def my_courses(request):
    return render(request, "student/my_courses.html", {
        "display_name": _student_name(request)
    })


@login_required
def explore_courses(request):
    return render(request, "student/explore_courses.html", {
        "display_name": _student_name(request)
    })


@login_required
def live_classes(request):
    return render(request, "student/live_classes.html", {
        "display_name": _student_name(request)
    })


@login_required
def assignments(request):
    return render(request, "student/assignments.html", {
        "display_name": _student_name(request)
    })


@login_required
def study_material(request):
    return render(request, "student/study_material.html", {
        "display_name": _student_name(request)
    })


@login_required
def quiz_exam(request):
    return render(request, "student/quiz_exam.html", {
        "display_name": _student_name(request)
    })


@login_required
def my_progress(request):
    return render(request, "student/my_progress.html", {
        "display_name": _student_name(request)
    })


@login_required
def payments(request):
    return render(request, "student/payments.html", {
        "display_name": _student_name(request)
    })

@login_required
def announcement(request):

    # Admin announcements for Students
    admin_ann = AdminAnnouncement.objects.filter(
        categories__icontains="Student"
    )

    # Faculty announcements for Students
    faculty_ann = FacultyAnnouncement.objects.filter(
        post_to__icontains="Student"
    ) | FacultyAnnouncement.objects.filter(
        post_to__icontains="Both"
    )

    announcements = []

    # Admin
    for ann in admin_ann:
        announcements.append({
            "title": ann.title,
            "message": ann.message,
            "sender": "Admin",
            "created_at": ann.created_at,
            "type": "admin"
        })

    # Faculty
    for ann in faculty_ann:
        announcements.append({
            "title": ann.title,
            "message": ann.announcement,
            "sender":"Faculty",
            "created_at": ann.created_at,
            "type": "faculty"
        })

    # latest first
    announcements = sorted(
        announcements,
        key=lambda x: x["created_at"],
        reverse=True
    )

    # NEW badge logic
    for ann in announcements:
        ann["is_new"] = timezone.now() - ann["created_at"] < timedelta(days=2)

    return render(
        request,
        "student/announcement.html",
        {
            "announcements": announcements,
            "display_name": _student_name(request)
        }
    )


@login_required
def my_account(request):
    return render(request, "student/my_account.html", {
        "display_name": _student_name(request)
    })


@login_required
def student_announcements(request):
    student_profile = StudentProfile.objects.get(user=request.user)
    batch = student_profile.batch

    announcements = FacultyAnnouncement.objects.filter(batch=batch).order_by('-created_at')
    return render(request, "student/announcement.html", {"announcements": announcements})