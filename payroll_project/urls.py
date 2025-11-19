from django.contrib import admin
from django.urls import path, include
from users.views import index # Import view trang chủ từ App core

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # TRANG CHỦ (ROOT URL)
    path('', index, name='home'),

    # KẾT NỐI CÁC APP CON 
    #path('users/', include('users.urls', namespace='users')),
    #path('payroll/', include('payroll.urls', namespace='payroll')),
    #path('attendance/', include('attendance.urls', namespace='attendance')),
    #path('funds/', include('funds.urls', namespace='funds')),
]