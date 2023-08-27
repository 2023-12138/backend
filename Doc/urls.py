# -*- coding = utf-8 -*-
# @Time: 2023-08-27 11:45
# @Author :张志扬
# @File : urls.py
# @Software: PyCharm
from django.contrib import admin
from django.urls import path, include
from Doc import  views

urlpatterns = [
    path("docaite",views.docAite),#doc @的广播
    path("savedoc",views.saveDoc),#保存文档
]