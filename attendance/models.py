from django.db import models

class Leave(models.Model):
    leave_id = models.IntegerField(primary_key=True)
    leave_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'leave'


class Leavedetail(models.Model):
    detail_id = models.IntegerField(primary_key=True)
    leave = models.ForeignKey(Leave, models.DO_NOTHING, blank=True, null=True)
    staff = models.ForeignKey('users.Staffprofile', models.DO_NOTHING, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        db_table = 'leavedetail'

