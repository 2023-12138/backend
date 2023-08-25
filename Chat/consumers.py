# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

userSocketDict = {}

class ChatConsumer(WebsocketConsumer):
    uid = -1
    def connect(self):
        self.uid = int(self.scope["url_route"]["kwargs"]["uid"])
        userSocketDict[self.uid] = self
        self.accept()

    def disconnect(self, close_code):
        del userSocketDict[self.uid]

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"] #要发送的信息
        to = int(text_data_json["to"]) #要发送给的成员id或者群id
        toUserSocket = userSocketDict.get(to)
        toUserSocket.send(text_data=json.dumps({"message": message}))
        self.send(text_data=json.dumps({"message": message}))