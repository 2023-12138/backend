from django.db import models

# Create your models here.
class Doc(models.Model):
    docId=models.AutoField('docId',primary_key=True)
    pid=models.IntegerField('pid')
    docname=models.CharField('docname',max_length=25)
    is_active=models.BooleanField('is_active',default=True)

class DocContent(models.Model):
    docContentId=models.AutoField('docContentId',primary_key=True)
    docId=models.IntegerField('docId')
    docContent=models.TextField('docContent')
    saveTime=models.DateTimeField('saveTime',auto_now_add=True)
    is_active=models.BooleanField('is_active',default=True)