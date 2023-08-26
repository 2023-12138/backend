from django.db import models

# Create your models here.
class Notice(models.Model):
    noticeId  = models.AutoField('nid',primary_key=True)  #消息id
    uid  = models.IntegerField('uid') #用户id
    rid = models.IntegerField('rid') #聊天记录id
    is_active = models.BooleanField('is_active',default=True) #默认未读
    tid = models.IntegerField('tid') #@该用户的组id
    docId = models.IntegerField('docId') #@该用户的文档id
    type = models.CharField('type') #"chat"代表群聊@,"doc"代表文档@
