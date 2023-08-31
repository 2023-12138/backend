import datetime
import json
import time

import Doc.views
from Tools.LoginCheck import loginCheck, asyncLoginCheck
from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from Chat.consumers import userSocketDict
from django.db.models import Q
from django.http import JsonResponse
from django.forms.models import model_to_dict
from Tools.MakeToken import make_token
from Chat.consumers import userSocketDict
from Doc.models import *
from User.models import *
from Team.models import *
from Notice.models import *
from Project.models import *
from File.models import *
from py_etherpad import EtherpadLiteClient

myPad = EtherpadLiteClient('4c87155dea77eb7c2927025bc807ee87304e5bf06239ba1439c17c1efa2e6c4e',
                           'http://43.138.59.36:10010/api')


def createGroup(tid):
    groupid = myPad.createGroup().get('groupID')
    userlist = User_team.objects.filter(Q(tid=tid) & Q(is_active=True))
    for user_data in userlist:
        try:
            user = User.objects.get(Q(uid=user_data.uid) & Q(is_active=True))
        except:
            return JsonResponse({'code': 400, 'message': '未找到对应用户', 'data': {}})
        authorid = user.authorid
        createSession(groupid, authorid)
    return groupid


def createAuthor(uid):
    if User.objects.filter(Q(uid=uid) & Q(is_active=True)):
        username = User.objects.get(Q(uid=uid) & Q(is_active=True)).username
    else:
        return JsonResponse({'code': 400, 'message': '未找到对应用户', 'data': {}})
    authorid = myPad.createAuthor(username).get('authorID')
    return authorid


def createSession(groupid, authorid):
    sessionid = myPad.createSession(groupid, authorid, 9999999999).get('sessionID')
    data = Session(groupid=groupid, authorid=authorid, sessionid=sessionid)
    try:
        data.save()
    except:
        return JsonResponse({'code': 400, 'message': '数据库操作失败', 'data': {}})
    return sessionid


def deleteSession(sessionid):
    myPad.deleteSession(sessionid)


@loginCheck
def createDoc(request):  # 创建文档     #处理同名文件
    user=request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    docname = json_obj.get('docname')
    pid = json_obj.get('pid')
    depth = json_obj.get('depth')
    father = json_obj.get("father")
    default=json_obj.get('default')
    if Project.objects.filter(Q(pid=pid) & Q(is_active=True)):
        project = Project.objects.get(Q(pid=pid) & Q(is_active=True))
    else:
        return JsonResponse({'code': 400, 'message': '该项目不存在', 'data': {}})
    if File.objects.filter(Q(pid=pid)&Q(father=father)&Q(filename=docname)):
        return JsonResponse({'code': 400, 'message': '文件名重复', 'data': {}})
    groupid = project.groupid
    try:
        padid = myPad.createGroupPad(groupid, docname).get('padID')
    except Exception as e:
        return JsonResponse({'code': 400, 'message': e.args[0], 'data': {}})
    newDoc = Doc(pid=pid, padid=padid, docname=docname)
    try:
        newDoc.save()
    except:
        return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})
    newFile = File(filename=docname, pid=pid, father=father, depth=depth, type=1,docID=newDoc.docId)
    try:
        newFile.save()
    except:
        return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})
    groupid=project.groupid
    sessionid=Session.objects.get(Q(groupid=groupid)&Q(authorid=user.authorid)).sessionid
    return JsonResponse({'code': 200, 'message': '文档创建成功', 'data': {'url':'http://43.138.59.36:10010/p/'+newDoc.padid,'session':sessionid}})

@loginCheck
def openDoc(request):
    user=request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    #docname = json_obj.get('docname')
    docid=json_obj.get('docid')
    doc=Doc.objects.get(docid=docid)
    pid=doc.pid
    if Project.objects.filter(Q(pid=pid) & Q(is_active=True)).exists():
        project = Project.objects.get(Q(pid=pid) & Q(is_active=True))
    else:
        return JsonResponse({'code': 400, 'message': '该项目不存在', 'data': {}})
    groupid = project.groupid
    sessionid = Session.objects.get(Q(groupid=groupid) & Q(authorid=user.authorid))
    return JsonResponse({'code': 200, 'message': '文档打开成功', 'data': {'url':'http://43.138.59.36:10010/p/'+doc.padid,'session':sessionid}})

@loginCheck
def delDoc(request):  # 删除文档
    json_str = request.body
    json_obj = json.loads(json_str)
    docid = json_obj.get("docid")
    if not Doc.objects.filter(Q(docid=docid) & Q(is_active=True)).exists():
        return JsonResponse({'code': 400, 'message': '该文档不存在', 'data': {}})
    else:
        doc = Doc.objects.get(docid=docid)
        doc.is_active = False
        try:
            doc.save()
            return JsonResponse({'code': 200, 'message': '删除成功', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'message': '服务器异常', 'data': {}})

def getAuthor(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    padid=json_obj.get('padid')
    userlist=[]
    doc=Doc.objects.get(padid=padid)
    pid=doc.pid
    project=Project.objects.get(Q(pid=pid)&Q(is_active=True))
    tid=project.tid
    userlists=User_team.objects.filter(Q(tid=tid)&Q(is_active=True))
    for i in userlists:
        user=User.objects.get(uid=i.uid)
        userdata={}
        userdata['uid']=user.uid
        userdata['username']=user.username
        userlist.append(userdata)
    return JsonResponse({'code':200,'message':'查询用户成功','data':{'userlist':userlist}})
# @loginCheck
# def saveDoc(request):
#     json_str = request.body
#     json_obj = json.loads(json_str)
#     docid = json_obj.get("docid")
#     doc = Doc.objects.get(docid=docid)
#     padid = doc.padid
#     try:
#         myPad.saveRevision(padid)
#     except Exception as e:
#         return JsonResponse({'code': 400, 'message': e.args[0], 'data': {}})


# @loginCheck
# def getDoc(request):  # 获取文档内容
#     json_str = request.body
#     json_obj = json.loads(json_str)
#     docid = json_obj.get("docid")
#     doc = Doc.objects.get(docid=docid)
#     padid = doc.padid


@loginCheck
def viewDoc(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    pid = json_obj.get('pid')
    docList = Doc.objects.filter(Q(pid=pid) & Q(is_active=True))
    doclist = []
    for doc in docList:
        data = {}
        data = model_to_dict(doc)
        doclist.append(data)
    return JsonResponse({'code': 200, 'message': "查询文档列表成功", 'data': {'doclist': doclist}})


@loginCheck
def saveDoc(request):  # 保存文档
    json_str = request.body
    json_obj = json.loads(json_str)
    # pid = json_obj.get("pid")
    # docname = json_obj.get("docname")
    docid = json_obj.get("docid")
    text = json_obj.get("text")
    nowTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 当前时间
    doc = Doc.objects.get(docId=docid)
    new_content = DocContent(docId=doc.docId, docContent=text, saveTime=nowTime)
    try:
        new_content.save()
        return JsonResponse({'code': 200, 'message': '保存成功', 'data': {}})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': '服务器异常', 'data': {}})
    # if DocContent.objects.filter(docId=doc.docId).exists(): #不是第一次
    #     content = DocContent.objects.get(Q(docId=doc.docId))
    #     content.docContent = text
    #     content.saveTime = nowTime
    #     try:
    #         content.save()
    #         return JsonResponse({'code': 200, 'message': '保存成功', 'data': {}})
    #     except Exception as e:
    #         return JsonResponse({'code': 500, 'message': '服务器异常', 'data': {}})
    # else : #第一次
    #     content = DocContent(docId=doc.docId,saveTime=nowTime)
    #     try:
    #         content.save()
    #         return JsonResponse({'code': 200, 'message': '保存成功', 'data': {}})
    #     except Exception as e:
    #         return JsonResponse({'code': 500, 'message': '服务器异常', 'data': {}})


async def docAite(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj.get('username')  # 被@的成员username
    user=await get_user(username)
    padid = json_obj.get("padid")
    doc = await get_doc(padid)
    userSocket = userSocketDict.get(user.uid)
    notice = Notice(uid=user.uid, rid=-1, docId=doc.docId, type="doc")
    await  notice_save(notice)
    if userSocket != None:
        data = {  "message": "", "senderId": "", "receiverId": "", "teamId": "", "time": ""
             , "rid": ""}
        await userSocket.send(text_data=json.dumps({
            "type":"doc_aite",
            "data": data}
            ))

    return JsonResponse({'code': 200, 'message': "文档@发送成功", "data": {}})


def makeLink(request):  # 生成链接
    json_str = request.body
    json_obj = json.loads(json_str)
    identity = json_obj.get("identity")
    docid = json_obj.get("docid")  # 文档编号
    user = User(username="xxx", password="xxx", name="xxx", identity=identity)
    try:
        user.save()
    except Exception as e:
        return JsonResponse({'code': 500, 'message': '服务器异常', 'data': {}})
    authorid=createAuthor(user.uid)
    doc=Doc.objects.get(Q(docid=docid)&Q(is_active=True))
    padid=doc.padid
    pid=doc.pid
    project=Project.objects.get(Q(pid=pid)&Q(is_active=True))
    groupid=project.groupid
    sessionid=createSession(groupid,authorid)
    if identity=='1':#代表仅查看游客
        padid=myPad.getReadOnlyID(padid).get('readOnlyID')
    link = "http://43.138.59.36:10010/p/&padID=" + padid + "&sessionID=" + sessionid
    return JsonResponse({'code':200,'message':'生成链接成功','data':{'url':link}})





@database_sync_to_async
def get_doc(padid):
    return Doc.objects.get(padid=padid)


@database_sync_to_async
def notice_save(notice):
    notice.save()
@database_sync_to_async
def get_user(username):
    return User.objects.get(username=username)