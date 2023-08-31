from django.shortcuts import render
from django.http import JsonResponse
from Tools.LoginCheck import loginCheck
from File.models import *
from django.db.models import Q
from django.forms.models import model_to_dict
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

@loginCheck
def getallFiles(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    pid = json_obj.get('pid')
    fileList = File.objects.filter(pid=pid)
    filelist = []
    for obj in fileList:
        filelist.append(model_to_dict(obj))
    return JsonResponse({'code': 200, 'message': '所有文件获取成功', 'data': {"filelist": filelist}})

@loginCheck
def getProjectFiles(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    pid = json_obj.get('pid')
    fileList = File.objects.filter(Q(pid=pid) & Q(depth=1))
    filelist = []
    for obj in fileList:
        filelist.append(model_to_dict(obj))
    return JsonResponse({'code': 200, 'message': '项目子文件获取成功', 'data': {"filelist": filelist}})
@loginCheck
def getFolderFiles(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    fileID = json_obj.get('fileID')
    fileList = File.objects.filter(Q(father=fileID) & Q(depth=2))
    filelist = []
    for obj in fileList:
        filelist.append(model_to_dict(obj))
    return JsonResponse({'code': 200, 'message': '文件夹子文件获取成功', 'data': {"filelist": filelist}})
