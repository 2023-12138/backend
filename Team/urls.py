from django.urls import path
from Team import  views
urlpatterns = [
    path('createTeam', views.createTeam),
    path('inviteUser', views.inviteUser),
    path('viewTeam',views.viewTeam),
    path('deleteUser',views.deleteUser),
    path('addAdmin',views.addAdmin),
    path('removeAdmin',views.removeAdmin),
    path('viewUser',views.viewUser),
    path('getUsers',views.getUsers),
]