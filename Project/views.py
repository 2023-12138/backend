import json
from django.http import JsonResponse
from Tools.LoginCheck import loginCheck
from django.db.models import Q
from Project.models import *
from User.models import User
from django.forms.models import model_to_dict
from Doc.views import *
from File.models import  *

@loginCheck
def createProject(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    project_name = json_obj.get('project_name')
    project_inform = json_obj.get('project_inform')
    tid = json_obj.get('tid')
    uid = user.uid
    new_project = Project(project_name=project_name, project_inform=project_inform, tid=tid, uid=uid)
    try:
        new_project.save()
    except:
        return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})
    groupid= createGroup(tid)
    new_project.groupid=groupid
    try:
        new_project.save()
    except:
        return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})
    newFile = File(filename=project_name, pid = new_project.pid,father=-1,depth=0,type=0)
    try:
        newFile.save()
    except:
        return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})
    return JsonResponse({'code': 200, 'message': '项目创建成功', 'data': {'pid': new_project.pid}})


@loginCheck
def deleteProject(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    pid = json_obj.get('pid')  # 项目id
    tid = json_obj.get('tid')  # 所属团队
    if Project.objects.filter(Q(pid=pid) & Q(tid=tid) & Q(is_active=True)).exists():
        data = Project.objects.get(Q(pid=pid) & Q(tid=tid))
    else:
        JsonResponse({'code': 400, 'message': '没有符合条件的项目', 'data': {}})
    try:
        data.is_active = 0
        data.save()
    except:
        return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})
    return JsonResponse({'code': 200, 'message': '项目删除成功', 'data': {}})


@loginCheck
def recoverProject(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    pid = json_obj.get('pid')  # 项目id
    tid = json_obj.get('tid')  # 所属团队
    if Project.objects.filter(Q(pid=pid) & Q(tid=tid) & Q(is_active=False)).exists():
        data = Project.objects.get(Q(pid=pid) & Q(tid=tid) & Q(is_active=False))
    else:
        JsonResponse({'code': 400, 'message': '没有符合条件的项目', 'data': {}})
    try:
        data.is_active = 1
        data.save()
    except:
        return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})
    return JsonResponse({'code': 200, 'message': '项目恢复成功', 'data': {}})


@loginCheck
def renameProject(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    pid = json_obj.get('pid')
    project_name = json_obj.get('project_name')
    if Project.objects.filter(Q(pid=pid) & Q(is_active=True)).exists():
        data = Project.objects.get(Q(pid=pid) & Q(is_active=True))
    else:
        return JsonResponse({'code': 400, 'message': '无该项目id对应的项目', 'data': {}})
    try:
        data.project_name = project_name
        data.save()
    except:
        return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})
    return JsonResponse({'code': 200, 'message': '项目重命名成功', 'data': {}})


@loginCheck
def renameProjectInform(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    pid = json_obj.get('pid')
    project_inform = json_obj.get('project_inform')
    if Project.objects.filter(Q(pid=pid) & Q(is_active=True)).exists():
        data = Project.objects.get(Q(pid=pid) & Q(is_active=True))
    else:
        return JsonResponse({'code': 400, 'message': '无该项目id对应的项目', 'data': {}})
    try:
        data.project_inform = project_inform
        data.save()
    except:
        return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})
    return JsonResponse({'code': 200, 'message': '项目描述重命名成功', 'data': {}})


@loginCheck
def getProject(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    pid = json_obj.get('pid')
    if Project.objects.filter(Q(pid=pid) & Q(is_active=True)).exists():
        data = Project.objects.get(Q(pid=pid) & Q(is_active=True))
    else:
        return JsonResponse({'code': 400, 'message': '无该项目id对应的项目', 'data': {}})
    return JsonResponse({'code': 200, 'message': "项目获取成功", "data": {'project': model_to_dict(data)}})


@loginCheck
def viewProject(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    tid = json_obj.get('tid')
    projectlist = Project.objects.filter(Q(tid=tid) & Q(is_active=True))
    projects = []
    for project in projectlist:
        data = {}
        user = User.objects.filter(Q(uid=project.uid) & Q(is_active=True)).first()
        username = user.name
        data = model_to_dict(project)
        data['username'] = username
        projects.append(data)
    return JsonResponse({'code': 200, 'message': '查询成功', 'data': {'projectlist': projects}})

@loginCheck
def searchProject(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    tid = json_obj.get('tid')
    key = json_obj.get('key')
    project_list = Project.objects.filter(Q(tid=tid) & Q(project_name__icontains=key))
    projects = []
    for project in project_list:
        data = {}
        data = model_to_dict(project)
        projects.append(data)
    return JsonResponse({'code': 200, 'message': '搜索成功', 'data': {'project_list': projects}})

@loginCheck
def copyProject(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    pid = json_obj.get('pid')
    try:
        project = Project.objects.filter(Q(pid=pid)).first()
        new_project = Project(project_name=project.project_name + "-副本", project_inform=project.project_inform,
                              tid=project.tid, uid=user.uid)
        new_project.groupid = createGroup(new_project.tid)
        new_project.save()  # 保存项目
        new_pid = new_project.pid
        prototype_list = Prototype.objects.filter(Q(pid=pid))
        for prototype in prototype_list:
            new_prototype = Prototype(pid=new_pid, protoname=prototype.protoname)
            new_prototype.save()
            protoinfo_list = Protoinfo.objects.filter(Q(proto_info_id=prototype.protoid))
            for protoinfo in protoinfo_list:
                new_protoinfo = Protoinfo(proto_info_id=new_prototype.protoid, info=protoinfo.info)
                new_protoinfo.save()  # 保存原型
        doc_list = Doc.objects.filter(Q(pid=pid))
        for doc in doc_list:
            new_padid = myPad.createGroupPad(new_project.groupid, doc.docname).get('padID')
            new_doc = Doc(pid=new_pid, docname=doc.docname, padid=new_padid)
            myPad.copyPad(new_padid, doc.padid, True)
            new_doc.save()  # 保存文档
    except:
        return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})
    return JsonResponse({'code': 200, 'message': '项目复制成功', 'data': {}})

def createProto(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    pid = json_obj.get("pid")
    protoname = json_obj.get("protoname")
    prototype = Prototype(pid=pid,protoname=protoname)
    try:
        prototype.save()
        return JsonResponse({'code': 400, 'message': '创建成功', 'data': {}})
    except Exception as e:
        print(e.args[0])
        return JsonResponse({'code': 200, 'message': '创建失败', 'data': {}})

@loginCheck
def saveInfo(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    protoid = json_obj.get("protoid")
    style  = json_obj.get("style")
    data = json_obj.get("data")
    info = {"style":style,"data":data}
    if Protoinfo.objects.filter(proto_info_id = protoid).exists():
        protoinfo = Protoinfo.objects.get(proto_info_id=protoid)
        protoinfo.info = info
    else:
        protoinfo = Protoinfo(proto_info_id=protoid,info=info)
    try:
        protoinfo.save()
        return JsonResponse({'code': 200, 'message': '保存成功', 'data': {}})
    except Exception as e:
        return JsonResponse({'code': 400, 'message': '保存失败', 'data': {}})

@loginCheck
def getProto(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    pid = json_obj.get("pid")
    protoList = Prototype.objects.filter(pid = pid)
    protolist = []
    for obj in protoList:
        protolist.append({"protoid":obj.protoid,"protoname":obj.protoname})
    return JsonResponse({'code': 200, 'message': '返回成功', 'data': {"protolist":protolist}})

@loginCheck
def getProtoInfo(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    protoid = json_obj.get("protoid")
    protoinfo = Protoinfo.objects.get(proto_info_id=protoid)
    data = protoinfo.info
    return JsonResponse({'code': 200, 'message': '返回成功', 'data': {"info": data}})
