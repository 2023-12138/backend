from django.db import models

class File(models.Model):
    fileID = models.AutoField('fileID', primary_key=True)  # 文件ID
    filename = models.CharField('filename', max_length=25)  # 文件/文件夹名称
    pid = models.IntegerField('pid')  # 所属项目ID
    father = models.IntegerField('father')  # 父文件夹ID
    depth = models.IntegerField('depth')  # 深度 #0代表父文件夹，1代表一级文件夹/文档，2代表二级文档
    type = models.IntegerField('type')  # 0代表文件夹，1代表文档
    docID = models.IntegerField('docID', null=True)  # 文档ID
