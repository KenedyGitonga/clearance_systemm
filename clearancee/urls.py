from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('generate/', views.generate_clearance_form, name='generate_clearance_form'),
    path('status/', views.clearance_status, name='clearance_status'),
    path('notifications/', views.notifications, name='notifications'),
    path('sign/<int:form_id>/', views.sign_clearance_form, name='sign_clearance_form'),
    path('admin_report/', views.admin_report, name='admin_report'),
]