# chat/consumers.py
import datetime
import json
from .models import *
from Team.models import *
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q
from django.http import JsonResponse

userSocketDict = {}

class ChatConsumer(AsyncWebsocketConsumer):
    uid=-1

    async def connect(self):
        self.uid = int(self.scope["url_route"]["kwargs"]["uid"])
        userSocketDict[self.uid] = self

        # Join room group

        await self.accept()

    async def disconnect(self, close_code):
        del userSocketDict[self.uid]
        # Leave room group

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        #需要信息{"uid","tid","teamname"}
        to_uid = int(text_data_json['to_uid'])  #私聊对象id
        tid = int(text_data_json['tid'])    #群聊团队id
        nowTime = datetime.datetime #当前时间
        if tid == "":   #私聊
            from_uid=int(text_data_json['from_uid'])
            cid=ChatUser.objects.get(Q(from_uid=from_uid)&Q(to_uid=to_uid)) #聊天室id
            toUserSocket = userSocketDict.get(to_uid)
            if toUserSocket != None:        #成员在线
                await toUserSocket.send(text_data=json.dumps({"message": message,"senderId":self.uid,"teamId":tid,"time":time}))
            await self.send(text_data=json.dumps({"message": message,"senderId":self.uid,"teamId":tid,"time":time}))  # 在自己窗口展示
        if to_uid == "": #群聊
            userlist = User_team.objects.filter(tid=tid)    #团队成员列表
            cid=ChatUser.objects.get(tid=tid)       #聊天室id
            for user in userlist:
                toUserSocket = userSocketDict.get(user.uid)
                if toUserSocket != None:            #成员在线
                    await toUserSocket.send(text_data=json.dumps({"message": message,"senderId":self.uid,"teamId":tid,"time":time}))
        new_record = Record(cid=cid, time=dtime, content=message, sender=from_uid)
        # try:
        new_record.save()
        # except:
        #     return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})
        # to = int(text_data_json["to"])  # 要发送给的成员id或者群id
        # toUserSocket = userSocketDict.get(to)
        # await toUserSocket.send(text_data=json.dumps({"message": message}))

