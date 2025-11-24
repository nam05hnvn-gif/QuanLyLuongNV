from django.shortcuts import render, redirect
from django.db import connection, transaction
from django.utils import timezone
from datetime import date, datetime
from zoneinfo import ZoneInfo

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

    # Truy vấn bậc lương
    salary_ranks = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT salary_id, rank FROM salary ORDER BY CAST(salary_id AS UNSIGNED)")
            salary_ranks = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Lỗi truy vấn bậc lương: {e}")

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
                        timezone.now().astimezone(ZoneInfo("Asia/Ho_Chi_Minh"))
                    ])
                return redirect('users:list_staff')
        except Exception as e:
            error = f"Lỗi khi thêm nhân viên: {e}"
            return render(request, 'add_staff.html', {'error': error,  'salary_ranks': salary_ranks})

    return render(request, 'add_staff.html', {'salary_ranks': salary_ranks})

def admin_edit_staff_view(request, staff_id):
    if 'user_id' not in request.session or request.session.get('user_role') != 'Admin':
        return redirect('users:login')
    
    admin_id = request.session['user_id']
    staff_data = None # Khai báo để có scope toàn cục trong hàm
    
    # Lấy danh sách bậc lương có sẵn
    salary_ranks = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT salary_id, rank, amount FROM salary ORDER BY CAST(salary_id AS UNSIGNED)")
            salary_ranks = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Lỗi truy vấn bậc lương: {e}")

    try:
        with connection.cursor() as cursor:
            # JOIN 4 bảng person, staffprofile, salary
            query = """
                SELECT 
                    p.id, p.username, p.gender, p.birth_date, p.start_date,
                    sp.salary_id, s.rank
                FROM person p
                JOIN staffprofile sp ON p.id = sp.staff_id
                JOIN salary s ON sp.salary_id = s.salary_id
                WHERE p.id = %s
            """
            cursor.execute(query, [staff_id])
            row = cursor.fetchone()
            
            if row:
                columns = [col[0] for col in cursor.description]
                staff_data = dict(zip(columns, row))
            
    except Exception as e:
        print(f"Database Error: {e}")
        staff_data = None

    # =================================================================================

    if request.method == 'POST':
        new_username   = request.POST.get('username')
        new_gender     = request.POST.get('gender')
        new_birth_date = request.POST.get('birth_date')
        new_salary_id  = request.POST.get('salary_id')
        
        # Check lỗi Ngày sinh
        try:
            datetime.strptime(new_birth_date, '%Y-%m-%d').date() 
        except ValueError:
            context = {
                'staff': staff_data,
                'error': 'Định dạng ngày sinh không hợp lệ.', 
                'salary_ranks': salary_ranks
            }
            return render(request, 'admin_edit_staff.html', context)

        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("SELECT salary_id FROM staffprofile WHERE staff_id = %s", [staff_id])
                    old_salary_id = cursor.fetchone()[0]

                    # Cập nhật Person
                    person_query = """
                        UPDATE person 
                        SET username = %s, gender = %s, birth_date = %s
                        WHERE id = %s
                    """
                    cursor.execute(person_query, [
                        new_username, new_gender, new_birth_date, staff_id
                    ])

                    # Cập nhật StaffProfile và ghi Log
                    if str(old_salary_id) != str(new_salary_id):
                        # Lấy lương cũ 
                        cursor.execute(
                            "SELECT amount, multiplier FROM salary WHERE salary_id = %s",
                            [old_salary_id]
                        )
                        old_amount, old_multiplier = cursor.fetchone()

                        # Lấy lương mới
                        cursor.execute(
                            "SELECT amount, multiplier FROM salary WHERE salary_id = %s",
                            [new_salary_id]
                        )
                        new_amount, new_multiplier = cursor.fetchone()

                        staff_profile_query = """
                            UPDATE staffprofile 
                            SET salary_id = %s
                            WHERE staff_id = %s
                        """
                        cursor.execute(staff_profile_query, [new_salary_id, staff_id])

                        # Ghi Log
                        cursor.execute("SELECT MAX(history_id) FROM salarychangehistory")
                        max_history_id = cursor.fetchone()[0]
                        new_history_id = max_history_id + 1 if max_history_id is not None else 1

                        history_query = """
                            INSERT INTO salarychangehistory (history_id, admin_id, staff_id, salary_id, old_amount, new_amount, old_multiplier, new_multiplier, change_date)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(history_query, [
                            new_history_id, 
                            admin_id, staff_id, new_salary_id,
                            old_amount, new_amount,
                            old_multiplier, new_multiplier,
                            timezone.now().astimezone(ZoneInfo("Asia/Ho_Chi_Minh"))
                        ])
                        
            return redirect('users:list_staff') 

        except Exception as e:
            error = f"Lỗi khi cập nhật nhân viên: {e}"
            context = {
                'staff': staff_data,
                'error': error, 
                'salary_ranks': salary_ranks
            }
            return render(request, 'admin_edit_staff.html', context)

    # --- Hiển thị Form hiện tại (GET) ---
    context = {
        'staff': staff_data,
        'salary_ranks': salary_ranks,
        'error': 'Không tìm thấy hồ sơ nhân viên này.' if staff_data is None else None
    }
    
    return render(request, 'admin_edit_staff.html', context)

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

def salary_history_view(request):
    if 'user_id' not in request.session:
        return redirect('users:login')
    
    staff_id = request.session['user_id']
    payment_history = []

    try:
        with connection.cursor() as cursor:
            # Lấy chi tiết các lần thanh toán, sắp xếp từ mới nhất
            query = """
                SELECT 
                    sp.payment_id, sp.payment_date, sp.total_amount
                FROM salarypayment sp
                WHERE sp.staff_id = %s
                ORDER BY sp.payment_date DESC
            """
            cursor.execute(query, [staff_id])
            
            columns = [col[0] for col in cursor.description]
            payment_history = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
    except Exception as e:
        print(f"Lỗi truy vấn lịch sử lương: {e}")
        
    context = {
        'payment_history': payment_history
    }
    return render(request, 'salary_history.html', context)

def leave_history_view(request):
    if 'user_id' not in request.session:
        return redirect('users:login')
    
    staff_id = request.session['user_id']
    leave_requests = []

    try:
        with connection.cursor() as cursor:
            # JOIN leavedetail (ld) và leave (l)
            query = """
                SELECT 
                    ld.detail_id,       
                    l.leave_date,       
                    ld.reason,          
                    ld.status           
                FROM leavedetail ld
                JOIN `leave` l ON ld.leave_id = l.leave_id -- `` do leave là từ khóa 
                WHERE ld.staff_id = %s
                ORDER BY l.leave_date DESC
            """
            cursor.execute(query, [staff_id])
            
            columns = [col[0] for col in cursor.description]
            leave_requests = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
    except Exception as e:
        print(f"Lỗi truy vấn lịch sử nghỉ phép: {e}")
        
    context = {
        'leave_requests': leave_requests
    }
    return render(request, 'leave_history.html', context)

def change_password_view(request):
    if 'user_id' not in request.session:
        return redirect('users:login')

    person_id = request.session['user_id']
    error = None
    message = None

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            error = 'Mật khẩu mới và xác nhận mật khẩu không khớp.'
        # elif len(new_password) < 6:
        #     error = 'Mật khẩu mới phải có ít nhất 6 ký tự.'
        else:
            try:
                with connection.cursor() as cursor:
                    query_check = "SELECT password FROM person WHERE id = %s"
                    cursor.execute(query_check, [person_id])
                    row = cursor.fetchone()
                    
                    if row and row[0] == old_password:
                        update_query = "UPDATE person SET password = %s WHERE id = %s"
                        cursor.execute(update_query, [new_password, person_id])
                        message = 'Đổi mật khẩu thành công!'
                    else:
                        error = 'Mật khẩu cũ không chính xác.'
            except Exception as e:
                error = f"Lỗi khi cập nhật mật khẩu: {e}"
                print(f"Database Error: {e}")

    context = {
        'error': error,
        'message': message
    }
    return render(request, 'change_password.html', context)

