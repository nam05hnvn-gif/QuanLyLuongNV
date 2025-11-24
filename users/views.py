from django.shortcuts import render, redirect
from django.db import connection, transaction
from datetime import date, datetime

def index(request):
    if 'user_id' in request.session:
        role = request.session.get('user_role')
        
        if role == 'Admin':
            return redirect('users:admin_dashboard')
        else:
            return redirect('users:staff_dashboard')      
    
    return redirect('users:login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        raw_password = request.POST.get('password') 
        
        with connection.cursor() as cursor:
            # raw pw
            query = "SELECT id, password, role FROM person WHERE username = %s"
            cursor.execute(query, [username])
            row = cursor.fetchone()

        if row:
            person_id, password_from_db, role = row
            
            if raw_password == password_from_db:
                # session
                request.session['user_id'] = person_id
                request.session['user_role'] = role
                
                # redirect
                if role == 'Admin':
                    return redirect('users:admin_dashboard')
                else:
                    return redirect('users:staff_dashboard') 
        
        error = 'Tên đăng nhập hoặc mật khẩu không hợp lệ.'
        return render(request, 'login.html', {'error': error})
    
    return render(request, 'login.html')

def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'user_role' in request.session:
        del request.session['user_role']
        
    return redirect('users:login')

# -------------------------ADMIN-------------------------

def admin_dashboard_view(request):
    if 'user_id' not in request.session or request.session.get('user_role') != 'Admin':
        return redirect('users:login') 
    return render(request, 'base_admin.html')

def list_staff_view(request):
    if 'user_id' not in request.session or request.session.get('user_role') != 'Admin':
        return redirect('users:login') 

    staff_list = []
    
    try:
        with connection.cursor() as cursor:
            # JOIN 3 bảng: person, staffprofile, và salary để lấy thông tin nhân viên và lương
            query = """
                SELECT 
                    p.id, p.username, p.gender, p.start_date, p.birth_date,
                    s.rank, s.amount, s.multiplier
                FROM person p
                JOIN staffprofile sp ON p.id = sp.staff_id
                JOIN salary s ON sp.salary_id = s.salary_id
                WHERE 
                    p.role = 'Staff'
                ORDER BY 
                    CAST(p.id AS UNSIGNED) ASC
            """
            cursor.execute(query)
            
            # Lấy tên cột để tạo dictionary
            columns = [col[0] for col in cursor.description]
            
            for row in cursor.fetchall():
                staff_list.append(dict(zip(columns, row)))

    except Exception as e:
        print(f"Database Error: {e}")
        staff_list = []
        
    # Render template và truyền dữ liệu
    context = {
        'staff_list': staff_list,
        'current_admin_id': request.session['user_id']
    }
    
    return render(request, 'list_staff.html', context)

def add_staff_view(request):
    if 'user_id' not in request.session or request.session.get('user_role') != 'Admin':
        return redirect('users:login')
    
    admin_id = request.session['user_id']

    if request.method == 'POST':
        username   = request.POST.get('username')
        password   = request.POST.get('password')
        gender     = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')
        salary_id  = request.POST.get('salary_id')

        start_date = date.today()
        role       = 'Staff'
        try:
            bd = datetime.strptime(birth_date, '%Y-%m-%d').date() 
        except ValueError:
            error = "Định dạng ngày không hợp lệ"
            return render(request, 'add_staff.html', {'error': error})
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT MAX(CAST(id AS UNSIGNED)) FROM person")
                max_id = cursor.fetchone()[0]
                new_id = str(max_id + 1) if max_id is not None else '1'

                with transaction.atomic():
                    person_query = """
                        INSERT INTO person (id, username, password, start_date, role, gender, birth_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(person_query, [
                        new_id,
                        username,
                        password,
                        start_date,
                        role,
                        gender,
                        birth_date
                    ])

                    # Thêm vào bảng staffprofile
                    staff_profile_query = """
                        INSERT INTO staffprofile (staff_id, salary_id)
                        VALUES (%s, %s)
                    """
                    cursor.execute(staff_profile_query, [
                        new_id,
                        salary_id
                    ])

                    # Thêm vào bảng staffmanagement
                    cursor.execute("SELECT MAX(manage_id) FROM staffmanagement")
                    max_manage_id = cursor.fetchone()[0]
                    new_manage_id = max_manage_id + 1 if max_manage_id is not None else 1

                    staff_manage_query = """
                        INSERT INTO staffmanagement (manage_id, admin_id, staff_id, action, timestamp)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(staff_manage_query, [
                        new_manage_id,
                        admin_id,
                        new_id,
                        "Thêm nhân viên mới",
                        datetime.now()
                    ])
                return redirect('users:list_staff')
        except Exception as e:
            error = f"Lỗi khi thêm nhân viên: {e}"
            return render(request, 'add_staff.html', {'error': error})

    return render(request, 'add_staff.html', {})

def delete_staff_view(request, staff_id):
    if 'user_id' not in request.session or request.session.get('user_role') != 'Admin':
        return redirect('users:login')
    
    if str(staff_id) == str(request.session['user_id']):
        print("Cảnh báo: Admin không thể tự xóa tài khoản của chính mình")
        return redirect('users:admin_dashboard')

    try:
        # rollback nếu có lỗi
        with transaction.atomic():
            with connection.cursor() as cursor:
                # Xóa các bản ghi phụ thuộc (Children Tables)
                # Thứ tự xóa: Phụ thuộc nhất -> Gốc
                
                cursor.execute("DELETE FROM leavedetail WHERE staff_id = %s", [staff_id])
                cursor.execute("DELETE FROM salarychangehistory WHERE staff_id = %s", [staff_id])
                cursor.execute("DELETE FROM salarypayment WHERE staff_id = %s", [staff_id])
                cursor.execute("DELETE FROM staffmanagement WHERE staff_id = %s", [staff_id])
                
                cursor.execute("DELETE FROM staffprofile WHERE staff_id = %s", [staff_id])
                
                cursor.execute("DELETE FROM person WHERE id = %s", [staff_id])
                
        return redirect('users:list_staff') 

    except Exception as e:
        print(f"Lỗi khi xóa nhân viên có ID {staff_id}: {e}")
        return redirect('users:list_staff')    


# -------------------------STAFF-------------------------

def staff_dashboard(request):
    if 'user_id' not in request.session:
         return redirect('users:login') 
         
    # staff_id = request.session['user_id']

    return render(request, 'base_staff.html')

def profile_view(request):
    if 'user_id' not in request.session:
         return redirect('users:login') 
         
    staff_id = request.session['user_id']
    profile_data = None

    try:
        with connection.cursor() as cursor:
            # JOIN 3 bảng person, salary, staffprofile để lấy thông tin
            query = """
                SELECT 
                    p.id, p.username, p.role, p.gender, p.start_date, p.birth_date,
                    s.rank, s.amount, s.multiplier
                FROM person p
                JOIN staffprofile sp ON p.id = sp.staff_id
                JOIN salary s ON sp.salary_id = s.salary_id
                WHERE 
                    p.id = %s
            """
            cursor.execute(query, [staff_id])
            row = cursor.fetchone()

            if row:
                columns = [col[0] for col in cursor.description]
                profile_data = dict(zip(columns, row))
    except Exception as e:
        print(f"Database lỗi: {e}")
    
    context = {
        'profile': profile_data,
        'error': 'Không tìm thấy hồ sơ' if profile_data is None else None
    }

    return render(request, 'profile.html', context)

def edit_profile_view(request):
    if 'user_id' not in request.session:
         return redirect('users:login') 

    person_id = request.session['user_id']
    
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_gender = request.POST.get('gender')
        new_birth_date = request.POST.get('birth_date')
        
        # Kiểm tra tính hợp lệ của ngày sinh
        try:
            datetime.strptime(new_birth_date, '%Y-%m-%d').date() 
        except ValueError:
            error = 'Định dạng ngày sinh không hợp lệ.'
            return render(request, 'edit_profile.html', {'error': error})
        
        try:
            with connection.cursor() as cursor:
                update_query = """
                    UPDATE person 
                    SET username = %s, gender = %s, birth_date = %s
                    WHERE id = %s
                """
                cursor.execute(update_query, [
                    new_username, 
                    new_gender, 
                    new_birth_date, 
                    person_id
                ])
                
            return redirect('users:profile') 

        except Exception as e:
            error = f"Lỗi khi cập nhật hồ sơ: {e}"
            return render(request, 'edit_profile.html', {'error': error, 'current_data': request.POST})

    # --- Hiển thị Form hiện tại (GET) ---
    try:
        with connection.cursor() as cursor:
            # Lấy dữ liệu profile hiện tại
            query = """
                SELECT id, username, gender, birth_date 
                FROM person 
                WHERE id = %s
            """
            cursor.execute(query, [person_id])
            row = cursor.fetchone()
            
            if row:
                columns = [col[0] for col in cursor.description]
                profile_data = dict(zip(columns, row))
            else:
                profile_data = None
                
    except Exception as e:
        print(f"Database Error: {e}")
        profile_data = None

    return render(request, 'edit_profile.html', {'profile': profile_data})