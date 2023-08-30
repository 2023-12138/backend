from django.shortcuts import render
from Tools.LoginCheck import loginCheck
import json
# Create your views here.
@loginCheck
def createdir(request):
    json_str = request.body
    json_obj = json.loads(json_str)