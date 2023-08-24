from django.db import models

# Create your models here.
class User(models.Model):#有自增主键 id,记录用户基本信息
    uid = models.AutoField('uid',primary_key=True) #用户id
    username = models.CharField('username', max_length=25) #用户名
    password = models.CharField('password', max_length=25) #密码
    name = models.CharField('name', max_length=10) #真实姓名
    phone = models.CharField('phone', default='null', max_length=11) #手机号
    email = models.EmailField('email', default='null') #邮箱
    is_active = models.BooleanField('is_active', default=True)  # 伪删除字段

