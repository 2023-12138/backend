from django.urls import path
from File import  views
urlpatterns = [
    path('createdir',views.createdir),#创建新文件夹
    path('getfiles',views.getFiles),#获取文件夹
]