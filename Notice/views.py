import  json
from django.http import JsonResponse
from django.db.models import Q
from Notice.models import *
from Tools.LoginCheck import loginCheck

@loginCheck
def allRead(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    type = json_obj.get("type")
    noticeList  = Notice.objects.filter(Q(uid=user.uid)&Q(is_active=True)&Q(read=True)&Q(type=type))
    try:
        for obj in noticeList:
            obj.read = False #修改为已读
            obj.save()
        return JsonResponse({'code': 200, 'message': "修改成功", 'data': {}})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': "服务器异常", 'data': {}})

@loginCheck
def oneRead(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    nid = json_obj.get("nid")
    notice = Notice.objects.get(nid=nid)
    try:
        notice.read = False #修改为已读
        notice.save()
        return JsonResponse({'code': 200, 'message': "修改成功", 'data': {}})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': "服务器异常", 'data': {}})

@loginCheck
def allDelete(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    type = json_obj.get("type")
    noticeList = Notice.objects.filter(Q(uid=user.uid) & Q(is_active=True) & Q(type=type))
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
    notice = Notice.objects.get(nid=nid)
    try:
        notice.is_active = False
        notice.save()
        return JsonResponse({'code': 200, 'message': "修改成功", 'data': {}})
    except Exception  as e:
        return JsonResponse({'code': 500, 'message': "服务器异常", 'data': {}})

@loginCheck
def getNotice(request): #返回群聊通知列表
    user = request.myUser
    uid = user.uid
    notices = Notice.objects.filter(uid=uid)
    notice_list = [notice.to_dict() for notice in notices]
    if notice_list:
        return JsonResponse({'code': 200, 'message': "通知获取成功", "data": {'notice_list': notice_list}})
    else:
        return JsonResponse({'code': 201, 'message': "无通知"})

