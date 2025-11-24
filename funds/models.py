from django.db import models

class Fund(models.Model):
    fund_id = models.IntegerField(primary_key=True)
    fund_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'fund'


class Fundtransaction(models.Model):
    transaction_id = models.IntegerField(primary_key=True)
    fund = models.ForeignKey(Fund, models.DO_NOTHING, blank=True, null=True)
    admin = models.ForeignKey('users.Person', models.DO_NOTHING, blank=True, null=True)
    old_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    new_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'fundtransaction'
