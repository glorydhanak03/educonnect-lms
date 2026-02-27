from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Enquiry, Feedback
from django.db.models import Q


def _student_name(request):
    name = (request.user.first_name or request.user.username or "Student")
    if "@" in name:
        name = name.split("@")[0]
    return name.strip().title()


@login_required
def dashboard(request):
    return render(request, "student/dashboard.html", {
        "display_name": _student_name(request)
    })



@login_required
def enquiry(request):

    # -------- SAVE ENQUIRY --------
    if request.method == "POST" and "submit_enquiry" in request.POST:
        Enquiry.objects.create(
            student=request.user,
            student_name=request.POST.get("student_name"),
            student_class=request.POST.get("student_class"),
            send_to=request.POST.get("send_to"),
            receiver_name=request.POST.get("receiver_name"),
            course_name=request.POST.get("course_name"),
            enquiry_type=request.POST.get("enquiry_type"),
            date=request.POST.get("date"),
            time_slot=request.POST.get("time_slot"),
            message=request.POST.get("message"),
        )
        return redirect("student_enquiry")

    # -------- SAVE FEEDBACK --------
    if request.method == "POST" and "submit_feedback" in request.POST:
        enquiry_id = request.POST.get("enquiry_id")
        enquiry_obj = get_object_or_404(
            Enquiry, id=enquiry_id, student=request.user
        )

        attachment = request.FILES.get("attachment")

        if not hasattr(enquiry_obj, "feedback"):
            Feedback.objects.create(
                enquiry=enquiry_obj,
                rating=request.POST.get("rating"),
                comment=request.POST.get("comment"),
                attachment=attachment,   
            )

        return redirect("student_enquiry")

    # -------- FETCH ENQUIRIES --------
    enquiry_list = Enquiry.objects.filter(
    student=request.user
    ).order_by("-created_at")
    
   # -------- SEARCH FILTER (YAHAN ADD KARO) --------
    search_query = request.GET.get("search")
    if search_query:
        enquiry_list = enquiry_list.filter(
            Q(enquiry_type__icontains=search_query) |
            Q(receiver_name__icontains=search_query) |
            Q(course_name__icontains=search_query)
    )   

    # -------- COUNTS (ADD YAHAN) --------
    total_count = enquiry_list.count()
    pending_count = enquiry_list.filter(status="pending").count()
    resolved_count = enquiry_list.filter(status="resolved").count()

    # -------- PAGINATION --------
    paginator = Paginator(enquiry_list, 5)
    page_number = request.GET.get("page")
    enquiries = paginator.get_page(page_number)


    context = {
    "display_name": _student_name(request),
    "enquiries": enquiries,
    "total_count": total_count,
    "pending_count": pending_count,
    "resolved_count": resolved_count,
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
    return render(request, "student/announcement.html", {
        "display_name": _student_name(request)
    })


@login_required
def my_account(request):
    return render(request, "student/my_account.html", {
        "display_name": _student_name(request)
    })
