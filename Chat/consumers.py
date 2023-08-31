# chat/consumers.py
import asyncio
import datetime
import json
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async, async_to_sync
from .models import *
from Team.models import *
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q
from django.http import JsonResponse
from Notice.models import *
from User.models import *
userSocketDict = {}


class ChatConsumer(AsyncWebsocketConsumer):
    uid = -1
    uname = ""
    async def connect(self):
        self.uid = int(self.scope["url_route"]["kwargs"]["uid"])
        userSocketDict[self.uid] = self
        self.uname = await self.get_username(self.uid)
        # Join room group

        await self.accept()

    async def disconnect(self, close_code):
        del userSocketDict[self.uid]
        # Leave room group

    # Receive message from WebSocket
    async def receive(self, text_data):
        tmp = json.loads(text_data)
        text_data_json = tmp["data"]
        msgType = tmp["type"]
        if msgType == "chat" or msgType == "chat_pic" or msgType == "chat_file": #是聊天消息
            message = text_data_json["message"]
            # 需要信息{"uid","tid","teamname"}
            to_uid = text_data_json.get('to_uid')  # 私聊对象id
            tid = text_data_json.get('tid')  # 群聊团队id
            nowTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 当前时间
            from_uid = int(self.scope["url_route"]["kwargs"]["uid"])
            if tid == "":  # 私聊
                cid = await self.get_cid(from_uid, to_uid)  # 聊天室id
                if cid == -1:  # 若未聊过天创建群聊
                    new_chatroom = Chatroom()
                    await self.chatroom_save(new_chatroom)
                    new_chatuser = ChatUser(cid=new_chatroom.cid, from_uid=from_uid, to_uid=to_uid)
                    await self.chatuser_save(new_chatuser)
                    cid = await self.get_cid(from_uid, to_uid)
                new_record = Record(cid=cid, time=nowTime, content=message, sender=from_uid,uid=to_uid,type=msgType)
                await self.record_save(new_record)
                toUserSocket = userSocketDict.get(to_uid)
                data = {"message": message, "senderId": self.uid, "senderName":self.uname ,"receiverId": to_uid, "teamId": tid, "time": nowTime,
                         "rid": new_record.rid}
                if toUserSocket != None:  # 成员在线
                    await toUserSocket.send(text_data=json.dumps(
                        {
                         "type": msgType,
                         "data": data }))

                await self.send(text_data=json.dumps(
                    {
                     "type": msgType,
                     "data": data}))  # 在自己窗口展示
            if to_uid == "":  # 群聊
                userlist = await self.get_userlist(tid)  # 团队成员列表
                cid = await self.get_cid2(tid)  # 聊天室id
                aite = text_data_json.get('aite')
                ntype = "chat"
                if aite!=None and len(aite)>0 :
                    ntype = "chat_at"
                new_record = Record(cid=cid, time=nowTime, content=message, sender=from_uid, tid=tid, type=ntype)
                await self.record_save(new_record)
                # await self.group_chat(aite, message, new_record, nowTime, tid, userlist)
                if aite!=None and len(aite) >0:
                    for i in aite:
                        if i == -1: # @所有人
                            async for user in userlist:
                                new_aite = Notice(uid=user.uid, rid=new_record.rid, tid=tid, type="chat")
                                await self.notice_save(new_aite)
                                toUserSocket = userSocketDict.get(user.uid)
                                if toUserSocket != None:  # 成员在线
                                    data = {"message": message, "senderId": self.uid, "senderName":self.uname ,"receiverId": "", "teamId": tid,
                                         "time": nowTime,
                                         "rid": new_record.rid}
                                    await toUserSocket.send(text_data=json.dumps(
                                        {
                                         "type": "chat_aite",
                                         "data":data}))
                        else:
                            new_aite = Notice(uid=i, rid=new_record.rid, tid=tid, type="chat")
                            await self.notice_save(new_aite)
                            async for user in userlist:
                                toUserSocket = userSocketDict.get(user.uid)
                                if toUserSocket != None:  # 成员在线
                                    data = {"message": message, "senderId": self.uid, "senderName":self.uname ,"receiverId": "", "teamId": tid,
                                             "time": nowTime,
                                             "rid": new_record.rid}
                                    if user.uid != i:
                                        await toUserSocket.send(text_data=json.dumps(
                                            {
                                             "type": msgType,
                                             "data":data}))
                                    if user.uid == i:
                                        await toUserSocket.send(text_data=json.dumps(
                                            {
                                             "type": "chat_aite",
                                             "data":data}))
                else:  # 该条消息无艾特
                    async for user in userlist:
                        data = {"message": message, "senderId": self.uid, "senderName":self.uname ,"receiverId": "", "teamId": tid,
                                "time": nowTime,
                                "rid": new_record.rid}
                        toUserSocket = userSocketDict.get(user.uid)
                        if toUserSocket != None:  # 成员在线
                            await toUserSocket.send(text_data=json.dumps(
                                {
                                 "type": msgType,
                                 "data":data}))



    @database_sync_to_async
    def get_cid(self, from_uid, to_uid):
        chatroom1 = ChatUser.objects.filter(Q(from_uid=from_uid) & Q(to_uid=to_uid))
        chatroom2 = ChatUser.objects.filter(Q(from_uid=to_uid) & Q(to_uid=from_uid))
        if chatroom1.exists():
            cid = chatroom1[0].cid
        elif chatroom2.exists():
            cid = chatroom2[0].cid
        else:
            cid = -1
        return cid

    @database_sync_to_async
    def get_userlist(self, tid):
        return User_team.objects.filter(tid=tid)

    @database_sync_to_async
    def get_cid2(self, tid):
        return ChatUser.objects.get(tid=tid).cid

    @database_sync_to_async
    def record_save(self, new_record):
        new_record.save()

    @database_sync_to_async
    def chatroom_save(self, chatroom):
        chatroom.save()

    @database_sync_to_async
    def chatuser_save(self, chatuser):
        chatuser.save()

    @database_sync_to_async
    def notice_save(self, notice):
        notice.save()

    @database_sync_to_async
    def get_username(self,uid):
        user = User.objects.get(uid=uid)
        return user.username