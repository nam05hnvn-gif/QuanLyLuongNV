from django.db import models

# Create your models here.
class Fund(models.Model):
    fund_id = models.IntegerField(primary_key=True)
    fund_name = models.CharField(max_length=100)
    fund_amount = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'fund'


class Fundtransaction(models.Model):
    transaction_id = models.IntegerField(primary_key=True)
    fund = models.ForeignKey(Fund, models.DO_NOTHING)
    admin = models.ForeignKey('users.Person', models.DO_NOTHING)
    old_fund = models.DecimalField(max_digits=15, decimal_places=2)
    new_fund = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_date = models.DateTimeField()

    class Meta:
        db_table = 'fundtransaction'
