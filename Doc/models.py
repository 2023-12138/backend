from django.db import models

# Create your models here.
class Doc(models.Model):
    docId=models.AutoField('docId',primary_key=True)
    pid=models.IntegerField('pid') #文档所属的项目id
    docname=models.CharField('docname',max_length=25) #文档名称
    is_active=models.BooleanField('is_active',default=True)

class DocContent(models.Model):
    docContentId=models.AutoField('docContentId',primary_key=True)
    docId=models.IntegerField('docId') #文档id
    docContent=models.TextField('docContent',default="") #文档内容
    saveTime=models.DateTimeField('saveTime',auto_now_add=True) #保存时间
    is_active=models.BooleanField('is_active',default=True)