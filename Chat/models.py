from django.db import models
from User.models import User

# Create your models here.
class Chatroom(models.Model):
    cid = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)

class ChatUser(models.Model):
    cid = models.IntegerField()
    uid1 = models.IntegerField(null=True)
    uid2 = models.IntegerField(null=True)
    tid = models.IntegerField(null=True)

class Record(models.Model):
    rid = models.AutoField(primary_key=True)
    cid = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1024)
    sender = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
