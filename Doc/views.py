import datetime
import json
import time
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

myPad = EtherpadLiteClient('08ed388c84d03eebf6745356d5e61534843cbf75fb48ef5e8628c4b24a9150a1',
                           'http://43.138.59.36:10010/api')


@loginCheck
def createGroup(pid):
    groupid = myPad.createGroup().get('groupID')
    userlist = User_team.objects.filter(Q(pid=pid) & Q(is_active=True))
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


@loginCheck
def createSession(groupid, authorid):
    sessionid = myPad.createSession(groupid, authorid, 9999999999).get('sessionID')
    data = Session(groupid=groupid, authorid=authorid, sessionid=sessionid)
    try:
        data.save()
    except:
        return JsonResponse({'code': 400, 'message': '数据库操作失败', 'data': {}})


@loginCheck
def deleteSession(sessionid):
    myPad.deleteSession(sessionid)


@loginCheck
def createDoc(request):  # 创建文档
    json_str = request.body
    json_obj = json.loads(json_str)
    docname = json_obj.get('docname')
    pid = json_obj.get('pid')
    depth = json_obj.get('depth')
    father = json_obj.get("father")
    if Project.objects.filter(Q(pid=pid) & Q(is_active=True)):
        project = Project.objects.get(Q(pid=pid) & Q(is_active=True))
    else:
        return JsonResponse({'code': 400, 'message': '该项目不存在', 'data': {}})
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
    return JsonResponse({'code': 200, 'message': '文档创建成功', 'data': {}})


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
    aite = json_obj.get('aite')  # 被@的成员uid
    # docname = json_obj.get('docname')
    # pid = json_obj.get("pid")
    docid = json_obj.get("docid")
    doc = await get_doc(docid)
    userSocket = userSocketDict.get(aite)
    notice = Notice(uid=aite, rid=-1, docId=doc.docId, type="doc")
    await  notice_save(notice)
    if userSocket != None:
        await userSocket.send(text_data=json.dumps(
            {"message": "", "senderId": "", "receiverId": "", "teamId": "", "time": "",
             "type": "doc_aite", "rid": ""}))

    return JsonResponse({'code': 200, 'message': "文档@发送成功", "data": {}})


def makeLink(request):  # 生成链接
    json_str = request.body
    json_obj = json.loads(json_str)
    identity = json_obj.get("identity")
    docId = json_obj.get("docId")  # 文档编号
    user = User(username="xxx", password="xxx", name="xxx", identity=identity)
    try:
        user.save()
        token = make_token(user.uid)
        link = "http://127.0.0.1:8000?token=" + str(token) + "&docId=" + str(docId)
        return JsonResponse({'code': 200, 'message': '链接生成成功', 'data': {'link': link}})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': '服务器异常', 'data': {}})


@database_sync_to_async
def get_doc(docid):
    return Doc.objects.get(docId=docid)


@database_sync_to_async
def notice_save(notice):
    notice.save()
