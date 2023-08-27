import json
from django.http import JsonResponse
from Tools.LoginCheck import loginCheck
from django.db.models import Q
from Project.models import Project
from django.forms.models import model_to_dict
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
    return JsonResponse({'code': 200, 'message': '项目创建成功', 'data': {'pid': new_project.pid}})

@loginCheck
def deleteProject(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    pid = json_obj.get('pid')  # 项目id
    tid = json_obj.get('tid')  # 所属团队
    data = Project.objects.get(Q(pid=pid) & Q(tid=tid))
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
    data = Project.objects.get(Q(pid=pid) & Q(tid=tid))
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
    data = Project.objects.get(Q(pid=pid))
    try:
        data.project_name = project_name
        data.save()
    except:
        return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})
    return JsonResponse({'code': 200, 'message': '项目重命名成功', 'data': {}})

@loginCheck
def getProject(request):
    user = request.myUser
    json_str = request.body
    json_obj = json.loads(json_str)
    pid = json_obj.get('pid')
    data = Project.objects.get(Q(pid=pid))
    JsonResponse({'code': 200, 'message': "项目获取成功", "data": {'project': data}})

@loginCheck
def viewProject(request):
    user=request.myuser
    json_str = request.body
    json_obj = json.loads(json_str)
    tid=json_obj.get('tid')
    projectlist=Project.objects.filter(tid=tid)
    projects=[]
    for project in projectlist:
        data={}
        data=model_to_dict(project)
        projects.append(data)
    return JsonResponse({'code': 200, 'message': '查询成功', 'data': {'projectlist': projects}})