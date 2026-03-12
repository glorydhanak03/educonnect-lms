from django.urls import path
from . import views

app_name = "admin_panel"

urlpatterns = [
    path("", views.admin_login, name="admin_login"),
    path("logout/", views.admin_logout, name="admin_logout"),

    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # USERS
    path("users/students/", views.manage_students, name="admin_manage_students"),
    path("users/faculty/", views.manage_faculty, name="admin_manage_faculty"),
    path("users/parents/", views.manage_parents, name="admin_manage_parents"),

    # PAYMENTS
    path("payments/history/", views.payment_history, name="admin_payment_history"),
    path("payments/fee-packages/", views.fee_packages, name="admin_fee_packages"),
    path("payments/refund-requests/", views.refund_requests, name="admin_refund_request"),

    # OTHERS
    path("courses/", views.manage_courses, name="admin_manage_courses"),\
    path("assign-batch/", views.assign_batch, name="assign_batch"),
    path("analytics/", views.analytics_report, name="admin_analytics_report"),
    path("announcement/", views.announcement, name="admin_announcement"),
    path(
        "announcement/create/",
         views.create_announcement,
         name="create_announcement"
        ),
 
    path(
        "announcement/update/<int:id>/",
         views.update_announcement,
         name="update_admin_announcement"
        ),

    path(
        "announcement/delete/<int:id>/",
        views.delete_announcement,
        name="delete_admin_announcement"
        ),
    path("enquiry/", views.enquiry, name="admin_enquiry"),
    path("update-enquiry-status/", views.update_enquiry_status, name="update_enquiry_status"),
    path("approve-enquiry/<int:id>/<str:type>/",views.approve_enquiry,name="approve_enquiry"),
    path("reject-enquiry/<int:id>/<str:type>/",views.reject_enquiry,name="reject_enquiry"),

path("add-guideline/", views.add_guideline, name="add_guideline"),
path("delete-guideline/<int:id>/", views.delete_guideline, name="delete_guideline"),
path("update-guideline/<int:id>/", views.update_guideline, name="update_guideline"),
    path("settings/", views.settings, name="admin_settings"),
]
