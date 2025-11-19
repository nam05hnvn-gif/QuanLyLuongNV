Cài môi trường:
    pip install django pymysql
    import payroll_db.sql vào workbench
    vào payroll_project\settings.py và chỉnh sửa lại
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'payroll_db',  # Tên DB trong Workbench
            'USER': 'root',        # User MySQL
            'PASSWORD': '123456',  # <--- Nhập mật khẩu MySQL vào đây
            'HOST': '127.0.0.1',  
            'PORT': '3306',
        }
    }
    python manage.py makemigrations
    python manage.py migrate --fake
Chạy thử:
    python manage.py runserver

