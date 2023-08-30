from django.shortcuts import render
from Tools.LoginCheck import loginCheck
from File.models import *
from django.db.models import Q
import json
@loginCheck
def createdir(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    dirname = json_obj.get("dirname")
    pid = json_obj.get("pid")
    faFile = File.objects.get(Q(pid = pid)&Q(father= -1))
    newFile = File(filename=dirname, pid=pid, father=faFile.fileID, depth=1, type=0)
    try:
        newFile.save()
        return JsonResponse({'code': 200, 'message': '文件夹创建成功', 'data': {"fileid":newFile.fileID}})
    except:
        return JsonResponse({'code': 400, 'message': '数据库保存失败', 'data': {}})

