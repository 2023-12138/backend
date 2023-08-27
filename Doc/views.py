import datetime
import json
from Tools.LoginCheck import loginCheck,asyncLoginCheck
from asgiref.sync import sync_to_async,async_to_sync
from channels.db import database_sync_to_async
from Chat.consumers import userSocketDict
from django.db.models import Q
from django.http import JsonResponse
from django.forms.models import model_to_dict
from Tools.MakeToken import make_token
from Chat.consumers import userSocketDict
from Doc.models import *
from User.models import *
from Notice.models import  *

@loginCheck
def createDoc(request): #创建文档
    json_str = request.body
    json_obj = json.loads(json_str)
    docname = json_obj.get("docname")
    pid = json_obj.get("pid")
    if Doc.objects.filter(Q(docname=docname)&Q(pid=pid)&Q(is_active=True)).exists():
        return JsonResponse({'code': 400, 'message': '文档名重复', 'data': {}})
    else:
        doc = Doc(docname=docname,pid=pid)
        try:
            doc.save()
            return JsonResponse({'code': 200, 'message': '创建成功', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'message': '服务器异常', 'data': {}})


@loginCheck
def delDoc(request): #删除文档
    json_str = request.body
    json_obj = json.loads(json_str)
    docname = json_obj.get("docname")
    pid = json_obj.get("pid")
    if not Doc.objects.filter(Q(docname=docname) & Q(pid=pid)&Q(is_active=True)).exists():
        return JsonResponse({'code': 400, 'message': '该文档不存在', 'data': {}})
    else:
        doc = Doc.objects.get(Q(docname=docname) & Q(pid=pid))
        doc.is_active = False
        try:
            doc.save()
            return JsonResponse({'code': 200, 'message': '删除成功', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'message': '服务器异常', 'data': {}})

@loginCheck
def renameDoc(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    oldname = json_obj.get("oldname")
    newname = json_obj.get("newname")
    pid = json_obj.get("pid")
    if not Doc.objects.filter(Q(docname=oldname) & Q(pid=pid)&Q(is_active=True)).exists():
        return JsonResponse({'code': 400, 'message': '该文档不存在', 'data': {}})
    elif Doc.objects.filter(Q(docname=newname) & Q(pid=pid)&Q(is_active=True)).exists():
        return JsonResponse({'code': 400, 'message': '名称重复', 'data': {}})
    else:
        doc = Doc.objects.get(Q(docname=oldname) & Q(pid=pid)&Q(is_active=True))
        doc.docname = newname
        try:
            doc.save()
            return JsonResponse({'code': 200, 'message': '修改成功', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'message': '服务器异常', 'data': {}})

@loginCheck
def getDoc(request): #获取文档
    json_str = request.body
    json_obj = json.loads(json_str)
    pid = json_obj.get("pid")
    docList = Doc.objects.filter(Q(pid=pid)&Q(is_active=True))
    data = []
    for obj in docList:
        content = DocContent.objects.get(docId=obj.docId) #目前是只能拿最新的文档内容
        data.append({"docname":obj.docname,"content":content})
    return JsonResponse({'code': 200, 'message': '获取文档成功', 'data': {"doclist":data}})

@loginCheck
def saveDoc(request): #保存文档
    json_str = request.body
    json_obj = json.loads(json_str)
    pid = json_obj.get("pid")
    docname = json_obj.get("docname")
    text = json_obj.get("text")
    nowTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 当前时间
    doc = Doc.objects.get(Q(pid=pid) & Q(docname=docname))
    if DocContent.objects.filter(docId=doc.docId).exists(): #不是第一次
        content = DocContent.objects.get(Q(docId=doc.docId))
        content.docContent = text
        content.saveTime = nowTime
        try:
            content.save()
            return JsonResponse({'code': 200, 'message': '保存成功', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'message': '服务器异常', 'data': {}})
    else : #第一次
        content = DocContent(docId=doc.docId,saveTime=nowTime)
        try:
            content.save()
            return JsonResponse({'code': 200, 'message': '保存成功', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'message': '服务器异常', 'data': {}})

async def docAite(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    aite = json_obj.get('aite') #被@的成员uid
    docname = json_obj.get('docname')
    pid = json_obj.get("pid")
    doc = await get_doc(pid,docname)
    userSocket = userSocketDict.get(aite)
    notice = Notice(uid=aite,rid=-1,docId=doc.docId,type="doc")
    await  notice_save(notice)
    if userSocket != None:
        await userSocket.send(text_data=json.dumps(
            {"message": "", "senderId": "", "receiverId": "", "teamId": "", "time": "",
             "type": "doc_aite", "rid": ""}))

    return JsonResponse({'code': 200, 'message': "文档@发送成功", "data": {}})

def makeLink(request): #生成链接
    json_str = request.body
    json_obj = json.loads(json_str)
    identity=json_obj.get("identity")
    docId = json_obj.get("docId") #文档编号
    user = User(username="xxx",password="xxx",name="xxx",identity=identity)
    try:
        user.save()
        token = make_token(user.uid)
        link = "http://127.0.0.1:8000?token="+str(token)+"&docId="+str(docId)
        return JsonResponse({'code': 200, 'message': '链接生成成功', 'data': {'link':link}})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': '服务器异常', 'data': {}})

@database_sync_to_async
def get_doc(pid,docname):
    return Doc.objects.get(Q(pid=pid)&Q(docname=docname))

@database_sync_to_async
def notice_save(notice):
    notice.save()