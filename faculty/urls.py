from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="faculty_dashboard"),

    path("my-courses/", views.my_courses, name="faculty_my_courses"),
    path("live-class/", views.live_class, name="faculty_live_class"),
    path("my-notes/", views.my_notes, name="faculty_my_notes"),
    path("quiz-exams/", views.quiz_exams, name="faculty_quiz_exams"),
    path("assignments/", views.assignments, name="faculty_assignments"),
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

