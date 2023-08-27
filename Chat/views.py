from django.shortcuts import render
from Tools.LoginCheck import loginCheck,asyncLoginCheck
from django.shortcuts import render
from Chat.models import *
import json
from Chat.consumers import userSocketDict
from django.db.models import Q
from django.http import JsonResponse
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async,async_to_sync
from django.forms.models import model_to_dict


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

@asyncLoginCheck
async def getHistory(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    tid = json_obj.get('tid')  # 团队id
    senderId = json_obj.get('senderId')  # 私聊对象的uid
    # uid = json_obj.get('uid') # 自己的uid
    uid = user.uid
    userSocket = userSocketDict.get(uid)
    if tid != "":  # 群消息记录
        cid = await get_cid(tid)  # 聊天室id
        recordTmp = await get_record(cid)  # 获取该聊天室所有的聊天记录
        async  for obj in recordTmp:
            nowTime = obj.time.strftime("%Y-%m-%d %H:%M:%S")  # 当前时间
            await userSocket.send(text_data=json.dumps(
                {"message": obj.content, "senderId": obj.sender, "receiverId":"","teamId": tid, "time": nowTime, "type": "chat","rid":obj.rid}))
    elif senderId != "":  # 私聊消息记录
        chatRoom1 = await get_chatroom(uid, senderId)
        chatRoom2 = await get_chatroom(senderId, uid)
        cid = -1
        if await chatroom_exists(chatRoom1)==1:
            cid = await chatroom_cid(chatRoom1)
        elif await chatroom_exists(chatRoom2)==1:
            cid = await chatroom_cid(chatRoom2)
        else:
            newChatRoom = Chatroom()
            await chatroom_save(newChatRoom)
            cid = newChatRoom.cid
            newchatuser=ChatUser(cid=cid,from_uid=uid,to_uid=senderId)
            await chatuser_save(newchatuser)
        recordTmp = await get_record(cid)  # 获取该聊天室所有的聊天记录
        async for obj in recordTmp:
            print(model_to_dict(obj))
            nowTime = obj.time.strftime("%Y-%m-%d %H:%M:%S")  # 当前时间

            await userSocket.send(
                text_data=json.dumps(
                    {"message": obj.content, "senderId": obj.sender, "receiverId":obj.uid,"teamId":"","time": nowTime, "type": "chat","rid":obj.rid}))
    return JsonResponse({'code': 200, 'message': "历史记录获取成功", "data": {}})

@database_sync_to_async
def chatroom_save(newChatRoom):
    newChatRoom.save()


@database_sync_to_async
def get_cid(tid):
    return ChatUser.objects.get(tid=tid).cid
@database_sync_to_async
def chatuser_save(chatuser):
    chatuser.save()

@database_sync_to_async
def get_record(cid):
    return Record.objects.filter(cid=cid)


@database_sync_to_async
def get_chatroom(uid, senderId):
    return ChatUser.objects.filter(Q(from_uid=uid) & Q(to_uid=senderId))
@database_sync_to_async
def chatroom_exists(chatroom):
    if chatroom.exists():
        return 1
    else:return 0
@database_sync_to_async
def chatroom_cid(chatroom):
    return chatroom.first().cid