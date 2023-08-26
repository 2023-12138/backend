from django.shortcuts import render
from Tools.LoginCheck import loginCheck
from django.shortcuts import render
from Chat.models import *
import json
from Chat.consumers import userSocketDict
from django.db.models import Q
from django.http import JsonResponse
from channels.db import database_sync_to_async


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


@loginCheck
async def getHistory(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    tid = json_obj.get('tid')  # 团队id
    senderId = json_obj.get('senderId')  # 私聊对象的uid
    uid = user.uid  # 自己的uid
    userSocket = userSocketDict.get(uid)
    if tid != "":  # 群消息记录
        cid = await get_cid(tid)  # 聊天室id
        recordTmp = await get_record(cid)  # 获取该聊天室所有的聊天记录
        sorted(recordTmp, key=lambda x: x.time, reverse=True)  # 大到小
        for obj in recordTmp:
            await userSocket.send(text_data=json.dumps(
                {"message": obj.content, "senderId": obj.sender, "teamId": tid, "time": obj.time, "type": "chat"}))
    elif senderId != "":  # 私聊消息记录
        chatRoom1 = await get_chatroom(uid, senderId)
        chatRoom2 = await get_chatroom(senderId, uid)
        cid = -1
        if chatRoom1.exists():
            cid = chatRoom1[0].cid
        elif chatRoom2.exists():
            cid = chatRoom2[0].cid
        else:
            newChatRoom = Chatroom()
            newChatRoom.save()
            cid = newChatRoom.cid
        recordTmp = await get_record(cid)  # 获取该聊天室所有的聊天记录
        for obj in recordTmp:
            await userSocket.send(
                text_data=json.dumps(
                    {"message": obj.content, "senderId": obj.sender, "teamId": tid, "time": obj.time, "type": "chat"}))
    return JsonResponse({'code': 200, 'message': "历史记录获取成功", "data": {}})


@database_sync_to_async
def get_cid(tid):
    return ChatUser.objects.get(tid=tid).cid


@database_sync_to_async
def get_record(cid):
    return Record.objects.filter(cid=cid)


@database_sync_to_async
def get_chatroom(uid, senderId):
    return ChatUser.objects.filter(Q(from_uid=uid) & Q(to_uid=senderId))
