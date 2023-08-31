from django.urls import path
from File import  views
urlpatterns = [
    path('createdir',views.createdir),#创建新文件夹
    path('getallfiles',views.getallFiles),#获取所有文件
    path('getprojectfiles',views.getProjectFiles),#获取项目子文件
    path('getfolderfiles',views.getFolderFiles),#获取文件夹子文件
]