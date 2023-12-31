import json
from django.http import JsonResponse
from django.db.models import Q
from Notice.models import *
from Tools.LoginCheck import loginCheck
from django.forms.models import model_to_dict
from Doc.models import *
from  Team.models import *

@loginCheck
def allRead(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    type = json_obj.get("type")
    noticeList = Notice.objects.filter(Q(uid=user.uid) & Q(is_active=True) & Q(read=0) & Q(type=type))
    try:
        for obj in noticeList:
            obj.read = 1  # 修改为已读
            obj.save()
        return JsonResponse({'code': 200, 'message': "修改成功", 'data': {}})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': "服务器异常", 'data': {}})


@loginCheck
def oneRead(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    nid = json_obj.get("nid")
    notice = Notice.objects.get(noticeId=nid)
    try:
        notice.read = 1  # 修改为已读
        notice.save()
        return JsonResponse({'code': 200, 'message': "修改成功", 'data': {}})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': "服务器异常", 'data': {}})


@loginCheck
def allDelete(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    type = json_obj.get("type")  # 删除文档@还是群通知@
    kind = json_obj.get("kind")  # "all"代表全部删除,"read"代表已读删除
    noticeList = []
    if kind == "all":
        noticeList = Notice.objects.filter(Q(uid=user.uid) & Q(is_active=True) & Q(type=type))
    else:
        noticeList = Notice.objects.filter(Q(uid=user.uid) & Q(is_active=True) & Q(type=type) & Q(read=1))
    try:
        for obj in noticeList:
            obj.is_active = False  # 修改为删除
            obj.save()
        return JsonResponse({'code': 200, 'message': "修改成功", 'data': {}})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': "服务器异常", 'data': {}})


@loginCheck
def oneDelete(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    nid = json_obj.get("nid")
    notice = Notice.objects.get(noticeId=nid)
    try:
        notice.is_active = False
        notice.save()
        return JsonResponse({'code': 200, 'message': "修改成功", 'data': {}})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': "服务器异常", 'data': {}})


@loginCheck
def getNotice(request):  # 返回群聊通知列表
    json_str = request.body
    json_obj = json.loads(json_str)
    user = request.myUser
    uid = user.uid
    type = json_obj.get("type")
    notices = Notice.objects.filter(Q(uid=uid) & Q(is_active=True) & Q(type=type))
    notice_list = []
    for notice in notices:
        notice_dic = model_to_dict(notice)
        name = ""
        if notice.docId :
            name = Doc.objects.get(docId=notice.docId).docname
            pid = Doc.objects.get(docId=notice.docId).pid
            notice_dic['pid'] = pid
        else:
            name = Team.objects.get(tid=notice.tid).teamname
        notice_dic['name'] = name
        notice_list.append(notice_dic)

    return JsonResponse({'code': 200, 'message': "通知获取成功", "data": {'notice_list': notice_list}})


@loginCheck
def haveRead(request):  # 某条消息已读
    json_str = request.body
    json_obj = json.loads(json_str)
    user = request.myUser
    rid = json_obj.get("rid")
    uid = request.myUser.uid
    notice = Notice.objects.get(Q(rid=rid)&Q(uid=uid))
    notice.read = 1  # 已读
    notice.save()
    return JsonResponse({'code': 200, 'message': "消息已读", "data": {}})
