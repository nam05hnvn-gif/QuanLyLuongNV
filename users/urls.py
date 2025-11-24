from django.urls import path
from . import views

app_name='users'

# urlpatterns = [
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
#     path('admin/add_staff', views.add_staff_view, name='add_staff'),
#     path('admin/list_staff', views.list_staff_view, name='list_staff'),
#     path('admin/delete_staff/<str:staff_id>', views.delete_staff_view, name='delete_staff'),
#     path('profile/', views.profile_view, name='profile'),
#     path('profile/edit', views.edit_profile_view, name='edit_profile'),
#     path('staff_dashboard', views.staff_dashboard, name='staff_dashboard')
# ]

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ADMIN FEATURES 
    path('admin/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/staffs/', views.list_staff_view, name='list_staff'),
    path('admin/staffs/add/', views.add_staff_view, name='add_staff'),
    path('admin/staffs/delete/<str:staff_id>/', views.delete_staff_view, name='delete_staff'), 
    path('admin/staffs/edit/<str:staff_id>/', views.admin_edit_staff_view, name='admin_edit_staff'),

    # STAFF FEATURES 
    path('staff/', views.staff_dashboard, name='staff_dashboard'), 
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/salary_history', views.salary_history_view, name='salary_history'),
    path('profile/leave_history', views.leave_history_view, name='leave_history'),
    path('profile/change_password', views.change_password_view, name='change_password'),

    path('leave_request/', views.leave_request, name='leave_request')

]
