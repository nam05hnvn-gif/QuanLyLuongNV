from django.db import models

# Create your models here.
class Person(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=128)
    start_date = models.DateField()
    role = models.CharField(max_length=5)

    class Meta:
        db_table = 'person'

class Staffmanagement(models.Model):
    manage_id = models.IntegerField(primary_key=True)
    admin = models.ForeignKey(Person, models.DO_NOTHING)
    staff = models.ForeignKey(Person, models.DO_NOTHING, related_name='staffmanagement_staff_set')
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'staffmanagement'

class Staffprofile(models.Model):
    staff = models.OneToOneField(Person, models.DO_NOTHING, primary_key=True)
    salary = models.ForeignKey('payroll.Salary', models.DO_NOTHING)
    gender = models.CharField(max_length=6, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'staffprofile'
