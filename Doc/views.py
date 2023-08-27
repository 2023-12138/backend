import json
from Tools.LoginCheck import loginCheck,asyncLoginCheck
from Chat.consumers import userSocketDict
from django.db.models import Q
from django.http import JsonResponse
from django.forms.models import model_to_dict
from Tools.MakeToken import make_token
from Doc.models import *
from User.models import *

def makeLink(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    status = json_obj.get("status") #权限
    identity=json_obj.get("identity")
    docId = json_obj.get("docId") #文档编号
    user = User(username="xxx",password="xxx",name="xxx",identity=identity)
    try:
        user.save()
        token = make_token(user.uid)
        link = "http://127.0.0.1:8000?token="+str(token)+"&docId="+str(docId)
        return JsonResponse({'code': 200, 'message': '链接生成成功', 'data': {'link':link}})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': '服务器异常', 'data': {}})


