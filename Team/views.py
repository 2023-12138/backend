from django.shortcuts import render
import json
from django.http import JsonResponse
from Team.models import *
from django.db.models import Q
from django.forms.models import model_to_dict
from Tools import *
from Tools.LoginCheck import loginCheck
from User.models import *

# Create your views here.
@loginCheck
def createTeam(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    teamname = json_obj.get('teamname')
    teaminform = json_obj.get('teaminform')
    teamlist = User_team.objects.filter(Q(uid=user.uid)&Q(is_active=1))
    for data in teamlist:  # 检查有无同名团队
        if Team.objects.get(tid=data.tid).teamname == teamname:
            return JsonResponse({'code': 400, 'message': '已有同名团队', 'data': {}})
    new_team = Team(teamname=teamname, teaminform=teaminform)
    try:
        new_team.save()
    except:
        return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})
    new_data = User_team(uid=user.uid, tid=new_team.tid, status=0)
    try:
        new_data.save()
    except:
        return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})
    return JsonResponse({'code': 200, 'message': '创建团队成功', 'data': {'tid': new_team.tid}})


@loginCheck
def inviteUser(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    tid = json_obj.get('tid')
    uid = json_obj.get('uid')
    data = User_team.objects.get(Q(uid=user.uid) & Q(tid=tid))
    if data.status == '2':  # 判断用户是否有权限邀请
        return JsonResponse({'code': 400, 'message': '用户没有权限邀请成员加入', 'data': {}})
    if User_team.objects.filter(Q(uid=uid) & Q(tid=tid)&Q(is_active=1)).exists():  # 判断被邀请用户是否已加入过该团队
        return JsonResponse({'code': 400, 'message': '该用户已加入团队!', 'data': {}})
    new_data = User_team(uid=uid, tid=tid, status=2)
    try:  # 判断数据操作是否成功
        new_data.save()
    except:
        return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})
    return JsonResponse({'code': 200, 'message': '邀请成功', 'data': {}})


@loginCheck
def viewTeam(request):  # 用户查看当前所属团队
    user = request.myUser
    if not User_team.objects.filter(Q(uid=user.uid)&Q(is_active=1)).exists():
        return JsonResponse({'code': 400, 'message': '用户未加入团队', 'data': {}})
    teamidlist = User_team.objects.filter(Q(uid=user.uid)&Q(is_active=1))
    teamlist = []
    tmp = {}
    for data in teamidlist:
        team = Team.objects.get(tid=data.tid)
        tmp = model_to_dict(team)
        teamlist.append(tmp)
    return JsonResponse({'code': 200, 'message': '查询成功', 'data': {'teamlist': teamlist}})


@loginCheck
def deleteUser(request): #删除用户
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    tid = json_obj.get('tid')
    uid = json_obj.get('uid')
    data = User_team.objects.get(Q(uid=user.uid) & Q(tid=tid))
    if data.status == '2':  # 判断用户是否有权限删除
        return JsonResponse({'code': 400, 'message': '用户没有权限删除成员', 'data': {}})
    data2 = User_team.objects.get(Q(uid=uid) & Q(tid=tid))
    # if data.status==1 and data2.status!=2: # 判断用户是否有权限删除 等级为1的不可互相删除
    #     return JsonResponse({'code': 400, 'message': '用户没有权限删除成员', 'data': {}})
    try:  # 判断数据操作是否成功
        data2.is_active=0
        data2.save()
    except:
        return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})
    return JsonResponse({'code': 200, 'message': '删除用户成功', 'data': {}})


@loginCheck
def addAdmin(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    tid = json_obj.get('tid')
    uid = json_obj.get('uid')
    data = User_team.objects.get(Q(uid=user.uid) & Q(tid=tid)&Q(is_active=1))
    if data.status == '2':
        return JsonResponse({'code': 400, 'message': '用户没有权限添加管理员', 'data': {}})
    data2=User_team.objects.get(Q(uid=uid)&Q(tid=tid)&Q(is_active=1))   #在前端就已经存储了用户角色
    if data2.status=='2':
        return JsonResponse({'code': 400, 'message': '用户已是管理员', 'data': {}})
    data2.status=1
    data2.save()
    return JsonResponse({'code':200,'message':'添加管理员成功','data':{}})

@loginCheck
def removeAdmin(request):
    user=request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    tid = json_obj.get('tid')
    uid = json_obj.get('uid')
    data = User_team.objects.get(Q(uid=user.uid) & Q(tid=tid)&Q(is_active=1))
    if data.status != '0':
        return JsonResponse({'code': 400, 'message': '用户没有权限移除管理员', 'data': {}})
    data2 = User_team.objects.get(Q(uid=uid) & Q(tid=tid)&Q(is_active=1))  # 在前端就已经存储了用户角色
    data2.status = 2
    data2.save()
    return JsonResponse({'code': 200, 'message': '移除管理员成功', 'data': {}})

@loginCheck
def viewUser(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    tid = json_obj.get('tid')
    datalist=User_team.objects.filter(Q(tid=tid)&Q(is_active=1))
    userlist=[]
    datadic={}
    for data in datalist:
        user=User.objects.get(Q(uid=data.uid)&Q(is_active=1))
        datadic=model_to_dict(user)
        datadic['status']=data.status
        userlist.append(datadic)
    return JsonResponse({'code':200,'message':'查询成员成功','data':{'userlist':userlist}})

