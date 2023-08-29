# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path("getHistory",views.getHistory),#获取历史记录
    path("savefile",views.saveFile), #保存图片，文件
]