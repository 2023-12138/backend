# -*- coding = utf-8 -*-
# @Time: 2023-08-24 15:54
# @Author :张志扬
# @File : LoginCheck.py
# @Software: PyCharm
import  jwt
from django.http import JsonResponse
from Tools.MakeToken import JWT_TOKEN_KEY
from User.models import User
from django.http import HttpResponse
def loginCheck(func):
    def wrap(request,*args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        if not token:
            return JsonResponse({'code': 400, 'message': "请重新登录", 'data': {}})
        try:
            res = jwt.decode(token,JWT_TOKEN_KEY,algorithms='HS256')
        except Exception as e:
            print('jwt decode error is %s'%e)
            return JsonResponse({'code': 400, 'message': "请重新登录", 'data': {}})

        uid = res['uid']
        user  = User.objects.get(uid=uid)
        request.myUser = user
        return func(request,*args,**kwargs)
    return wrap