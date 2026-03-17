from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from .models import ParentEnquiry, ParentFeedback
from django.contrib import messages
from admin_panel.models import AdminAnnouncement
from faculty.models import FacultyAnnouncement
from django.utils import timezone
from datetime import timedelta
from admin_panel.models import AdminGuideline
from admin_panel.models import EnquiryAction
from core.models import LiveSession

def _parent_name(request) -> str:
    name = (request.user.first_name or request.user.username or "Parent")
    if "@" in name:
        name = name.split("@")[0]
    return name.strip().title()


@login_required
def dashboard(request):
    return render(request, "parent/dashboard.html", {"display_name": _parent_name(request)})


@login_required
def student_overview(request):
    return render(request, "parent/student_overview.html", {"display_name": _parent_name(request)})


@login_required
def attendance_monitoring(request):
    return render(request, "parent/attendance_monitoring.html", {"display_name": _parent_name(request)})


@login_required
def performance_reports(request):
    return render(request, "parent/performance_reports.html", {"display_name": _parent_name(request)})


@login_required
def fees_payments(request):
    return render(request, "parent/fees_payments.html", {"display_name": _parent_name(request)})


@login_required
def exam_results(request):
    return render(request, "parent/exam_results.html", {"display_name": _parent_name(request)})




@login_required
def announcement(request):

    admin_ann = AdminAnnouncement.objects.filter(
        categories__icontains= "Parents"
    )

    faculty_ann = FacultyAnnouncement.objects.filter(
           post_to__icontains="Parent"
) | FacultyAnnouncement.objects.filter(
    post_to__icontains="Both"
)

    announcements = []

    # Admin announcements
    for ann in admin_ann:

        announcements.append({
            "title": ann.title,
            "message": ann.message,
            "sender": "Admin",
            "created_at": ann.created_at,
            "type": "admin"
        })

    # Faculty announcements
    for ann in faculty_ann:

        announcements.append({
            "title": ann.title,
            "message": ann.announcement,
            "sender": "Faculty",
            "created_at": ann.created_at,
            "type": "faculty"
        })

    # Sort by latest
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
        "parent/announcement.html",
        {
            "announcements": announcements,
            "display_name": _parent_name(request)
        }
    )

@login_required
def enquiry(request):

    # ================= SAVE ENQUIRY =================
    if request.method == "POST" and "submit_enquiry" in request.POST:

        ParentEnquiry.objects.create(
            parent=request.user,
            parent_name=request.POST.get("parent_name"),
            child_name=request.POST.get("child_name"),
            child_class=request.POST.get("child_class"),
            send_to=request.POST.get("send_to"),
            receiver_name=request.POST.get("receiver_name"),
            enquiry_type=request.POST.get("enquiry_type"),
            date=request.POST.get("date"),
            time_slot=request.POST.get("time_slot"),
            message=request.POST.get("message"),
        )

        return redirect("/parent/enquiry/?enquiry=success")
        return redirect("parent_app:enquiry")


    # ================= SAVE FEEDBACK =================
    if request.method == "POST" and "submit_feedback" in request.POST:

        enquiry_id = request.POST.get("enquiry_id")

        enquiry_obj = get_object_or_404(
            ParentEnquiry,
            id=enquiry_id,
            parent=request.user
        )

        if not ParentFeedback.objects.filter(enquiry=enquiry_obj).exists():

            ParentFeedback.objects.create(
                enquiry=enquiry_obj,
                comment=request.POST.get("comment"),
                rating=request.POST.get("rating") or None,
                attachment=request.FILES.get("attachment")
            )
            
            return redirect("/parent/enquiry/?feedback=success")
        else:
            return redirect("/parent/enquiry/?feedback=already")



    # ================= BASE QUERYSET =================
    base_queryset = ParentEnquiry.objects.filter(parent=request.user)

    enquiry_list = base_queryset.order_by("-created_at")

    # ================= SEARCH =================
    search_query = request.GET.get("search")
    if search_query:
        enquiry_list = enquiry_list.filter(
            Q(id__icontains=search_query.replace("PENQ-", "")) |   
            Q(send_to__icontains=search_query) |                  
            Q(child_name__icontains=search_query) |
            Q(receiver_name__icontains=search_query) |
            Q(enquiry_type__icontains=search_query)
        )

    # ================= STATUS FILTER =================
    status_filter = request.GET.get("status")
    if status_filter:
        enquiry_list = enquiry_list.filter(status=status_filter)

    # ================= COUNTS (NO FILTER EFFECT) =================
    total_count = base_queryset.count()
    pending_count = base_queryset.filter(status__in=["pending","in_progress"]).count()
    resolved_count = base_queryset.filter(status__in=["completed","closed"]).count()

    # ================= PAGINATION =================

    paginator = Paginator(enquiry_list, 5)
    page = request.GET.get("page")
    enquiries = paginator.get_page(page)

    guidelines = AdminGuideline.objects.filter(role="parent").order_by("-created_at")

    for e in enquiries:
        action = EnquiryAction.objects.filter(
            enquiry_id=e.id,
            enquiry_type="parent",
            action="approved"
        ).order_by("-created_at").first()
        
        if action:
            e.session = action
            e.meeting_link = action.meeting_link
        else:
            e.session = None
    

    context = {
        "display_name": _parent_name(request),
        "total_count": total_count,
        "pending_count": pending_count,
        "resolved_count": resolved_count,
        "search_query": search_query,
        "status_filter": status_filter,
        "guidelines": guidelines,
        "enquiries": enquiries
    }

    return render(request, "parent/enquiry.html", context)


@login_required
def settings(request):
    return render(request, "parent/settings.html", {"display_name": _parent_name(request)})
