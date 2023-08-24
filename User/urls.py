# -*- coding = utf-8 -*-
# @Time: 2023-08-24 14:52
# @Author :张志扬
# @File : urls.py.py
# @Software: PyCharm
from django.urls import path
from User import  views

urlpatterns = [
    path('login', views.userLogin),#登录
    path('register', views.userRegister),#注册
    path('sendCaptcha',views.sendCaptcha),#发送验证码
    path('changeInfo',views.changeInformation),#修改个人信息
    path('changePwd',views.changePassword),#修改密码
    path('pwdFind',views.pwdFind),#找回密码
    path('showInfo',views.showInfo),#查询用户信息
]