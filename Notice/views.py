from Tools.LoginCheck import loginCheck
from django.http import JsonResponse
from models import Notice
import json

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

