from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import ClearanceForm, Signature, Notification, Student
from .forms import ClearanceFormForm
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration
            return redirect('index')  # Redirect to the homepage or any other page
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
@login_required
def generate_clearance_form(request):
    if request.method == 'POST':
        form = ClearanceFormForm(request.POST)
        if form.is_valid():
            clearance_form = form.save(commit=False)
            clearance_form.student = request.user.student
            clearance_form.save()
            # Notify admins
            notify_admins(clearance_form)
            return redirect('clearance_status')
    else:
        form = ClearanceFormForm()
    return render(request, 'clearance/generate_form.html', {'form': form})

@login_required
def clearance_status(request):
    clearance_forms = ClearanceForm.objects.filter(student=request.user.student)
    return render(request, 'clearance/status.html', {'clearance_forms': clearance_forms})
@login_required
def clearance_status(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        # Handle the case where the student instance does not exist
        return render(request, 'error.html', {'message': 'Student profile not found. Please contact administration.'})

    # Proceed with the logic if the student instance exists
    # Example:
    clearance_forms = ClearanceForm.objects.filter(student=student)
    return render(request, 'clearance/status.html', {'clearance_forms': clearance_forms})

def notify_admins(clearance_form):
    # Notify all admins about new clearance form
    admins = User.objects.filter(is_staff=True)
    for admin in admins:
        Notification.objects.create(user=admin, message=f'New clearance form submitted by {clearance_form.student.user.username}')

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user, read=False)
    return render(request, 'clearance/notifications.html', {'notifications': notifications})


@login_required
def sign_clearance_form(request, form_id):
    clearance_form = ClearanceForm.objects.get(id=form_id)
    if request.method == 'POST':
        Signature.objects.create(clearance_form=clearance_form, signed_by=request.user, signature='ElectronicSignature')
        clearance_form.status = 'Approved'
        clearance_form.save()
        return redirect('clearance_status')
    return render(request, 'clearance/sign_form.html', {'form': clearance_form})


@login_required
def admin_report(request):
    if not request.user.is_staff:
        return redirect('home')
    clearance_forms = ClearanceForm.objects.all()
    return render(request, 'clearance/admin_report.html', {'clearance_forms': clearance_forms})
