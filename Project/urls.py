from django.urls import path
from Project import views
urlpatterns = [
    path('createProject',views.createProject),#创建新项目
    path('deleteProject',views.deleteProject),#删除项目
    path('recoverProject',views.recoverProject),#恢复项目
    path('renameProject',views.renameProject),#重命名项目
    path('viewProject',views.viewProject),#查看团队下属项目
    path('getProject',views.getProject),#获取某个项目信息
    path('searchProject',views.searchProject),#搜索项目
]