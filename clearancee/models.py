from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    year_of_study = models.IntegerField(default=1)

class ClearanceForm(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])
    comments = models.TextField(blank=True, null=True)

class Signature(models.Model):
    clearance_form = models.ForeignKey(ClearanceForm, on_delete=models.CASCADE)
    signed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    signed_at = models.DateTimeField(auto_now_add=True)
    signature = models.CharField(max_length=100)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
