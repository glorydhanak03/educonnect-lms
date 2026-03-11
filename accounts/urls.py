from django.urls import path
from . import views
from .views import student_register
from .views import role_login, role_register, user_logout

urlpatterns = [
    path("login/<str:role>/", views.role_login, name="role_login"),
    path("register/<str:role>/", views.role_register, name="role_register"),
    path("logout/", views.user_logout, name="logout"),
    path("student-register/", student_register, name="student_register"),
]
