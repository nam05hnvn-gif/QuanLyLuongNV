import datetime

from django.shortcuts import render, redirect
import pymysql.cursors
from django.db import connection
from django.urls import reverse
from pymysql.cursors import DictCursor
from django.conf import settings


conn_settings = settings.DATABASES['default']
conn = pymysql.connect(
    host=conn_settings['HOST'],
    user=conn_settings['USER'],
    password=conn_settings['PASSWORD'],
    database=conn_settings['NAME'],
    port=int(conn_settings.get('PORT', 3306)),
    charset='utf8mb4',
    cursorclass=DictCursor
)
# Create your views here.
def view_salary(request):
    salary_data = None
    salary_id = request.GET.get('salary_id')  # Lấy từ hidden input khi ấn

    # Nếu GET có salary_id → lấy dữ liệu để hiển thị trên form
    if salary_id:
        cursor = conn.cursor(DictCursor)
        cursor.execute("SELECT * FROM salary WHERE salary_id=%s", (salary_id,))
        salary_data = cursor.fetchone()
        cursor.close()

    # Nếu POST (submit form sửa)
    if request.method == 'POST':
        salary_id = request.POST.get('salary_id')
        salary_rank = request.POST.get('salary_rank')
        amount = request.POST.get('amount')
        multiplier = request.POST.get('multiplier')

        cursor = conn.cursor(DictCursor)
        # 1. Lấy dữ liệu cũ
        cursor.execute("SELECT `rank`, amount, multiplier FROM salary WHERE salary_id=%s", (salary_id,))
        old = cursor.fetchone()

        old_rank = old["rank"]
        old_amount = old["amount"]
        old_multiplier = old["multiplier"]

        #2: Update bảng salary
        cursor.execute(
            "UPDATE salary SET `rank`=%s, amount=%s, multiplier=%s WHERE salary_id=%s",
            (salary_rank, amount, multiplier, salary_id)
        )

        # 3. Ghi lịch sử thay đổi
        cursor.execute(
            """
            INSERT INTO salarychangehistory(
                salary_id, old_rank, new_rank,
                old_amount, new_amount,
                old_multiplier, new_multiplier,
                change_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            """,
            (salary_id,
             old_rank, salary_rank,
             old_amount, amount,
             old_multiplier, multiplier)
        )
        conn.commit()
        cursor.close()
        return redirect('payroll:view_salary')  # Reload bảng sau khi sửa

    cursor = conn.cursor(DictCursor)
    cursor.execute("SELECT * FROM salary")
    salary_list = cursor.fetchall()
    cursor.close()

    return render(request, 'view_salary.html', {
        'salary': salary_list,
        'edit_salary': salary_data,  # None nếu chưa chọn dòng
    })

def add_salary(request):
    if request.method == 'POST':
        salary_id = request.POST.get('salary_id')
        salary_rank = request.POST.get('salary_rank')
        amount = request.POST.get('amount')
        multiplier = request.POST.get('multiplier')
        cursor=conn.cursor(DictCursor)
        sql='''
            INSERT INTO salary (salary_id, `rank`, amount, multiplier)
                VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(sql, (salary_id, salary_rank, amount, multiplier))
        cursor.close()
        conn.commit()
        return redirect('payroll:view_salary')
    return render(request, 'add_salary.html')

def view_history_salary(request):
    if request.method=='POST':
        history_id=request.POST.get('history_id')
        cursor=conn.cursor(DictCursor)
        cursor.execute('''
            DELETE from salarychangehistory
            where history_id=%s
        ''', (history_id,))
        conn.commit()
        cursor.close()
        return redirect('payroll:view_history_salary')
    cursor=conn.cursor(DictCursor)
    sql=''' 
        select * from salarychangehistory
    '''
    cursor.execute(sql)
    histories=cursor.fetchall()
    cursor.close()

    return render(request, 'view_history_salary.html', {'histories': histories})

def salary_payment(request):
    status = request.GET.get("status")

    cursor=conn.cursor(DictCursor)
    if request.method=='POST':
        status = request.GET.get('status', '')
        staff_id=request.POST.get('staff_id')
        month=request.POST.get('month')
        admin_id='2'
        total_amount=request.POST.get('total_amount')
        salary_id = request.POST.get('salary_id')
        payment_datetime = datetime.datetime.strptime(month + "-15 0:0:00", "%Y-%m-%d %H:%M:%S")

        cursor.execute("SELECT MAX(payment_id) AS max_id FROM salarypayment")
        result = cursor.fetchone()
        max_id = result['max_id'] if result['max_id'] is not None else 0
        new_payment_id = max_id + 1

        cursor.execute('''
            INSERT INTO salarypayment(
                staff_id, total_amount, admin_id, salary_id, payment_date, payment_id
            ) VALUES (%s, %s, %s, %s, %s, %s)
        ''', (staff_id, total_amount, admin_id, salary_id, payment_datetime, new_payment_id))
        conn.commit()
        redirect_url = f"{reverse('payroll:salary_payment')}?month={month}"
        if status:
            redirect_url += f"&status={status}"
        return redirect(redirect_url)

    months = range(1, 13)
    select_month=request.GET.get('month')
    admin_id='2'
    query='''
        SELECT 
    s1.id, s1.username, s2.salary_id, s2.rank, s2.amount, s2.multiplier,
    COALESCE(sp.total_amount, s2.amount * s2.multiplier) AS total_salary,
    sp.payment_date,
    CASE WHEN sp.payment_date IS NOT NULL THEN 1 ELSE 0 END AS is_paid
    FROM staffprofile s
    JOIN person s1 ON s.staff_id = s1.id
    JOIN salary s2 ON s.salary_id = s2.salary_id
    LEFT JOIN salarypayment sp
        ON sp.staff_id = s.staff_id
       AND DATE_FORMAT(sp.payment_date, '%%Y-%%m') = %s
    '''
    params = [select_month]
    # Lọc theo trạng thái
    if status == "paid":
        query += " WHERE sp.payment_date IS NOT NULL"
    elif status == "unpaid":
        query += " WHERE sp.payment_date IS NULL"

    cursor.execute(query, params)
    salaries=cursor.fetchall()
    if not select_month: return render(request, 'salary_payment.html', {'months':months})
    return render(request, 'salary_payment.html', {'salaries':salaries,
                                                   'months':months,
                                                   'selected_month':select_month,
                                                   'admin_id':admin_id,
                                                   "selected_status": status})