from django.urls import path
from .views import home
from .views import create_admin 
urlpatterns = [
    path("", home, name="home"),
    path("create-admin/", create_admin, name="create_admin"),
]
