from django.shortcuts import render, redirect
from django.db import connection

def index(request):
    if 'user_id' in request.session:
        role = request.session.get('user_role')
        
        if role == 'Admin':
            return redirect('users:admin_dashboard')
        else:
            return redirect('users:profile')      
    
    return redirect('users:login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        raw_password = request.POST.get('password') 
        
        with connection.cursor() as cursor:
            # Get raw password
            query = "SELECT id, password, role FROM person WHERE username = %s"
            cursor.execute(query, [username])
            row = cursor.fetchone()

        if row:
            person_id, password_from_db, role = row
            
            if raw_password == password_from_db:
                # THIẾT LẬP SESSION THỦ CÔNG
                request.session['user_id'] = person_id
                request.session['user_role'] = role
                
                # Redirect
                if role == 'Admin':
                    return redirect('users:admin_dashboard')
                else:
                    return redirect('users:profile') 
        
        error = 'Tên đăng nhập hoặc mật khẩu không hợp lệ.'
        return render(request, 'login.html', {'error': error})
    
    return render(request, 'login.html')


def logout_view(request):
    # Tương đương với session.clear() hoặc xóa các khóa session thủ công
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'user_role' in request.session:
        del request.session['user_role']
        
    return redirect('users:login')

def profile_view(request):
    # Bảo vệ trang bằng cách kiểm tra session thủ công
    if 'user_id' not in request.session:
         return redirect('users:login') 
         
    # Ở đây, bạn có thể tải thông tin Person từ DB bằng ID trong session:
    # person_id = request.session['user_id']
    # person_obj = Person.objects.get(id=person_id)
    
    return render(request, 'profile.html')

def admin_dashboard_view(request):
    if 'user_id' not in request.session or request.session.get('user_role') != 'Admin':
        return redirect('users:login') 
    return render(request, 'base_admin.html')