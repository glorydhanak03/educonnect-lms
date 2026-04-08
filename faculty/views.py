from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from django.http import HttpResponse

from .models import Assignment, AssignmentQuestion
from student.models import AssignmentSubmission


def _faculty_name(request):
    name = (request.user.first_name or request.user.username or "Faculty")
    if "@" in name:
        name = name.split("@")[0]
    return name.strip().title()


@login_required
def dashboard(request):
    return render(request, "faculty/dashboard.html", {
        "display_name": _faculty_name(request)
    })


@login_required
def assignments(request):

    assignments_list = Assignment.objects.filter(
    faculty_id=request.user.id
    ).order_by("-created_at")
    print("USER:", request.user, request.user.id)
    print("COUNT:", assignments_list.count())

    paginator = Paginator(assignments_list, 7)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "faculty/assignments.html",
        {
            "display_name": _faculty_name(request),
            "page_obj": page_obj
        }
    )


@login_required
def create_assignment(request):

    if not request.user.is_authenticated or getattr(request.user, "role", "").lower() != "faculty":
        messages.error(request, "Access denied")
        return redirect("login")

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description", "")

        subject = request.POST.get("subject")
        class_name = request.POST.get("class_name")
        section = request.POST.get("section")

        start_date = request.POST.get("start_date")
        due_date = request.POST.get("due_date")

        total_marks =request.POST.get("total_marks")
        if not total_marks:
            messages.error(request, "Please enter total marks")
            return redirect("faculty_create_assignment")

        try:
            total_marks = int(total_marks)
        except:
            messages.error(request, "Invalid marks")
            return redirect("faculty_create_assignment")
        file = request.FILES.get("question_file")

        assignment = Assignment.objects.create(
            title=title,
            description=description,
            subject=subject,
            class_name=class_name,
            section=section,
            start_date=start_date,
            due_date=due_date,
            total_marks=total_marks,
            faculty=request.user,
            question_file=file
        )

        questions = request.POST.getlist("questions[]")

        for q in questions:
            if q.strip():
                AssignmentQuestion.objects.create(
                    assignment=assignment,
                    question_text=q,
                    question_type=request.POST.get("question_type")
                )

        messages.success(request, "Assignment saved successfully")
        return redirect("faculty_assignments")

    return render(request, "faculty/create_assignment.html")


@login_required
def assignment_details(request, id):

    assignment = get_object_or_404(Assignment, id=id)

   

    submissions = AssignmentSubmission.objects.filter(
        assignment_id=assignment.id
    )

    questions = assignment.questions.all()

    return render(
        request,
        "faculty/assignment_details.html",
        {
            "assignment": assignment,
            "submissions": submissions,
            "questions": questions
        }
    )

@login_required
def delete_assignment(request, id):

    assignment = get_object_or_404(
        Assignment,
        id=id,
        faculty=request.user
    )

    assignment.delete()

    messages.success(request, "Assignment deleted successfully")

    return redirect("faculty_assignments")

@login_required
def grade_submission(request, id):

    submission = get_object_or_404(AssignmentSubmission, id=id)

    if request.method == "POST":

        marks = request.POST.get("marks")
        feedback = request.POST.get("feedback")

        # ✅ Convert marks to integer safely
        if marks:
            submission.marks = int(marks)

        submission.feedback = feedback
        submission.status = "graded"

        submission.save()

        messages.success(request, "Graded successfully")

        return redirect("faculty_assignment_details", id=submission.assignment.id)


@login_required
def study_material(request):
    return render(request, "faculty/study_material.html")


@login_required
def announcement(request):
    return render(request, "faculty/announcement.html")


@login_required
def students(request):
    return render(request, "faculty/students.html")


@login_required
def enquiry(request):
    return render(request, "faculty/enquiry.html")


@login_required
def profile(request):
    return render(request, "faculty/profile.html")
@login_required
def my_courses(request):
    return render(request, "faculty/my_courses.html")


@login_required
def live_class(request):
    return render(request, "faculty/live_class.html")


@login_required
def my_notes(request):
    return render(request, "faculty/my_notes.html")


@login_required
def quiz_exams(request):
    return render(request, "faculty/quiz_exams.html")
