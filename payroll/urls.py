from django.urls import path
from . import views

app_name='payroll'

urlpatterns = [
    path('view_salary/', views.view_salary, name='view_salary'),
    path('add_salary/', views.add_salary, name='add_salary'),
    path('view_history_salary/', views.view_history_salary, name='view_history_salary'),
    path('salary_payment/', views.salary_payment, name='salary_payment')
]
