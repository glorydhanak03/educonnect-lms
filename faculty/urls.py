from django.urls import path
from . import views

urlpatterns =[

    path("dashboard/", views.dashboard, name="faculty_dashboard"),

    path("my-courses/", views.my_courses, name="faculty_my_courses"),

    path("live-class/", views.live_class, name="faculty_live_class"),

    path("my-notes/", views.my_notes, name="faculty_my_notes"),

    path("quiz-exams/", views.quiz_exams, name="faculty_quiz_exams"),

    path("assignments/", views.assignments, name="faculty_assignments"),

    path("create-assignment/", views.create_assignment, name="faculty_create_assignment"),

    path("assignment/<int:id>/", views.assignment_details, name="faculty_assignment_details"),

    path("assignment/delete/<int:id>/", views.delete_assignment, name="delete_assignment"),

    path("study-material/", views.study_material, name="faculty_study_material"),

    path("announcement/", views.announcement, name="faculty_announcement"),



    path(
        "announcement/edit/<int:ann_id>/",
        views.edit_announcement,
        name="edit_announcement"
    ),

    path(
        "announcement/delete/<int:ann_id>/",
        views.delete_announcement,
        name="delete_announcement"
    ),

    path("students/", views.students, name="faculty_students"),

    path("enquiry/", views.enquiry, name="faculty_enquiry"),

    
    path("submission/<int:id>/grade/", views.grade_submission, name="grade_submission"),



    path(
    "accept-enquiry/<int:enquiry_id>/",
    views.accept_enquiry,
    name="accept_enquiry"
),

path(
    "resolve-enquiry/<int:enquiry_id>/",
    views.resolve_enquiry,
    name="resolve_enquiry"
),

path(
"student-enquiry-status/<int:enquiry_id>/",
views.update_student_enquiry_status,
name="update_student_enquiry_status"
),

path(
"parent-enquiry-status/<int:enquiry_id>/",
views.update_parent_enquiry_status,
name="update_parent_enquiry_status"
),

    path("profile/", views.profile, name="faculty_profile"),
    


]

