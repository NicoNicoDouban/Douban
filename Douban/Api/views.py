from django.template.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render
from Users.models import Users
from Users.models import Books
from Users.models import Articles
from DouBan_pages import func
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
import json

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
            try:
                user=Users.objects.get(email=text)
            except:
                return False
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

    def createUser(request):
        if request.method!="POST":
            resp = {'rsNum': 0}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        #try:
        text=request.POST.get("text")
        pwd = request.POST.get("pwd")
        type = request.POST.get("type")

        if not users().judgeExist(type=type, text=text):
            user=Users.objects.create()
            if type=="email":
                user.email=text
            user.password=pwd
            user.save()
            resp = {'rsNum': 1}
        else:
            resp = {'rsNum': -1}
    #except:
     #   resp = {'rsNum': 0}
        return HttpResponse(json.dumps(resp), content_type="application/json")



    def login(request):
        text=request.GET.get("text")
        pwd=request.GET.get("pwd")
        type=request.GET.get("type")
        if type=="email":
            user = authenticate(username=text)
            if user is not None:
                user = authenticate(username=text, password=pwd)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        resp = {'rsNum':1}
                    else:
                        resp = {'rsNum': 0}
                else:
                    resp = {'rsNum': -2}
            else:
                resp = {'rsNum': -1}
            return HttpResponse(json.dumps(resp), content_type="application/json")



class search(View):
    #获取热门文章
    def getHotArtcles(self):
        search=func.Search(1,5)
        result=search.good_article()
        #result=search.book_search("a","name")
        context=serializers.serialize("json", result["search_result"]["objects"])
        return HttpResponse(context, content_type="application/json")

    #获取热门图书
    def getHotBooks(self):
        search=func.Search(1,5)
        result=search.good_book()
        #result=search.book_search("a","name")
        context=serializers.serialize("json", result["search_result"]["objects"])
        return HttpResponse(context, content_type="application/json")

    '''
    搜索书 
    type 为搜索类型(name author)
    '''
    def bookSearch(self,request):
        searchText=request.GET.get("text")
        search = func.Search(1, 5)
        result = search.book_search(searchText, request.GET.get("type"))
        context = serializers.serialize("json", result["search_result"]["objects"])
        return HttpResponse(context, content_type="application/json")

    '''
        搜索文章
        type 为搜索类型(title， text，writer)
    '''
    def artclesSearch(self,request):
        searchText=request.GET.get("text")
        search = func.Search(1, 5)
        result = search.article_search(searchText, request.GET.get("type"))
        context = serializers.serialize("json", result["search_result"]["objects"])
        return HttpResponse(context, content_type="application/json")


    def getDetails(request):
        #search = func.Search(1, 5)
        if request.GET.get("type")=="book":
            result=Books.objects.filter(id=request.GET.get("id"))
        elif request.GET.get("type")=="artcles":
            result = Articles.objects.filter(id=request.GET.get("id"))
        context = serializers.serialize("json",result)
        return HttpResponse(context, content_type="application/json")

