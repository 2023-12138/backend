from django.shortcuts import render
from Tools.LoginCheck import loginCheck
import json
# Create your views here.
from django.shortcuts import render


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

@loginCheck
def getHistory(request):
    user=request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    tid = json_obj.get('tid')
    uid=json_obj.get('uid')
