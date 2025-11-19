from django.db import models

# Create your models here.
class Leave(models.Model):
    leave_id = models.IntegerField(primary_key=True)
    leave_date = models.DateField()

    class Meta:
        db_table = 'leave'

class Leavedetail(models.Model):
    detail_id = models.IntegerField(primary_key=True)
    leave = models.ForeignKey(Leave, models.DO_NOTHING)
    staff = models.ForeignKey('users.Person', models.DO_NOTHING)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=8)

    class Meta:
        db_table = 'leavedetail'
