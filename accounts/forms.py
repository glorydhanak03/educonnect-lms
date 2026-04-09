from django import forms
from .models import User
from core.models import GradeClass

class StudentRegisterForm(forms.ModelForm):
    grade_class = forms.ModelChoiceField(
        queryset=GradeClass.objects.filter(is_active=True),
        empty_label="Select Grade/Class",
    )
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username","email","contact_number","password"]