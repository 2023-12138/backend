from django.urls import path
from Project import views
urlpatterns = [
    path('createProject',views.createProject),#创建新项目
    path('deleteProject',views.deleteProject),#删除项目
    path('recoverProject',views.recoverProject),#恢复项目
    path('renameProject',views.renameProject),#重命名项目
    path('viewProject',views.viewProject),
]