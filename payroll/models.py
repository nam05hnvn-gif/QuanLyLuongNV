from django.db import models

class Salary(models.Model):
    salary_id = models.IntegerField(primary_key=True)
    rank = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    multiplier = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'salary'


class Salarychangehistory(models.Model):
    history_id = models.IntegerField(primary_key=True)
    admin = models.ForeignKey('users.Person', models.DO_NOTHING, blank=True, null=True)
    staff = models.ForeignKey('users.Staffprofile', models.DO_NOTHING, blank=True, null=True)
    salary = models.ForeignKey(Salary, models.DO_NOTHING, blank=True, null=True)
    old_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    new_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    old_multiplier = models.FloatField(blank=True, null=True)
    new_multiplier = models.FloatField(blank=True, null=True)
    change_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'salarychangehistory'


class Salarypayment(models.Model):
    payment_id = models.IntegerField(primary_key=True)
    staff = models.ForeignKey('users.Staffprofile', models.DO_NOTHING, blank=True, null=True)
    admin = models.ForeignKey('users.Person', models.DO_NOTHING, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    salary = models.ForeignKey(Salary, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'salarypayment'

