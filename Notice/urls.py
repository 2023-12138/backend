# -*- coding = utf-8 -*-
# @Time: 2023-08-26 10:16
# @Author :张志扬
# @File : urls.py.py
# @Software: PyCharm
from django.urls import path
from Notice import  views

urlpatterns = [
    path('allread', views.allRead),#一键已读
    path('oneread',views.oneRead),#读指定消息
    path('alldelete',views.allDelete),#一键删除
    path('onedelete',views.oneDelete),#删除指定消息
]