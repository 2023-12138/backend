from django.urls import path
from Project import views
urlpatterns = [
    path('createProject',views.createProject),#创建新项目
    path('deleteProject',views.deleteProject),#删除项目
    path('recoverProject',views.recoverProject),#恢复项目
    path('renameProject',views.renameProject),#重命名项目
    path('renameProjectInform',views.renameProjectInform),#重命名项目描述
    path('viewProject',views.viewProject),#查看团队下属项目
    path('getProject',views.getProject),#获取某个项目信息
    path('createProto',views.createProto),#创建项目原型
    path('getProto',views.getProto) ,#获取项目下的原型
    path('saveProto',views.saveInfo),#保存原型信息
    path('getProtoInfo',views.getProtoInfo),#获取某个原型的信息
    path('searchProject',views.searchProject),#搜索项目
    path('copyProject', views.copyProject),  # 复制项目
]