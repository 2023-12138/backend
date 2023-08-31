from django.db import models

class Project(models.Model):
    pid = models.AutoField('pid', primary_key=True)  # 项目id
    project_name = models.CharField('project_name', max_length=25)  # 项目名称
    project_inform = models.TextField('project_inform', max_length=255)  # 项目信息
    tid = models.IntegerField('tid')  # 所属团队
    uid = models.IntegerField('uid')  # 创建者
    groupid = models.CharField('groupid', max_length=55)
    create_time = models.DateTimeField('create_time', auto_now_add=True)  # 创建时间
    is_active = models.BooleanField('is_active', default=True)  # 伪删除字段

class Prototype(models.Model):
    protoid = models.AutoField("protoid",primary_key = True) #原型id
    pid = models.IntegerField("pid") #原型所属的项目id
    protoname = models.CharField("protoname",max_length=25) #原型设计名称

class Protoinfo(models.Model):
    proto_info_id = models.IntegerField("proto_info_id",primary_key=True)
    info = models.JSONField("info")  # 保存style和data信息
    use = models.BooleanField("use", default=False)  # 该原型是否有人使用
