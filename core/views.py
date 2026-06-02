from django.http import HttpResponse
from django.contrib.auth import get_user_model

def create_admin(request):
    User = get_user_model()

    user, created = User.objects.get_or_create(
        email="mahidhanak08@gmail.com",
        defaults={
            "username": "admin"
        }
    )

    user.is_staff = True
    user.is_superuser = True
    user.set_password("mahi2808")
    user.save()

    return HttpResponse("Admin fixed successfully!")