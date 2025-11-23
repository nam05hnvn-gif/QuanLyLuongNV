from django.urls import path
from . import views


app_name = 'attendance'


urlpatterns = [
    path('', views.attendance_redirect, name='attendance'),
    path('admin_leave/', views.admin_leave, name='admin_leave'),
    path('staff_attendance/', views.staff_attendance, name='staff_attendance'),
]
