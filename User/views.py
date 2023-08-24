import  json
import  re
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from User.models import *
from Tools.EmailCheck import *
#注册
def userRegister(request):
    json_str = request.body #拿到json字符串
    json_obj = json.loads(json_str)  #将json字符串转换为字典对象
    username = json_obj.get('username')
    password = json_obj.get('password')
    confirmPassword = json_obj.get('confirmPassword')
    phone = json_obj.get('phone')
    email = json_obj.get('email')
    name  = json_obj.get('name')
    captcha = json_obj.get('captcha')
    usernameToString = str(username)
    if password != confirmPassword:
        return JsonResponse({'code': 400, 'message': "两次密码不同", 'data':{}})
    elif not  usernameToString.isalnum():
        return JsonResponse({'code': 400, 'message': "用户名不合法", 'data':{}})
    elif User.objects.filter(Q(username=username) & Q(is_active=True)).exists():
        return JsonResponse({'code': 400, 'message': "用户名已存在", 'data':{}})
    elif not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{5,18}$', password):  # 密码为5-18位字母和数字的组合
        return JsonResponse({'code': 400, 'message': "密码不合法", 'data': {}})
    elif not re.match('^1\d{10}$', phone):
        return JsonResponse({'code': 400, 'message': "手机号不合法", 'data': {}})
    elif User.objects.filter(phone=phone).exists():
        return JsonResponse({'code': 400, 'message': "手机号已存在", 'data': {}})
    elif not re.match('^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', email):
        return JsonResponse({'code': 400, 'message': "邮箱不合法", 'data': {}})
    elif User.objects.filter(email=email).exists():
        return JsonResponse({'code': 400, 'message': "邮箱已被使用", 'data': {}})
    else :
        correctCaptcha = Captcha.objects.get(email=email)
        if correctCaptcha != captcha:
            return JsonResponse({'code': 400, 'message': "验证码错误", 'data': {}})
        else:
            newUser = User(username=username, password=password, phone=phone, email=email, name=name)
            try:
                newUser.save()
                return JsonResponse({'code': 200, 'message': "注册成功", 'data': {}})
            except Exception as e:
                return JsonResponse({'code': 500, 'message': "服务器错误", 'data': {}})

#登录
def userLogin(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj.get('username')  # 获取请求数据
    password = json_obj.get('password')
    if not User.objects.filter(Q(username=username) &Q(is_active = True)).exists():  # 用户名是否存在
        return JsonResponse({'code': 400, 'message': "用户名不存在", 'data': {}})
    else:
        user = User.objects.get(username=username)
    if user.password == password:  # 判断请求的密码是否与数据库存储的密码相同
        token = make_token(user.uid) #成功登录生成token并以字符串的形式返回
        return JsonResponse({'code': 200, 'message': "登录成功",'data':{
            'token' : token
        }})
    #重定向回先前页面
    else:
        return JsonResponse({'code': 400, 'message': "密码错误", 'data': {}})

#发送验证码
def sendCaptcha(email):
    captcha = createCaptacha()
    if Captcha.objects.filter(email = email).exists():
        oldCaptcha = Captcha.objects.get(email)
        oldCaptcha.captcha = captcha
        oldCaptcha.save()
    else:
        newCaptcha = Captcha(email=email,captcha=captcha)
        newCaptcha.save()
    emailCheck(email,captcha)


