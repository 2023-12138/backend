import json
from django.http import JsonResponse
from Tools.LoginCheck import loginCheck
from models import Project

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
