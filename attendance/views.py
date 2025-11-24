from csv import DictReader

from django.shortcuts import render, redirect
import pymysql.cursors
from django.conf import settings
import datetime

from pymysql.cursors import DictCursor

# --- KẾT NỐI DATABASE ---
conn_settings = settings.DATABASES['default']
conn = pymysql.connect(
    host=conn_settings['HOST'],
    user=conn_settings['USER'],
    password=conn_settings['PASSWORD'],
    database=conn_settings['NAME'],
    port=int(conn_settings.get('PORT', 3306)),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)



def admin_leave(request):
    with conn.cursor() as cursor:


        # --- XỬ LÝ POST DUYỆT / TỪ CHỐI ---
        if request.method == 'POST':
            detail_id = request.POST.get('detail_id')
            action = request.POST.get('status')  # approve / reject


            status_map = {
                "approve": "Approved",
                "reject": "Rejected"
            }
            status = status_map.get(action, "Pending")


            cursor.execute("""
                UPDATE leavedetail
                SET status=%s
                WHERE detail_id=%s
            """, (status, detail_id))
            conn.commit()


            return redirect('attendance:admin_leave')


        # --- LẤY DANH SÁCH NGHỈ PHÉP ---
        cursor.execute("""
            SELECT ld.detail_id, ld.reason, ld.status,
                   p.username AS staff_name,
                   ld.leavedetail_date
            FROM leavedetail ld
            JOIN person p ON ld.staff_id = p.id
            ORDER BY ld.leavedetail_date DESC
        """)
        details = cursor.fetchall()


        # --- LẤY NHÂN VIÊN ---
        cursor.execute("SELECT id AS staff_id, username AS name FROM person")
        staff_list = cursor.fetchall()


        # --- ĐẾM NGÀY NGHỈ PHÉP ĐƯỢC DUYỆT ---
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year


        cursor.execute("""
            SELECT ld.staff_id, COUNT(*) AS leave_count
            FROM leavedetail ld
            JOIN `leave` l ON ld.leave_id = l.leave_id
            WHERE ld.status='Approved'
              AND MONTH(l.leave_date)=%s AND YEAR(l.leave_date)=%s
            GROUP BY ld.staff_id
        """, (month, year))


        leave_data = {row['staff_id']: row['leave_count'] for row in cursor.fetchall()}


        # --- TÍNH LƯƠNG ---
        STANDARD_WORK_DAYS = 20
        DAILY_SALARY = 100000
        results = []


        for staff in staff_list:
            leave_count = leave_data.get(staff['staff_id'], 0)
            present_days = STANDARD_WORK_DAYS - leave_count
            absent_days = 0
            salary = present_days * DAILY_SALARY


            results.append({
                "name": staff["name"],
                "present": present_days,
                "leave": leave_count,
                "absent": absent_days,
                "salary_formatted": f"{salary:,}"
            })


    return render(request, "attendance/admin_leave.html", {
        "details": details,
        "results": results
    })


def staff_attendance(request):
    staff_id = request.session.get('user_id')
    if not staff_id:
        return redirect('users:login')

    today = datetime.date.today()
    checked_in = False

    with conn.cursor() as cursor:
        # --- Xử lý check-in ---
        if request.method == "POST":
            cursor.execute("""
                SELECT * FROM attendance
                WHERE staff_id=%s AND date=%s
            """, (staff_id, today))
            exist = cursor.fetchone()
            if not exist:
                cursor.execute("""
                    INSERT INTO attendance(staff_id, date, status, checkin_time)
                    VALUES (%s, %s, 'present', NOW())
                """, (staff_id, today))
                conn.commit()
                checked_in = True

        # --- Lấy toàn bộ lịch attendance, kết hợp nghỉ phép từ leave/leavedetail ---
        cursor.execute("""
            SELECT a.date, 
                   CASE 
                       WHEN ld.status='Approved' THEN 'leave'
                       WHEN a.status='present' THEN 'present'
                       ELSE 'absent'
                   END AS status
            FROM attendance a
            LEFT JOIN leavedetail ld 
                   ON ld.staff_id = a.staff_id
            LEFT JOIN `leave` l 
                   ON l.leave_id = ld.leave_id AND l.leave_date = a.date
            WHERE a.staff_id=%s
            ORDER BY a.date DESC
        """, (staff_id,))
        records = cursor.fetchall()

    return render(request, "attendance/staff_attendance.html", {
        "records": records,
        "today": today,
        "checked_in": checked_in
    })




def attendance_redirect(request):
    role = request.session.get("role")


    if role == "admin":
        return redirect('attendance:admin_leave')
    else:
        return redirect('attendance:staff_calendar')


