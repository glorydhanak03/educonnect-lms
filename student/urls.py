from django.urls import path
from . import views

urlpatterns = [

    path("dashboard/", views.dashboard, name="student_dashboard"),

    path("my-courses/", views.my_courses, name="student_my_courses"),

    path("explore-courses/", views.explore_courses, name="student_explore_courses"),

    path("live-classes/", views.live_classes, name="student_live_classes"),

    path("assignments/", views.student_assignments, name="student_assignments"),

    path("study-material/", views.study_material, name="student_study_material"),

    path("quiz-exam/", views.quiz_exam, name="student_quiz_exam"),

    path("my-progress/", views.my_progress, name="student_my_progress"),

    path("payments/", views.payments, name="student_payments"),

    path("enquiry/", views.enquiry, name="student_enquiry"),

    path("my-account/", views.my_account, name="student_my_account"),

    path("assignments/<int:id>/submit/", views.submit_assignment, name="submit_assignment"),

]
