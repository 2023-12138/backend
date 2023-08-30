from django.db import models

class Project(models.Model):
    pid = models.AutoField('pid', primary_key=True)  # 项目id
    project_name = models.CharField('project_name', max_length=25)  # 项目名称
    project_inform = models.TextField('project_inform', max_length=255)  # 项目信息
    tid = models.IntegerField('tid')  # 所属团队
    uid = models.IntegerField('uid')  # 创建者
    groupid=models.CharField('groupid',max_length=55)
    is_active = models.BooleanField('is_active', default=True)  # 伪删除字段


