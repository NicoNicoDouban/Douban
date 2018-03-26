from django.template.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render
from Users.models import Users
from DouBan_pages import func
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout


def test(request):
    return render(request,"index.html")

#对request加csrftoken并返回
def getCsrf(request):
    csrf_tok=csrf(request)
    csrf_token=str(csrf_tok.get("csrf_token"))
    return HttpResponse(csrf_token,content_type="application/json")


def getHotAricles(request):
    result=func.Search.good_article()
    return HttpResponse(result, content_type="application/json")

def toRegiste(request):
    if request.GET.get("type")=="email":
        if users().createUser(text=request.GET.get("text"),pwd=request.GET.get("pwd")):
            return HttpResponse("注册成功", content_type="application/json")
        else:
            return HttpResponse("注册失败", content_type="application/json")
    return HttpResponse("type不对", content_type="application/json")


class users(View):
    def judgeExist(self,type,text):#判断用户是否存在 type为标识类型(email phone)
        if type=="email":
            user=Users.objects.get(email=text)
            if user:
                return True
            else :
                return False
        else:
            return False

    def judgePwd(self,type,text,pwd):#判断用户密码是否正确 type为标识类型(email phone)
        if type=="email":
            user=Users.objects.get(email=text)
            if user.password==pwd:
                return True
            else:
                return False

    def createUser(self,text,pwd,type="email"):
        #try:
            user=Users.objects.create()
            if type=="email":
                user.email=text
            user.password=pwd
            user.save()
            return True
        #except:
         #   return False

    def login(self,text,pwd,type="type"):
        if type=="email":
            user=authenticate()

