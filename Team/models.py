from django.db import models

# Create your models here.
class Team(models.Model):
    tid=models.AutoField('tid',primary_key=True) #团队id
    teamname=models.CharField('teamname', max_length=25) #团队名称
    teaminform=models.TextField('teaminform',max_length=255) #团队信息
    is_active = models.BooleanField('is_active', default=True)  # 伪删除字段

class User_team(models.Model):
    uid = models.IntegerField('uid')  # 用户id
    tid = models.IntegerField('tid')  # 团队id
    status=models.CharField('status',max_length=25) #用户角色
    is_active = models.BooleanField('is_active', default=True)  # 伪删除字段