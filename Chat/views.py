from django.shortcuts import render
from Tools.LoginCheck import loginCheck
from django.shortcuts import render
from Chat.models import  *
from Chat.consumers import userSocketDict
from django.db.models import Q
def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

@loginCheck
async def getHistory(request):
    user=request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    tid = json_obj.get('tid') #团队id
    senderId =json_obj.get('senderId') #私聊对象的uid
    uid = user.uid #自己的uid
    userSocket = userSocketDict.get(uid)
    if tid != "": #群消息记录
        cid = ChatUser.objects.get(tid = tid).cid #聊天室id
        recordTmp = Record.objects.filter(cid = cid)#获取该聊天室所有的聊天记录
        sorted(recordTmp,key= lambda x:x.time, reverse=True )#大到小
        for obj in recordTmp:
            await userSocket.send(text_data=json.dumps({"message": obj.content,"senderId":obj.sender,"teamId":tid,"time":obj.time}))
    elif senderId != "": #私聊消息记录
        chatRoom1 = ChatUser.objects.filter(Q(from_uid=uid)&Q(to_uid=senderId))
        chatRoom2 = ChatUser.objects.filter(Q(to_uid=uid) & Q(from_uid=senderId))
        cid = -1
        if chatRoom1.exists():
            cid = chatRoom1[0].cid
        elif chatRoom2.exists():
            cid = chatRoom2[0].cid
        else:
            newChatRoom = Chatroom()
            newChatRoom.save()
            cid = newChatRoom.cid
        recordTmp = Record.objects.filter(cid=cid)  # 获取该聊天室所有的聊天记录
        for obj in recordTmp:
            await userSocket.send(
                text_data=json.dumps({"message": obj.content, "senderId": obj.sender, "teamId": tid, "time": obj.time}))
    return JsonResponse({'code': 400, 'message': "历史记录获取成功", "data":{}})









