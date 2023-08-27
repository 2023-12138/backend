from django.db import models
from User.models import User

# Create your models here.
class Chatroom(models.Model):
    cid = models.AutoField('cid',primary_key=True)
    cname = models.CharField('cname',max_length=256,default="FusionChat")
    is_active = models.BooleanField('is_active',default=True)

class ChatUser(models.Model):
    cid = models.IntegerField('cid')
    from_uid = models.IntegerField('from_uid',null=True)
    to_uid = models.IntegerField('to_uid',null=True)
    tid = models.IntegerField('tid',null=True)

class Record(models.Model):
    rid = models.AutoField('rid',primary_key=True)
    cid = models.IntegerField('cid')
    time = models.DateTimeField('time',auto_now_add=True)
    content = models.TextField('content',max_length=1024)
    sender = models.IntegerField('sender',null=True)
    uid=models.IntegerField('uid',null=True)
    tid=models.IntegerField('tid',null=True)
    is_active = models.BooleanField('is_active',default=True)
