from django import forms
from .models import ClearanceForm, Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
class ClearanceFormForm(forms.ModelForm):
    class Meta:
        model = ClearanceForm
        fields = ['status', 'comments']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['year_of_study']

    def save(self, user=None, commit=True):
        student = super().save(commit=False)
        if user:
            student.user = user
        if commit:
            student.save()
        return student