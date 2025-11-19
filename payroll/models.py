from django.db import models

# Create your models here.
class Salary(models.Model):
    salary_id = models.IntegerField(primary_key=True)
    salary_rank = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    multiplier = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'salary'

class Salarychangehistory(models.Model):
    history_id = models.IntegerField(primary_key=True)
    staff = models.ForeignKey('users.Person', models.DO_NOTHING)
    admin = models.ForeignKey('users.Person', models.DO_NOTHING, related_name='salarychangehistory_admin_set')
    salary = models.ForeignKey(Salary, models.DO_NOTHING)
    old_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    new_amount = models.DecimalField(max_digits=15, decimal_places=2)
    old_multiplier = models.FloatField(blank=True, null=True)
    new_multiplier = models.FloatField(blank=True, null=True)
    change_date = models.DateTimeField()

    class Meta:
        db_table = 'salarychangehistory'

class Salarypayment(models.Model):
    payment_id = models.IntegerField(primary_key=True)
    staff = models.ForeignKey('users.Person', models.DO_NOTHING)
    admin = models.ForeignKey('users.Person', models.DO_NOTHING, related_name='salarypayment_admin_set')
    salary = models.ForeignKey(Salary, models.DO_NOTHING)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateTimeField()

    class Meta:
        db_table = 'salarypayment'
