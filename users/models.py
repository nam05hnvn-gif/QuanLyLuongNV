from django.db import models

class Person(models.Model):
    id = models.CharField(primary_key=True, max_length=50, null=False)
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    password = models.CharField(max_length=150, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=5, blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'person'

class Staffmanagement(models.Model):
    manage_id = models.IntegerField(primary_key=True)
    admin = models.ForeignKey(Person, models.DO_NOTHING, blank=True, null=True)
    staff = models.ForeignKey('Staffprofile', models.DO_NOTHING, blank=True, null=True)
    action = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'staffmanagement'


class Staffprofile(models.Model):
    staff = models.OneToOneField(Person, models.DO_NOTHING, primary_key=True)
    salary = models.ForeignKey('payroll.Salary', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'staffprofile'
