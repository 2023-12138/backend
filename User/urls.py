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
]