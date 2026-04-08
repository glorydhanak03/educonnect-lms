from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from faculty.models import Assignment
from .models import AssignmentSubmission


@login_required
def dashboard(request):
    return render(request, "student/dashboard.html")


@login_required
def my_courses(request):
    return render(request, "student/my_courses.html")


@login_required
def explore_courses(request):
    return render(request, "student/explore_courses.html")


@login_required
def live_classes(request):
    return render(request, "student/live_classes.html")


# ✅ IMPORTANT FUNCTION (status + submitted_ids)
@login_required
def student_assignments(request):

    assignments = Assignment.objects.all().order_by("-created_at")

    assignments_data = []

    for assignment in assignments:
        submission = AssignmentSubmission.objects.filter(
            assignment=assignment,
            student=request.user
        ).first()

        if not submission:
            status = "pending"
            marks = None
            feedback = None

        elif submission.status == "graded":
            status = "graded"
            marks = submission.marks
            feedback = submission.feedback

        else:
            status = "submitted"
            marks = None
            feedback = None

        assignments_data.append({
            "assignment": assignment,
            "status": status,
            "marks": marks,
            "feedback": feedback,   # ✅ NEW
            "submitted_at": submission.submitted_at if submission else None
        })

    return render(
        request,
        "student/assignments.html",
        {
            "assignments_data": assignments_data
        }
    )


# ✅ FINAL SUBMISSION FUNCTION
@login_required
def submit_assignment(request, id):
    if request.user.role != "STUDENT":
        messages.error(request, "Only students can submit assignments.")
        return redirect("student_assignments")

    assignment = get_object_or_404(Assignment, id=id)

    # ❗ अगर GET request आया
    if request.method != "POST":
        return redirect("student_assignments")

    already_submitted = AssignmentSubmission.objects.filter(
        assignment=assignment,
        student=request.user
    ).exists()

    if already_submitted:
        messages.error(request, "You already submitted this assignment.")
        return redirect("student_assignments")

    file = request.FILES.get("file")
    answers = request.POST.getlist("answers[]")

    print("Answers:", answers)

    answers_text = "\n".join(answers)

    if not file and not any(a.strip() for a in answers):
        messages.error(request, "Please write something.")
        return redirect("student_assignments")

    AssignmentSubmission.objects.create(
        assignment=assignment,
        student=request.user,
        file=file if file else None,
        answers=answers_text
    )

    print("✅ SAVED SUCCESSFULLY")

    messages.success(request, "Assignment submitted successfully")

    return redirect("student_assignments")


@login_required
def study_material(request):
    return render(request, "student/study_material.html")


@login_required
def quiz_exam(request):
    return render(request, "student/quiz_exam.html")


@login_required
def my_progress(request):
    return render(request, "student/my_progress.html")


@login_required
def payments(request):
    return render(request, "student/payments.html")


@login_required
def enquiry(request):
    return render(request, "student/enquiry.html")


@login_required
def my_account(request):
    return render(request, "student/my_account.html")