from django.shortcuts import render

def home(request):
    return render(request, "home.html")
from django.http import HttpResponse
from django.contrib.auth import get_user_model

def create_admin(request):
    User = get_user_model()

    if not User.objects.filter(email="mahidhanak08@gmail.com").exists():
        User.objects.create_superuser(
            username="admin",
            email="mahidhanak08@gmail.com",
            password="mahi2808"
        )
        return HttpResponse("Superuser created!")

    return HttpResponse("User already exists!")