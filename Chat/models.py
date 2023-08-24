from django.db import models
from User.models import User

# Create your models here.
class Chatroom(models.Model):
    cid = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=256)

class ChatUser(models.Model):
    cid = models.IntegerField(max_length=1024)
    uid1 = models.IntegerField(max_length=1024, null=True)
    uid2 = models.IntegerField(max_length=1024, null=True)
    tid = models.IntegerField(max_length=1024, null=True)

class Record(models.Model):
    rid = models.AutoField(primary_key=True)
    cid = models.IntegerField(max_length=1024)
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1024)
    sender = models.IntegerField(max_length=1024, null=True)
