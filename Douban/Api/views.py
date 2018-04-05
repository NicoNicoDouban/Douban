from django.template.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render
from Users import models
from Users.models import Users
from Users.models import Books
from Users.models import Articles
from Users.models import GoodLink
from DouBan_pages import func
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.contrib.auth.hashers import make_password
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import datetime


def test(request):
    return render(request, "index.html")


def test2(request):
    id = request.user.id
    return HttpResponse(json.dumps(id), content_type="application/json")
    if not request.user.is_authenticated():
        return render(request, "index.html")
    else:
        return render(request, "test.html")


@csrf_exempt
def photo(request):
    image = request.FILES.get("photo")
    result = image.size
    return HttpResponse(json.dumps(result), content_type="application/json")


# 对request加csrftoken并返回
def getCsrf(request):
    csrf_tok = csrf(request)
    csrf_token = str(csrf_tok.get("csrf_token"))
    return HttpResponse(csrf_token, content_type="application/json")


def getHotAricles(request):
    result = func.Search.good_article()
    return HttpResponse(result, content_type="application/json")


def toRegiste(request):
    if request.GET.get("type") == "email":
        if users().createUser(text=request.GET.get("text"), pwd=request.GET.get("pwd")):
            return HttpResponse("注册成功", content_type="application/json")
        else:
            return HttpResponse("注册失败", content_type="application/json")
    return HttpResponse("type不对", content_type="application/json")


class users(View):
    def judgeExist(self, type, text):  # 判断用户是否存在 type为标识类型(email phone)
        if type == "email":
            try:
                user = Users.objects.get(email=text)
            except:
                return 0
            if user:
                return 1
            else:
                return 0
        elif type == "id":
            try:
                user = Users.objects.get(id=text)
            except:
                return 0
            if user:
                return 1
            else:
                return 0
        else:
            return 0

    def checkExist(request):
        type = request.POST.get("type")
        text = request.POST.get("text")
        if type == "email":
            try:
                user = Users.objects.get(email=text)
            except:
                return False
            if user:
                return True
            else:
                return False
        else:
            return False

    def judgePwd(self, type, text, pwd):  # 判断用户密码是否正确 type为标识类型(email phone)
        if type == "email":
            user = Users.objects.get(email=text)
            if user.password == pwd:
                return True
            else:
                return False

    def createUser(request):
        if request.method != "POST":
            resp = {'rsNum': 0}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        try:
            text = request.POST.get("text")
            pwd = request.POST.get("pwd")
            type = request.POST.get("type")
            username = request.POST.get("username")
            if not users().judgeExist(type=type, text=text):

                user = Users.objects.create_user(username=username)
                # user=Users.objects.create()
                if type == "email":
                    user.email = text
                    user.username = username
                    user.password = make_password(pwd)
                    user.save()
                    resp = {'rsNum': 1}
                else:
                    resp = {'rsNum': -1}
            else:
                resp = {'rsNum': -1}
        except:
            resp = {'rsNum': 0}
        return HttpResponse(json.dumps(resp), content_type="application/json")

    def login(request):
        text = request.POST.get("text")
        pwd = request.POST.get("pwd")
        type = request.POST.get("type")
        if type == "email":
            user = Users.objects.filter(email=text)
            if len(user):
                user = authenticate(username=text, password=pwd)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        resp = {'rsNum': 1}
                    else:
                        resp = {'rsNum': 0}
                else:
                    resp = {'rsNum': -2}
            else:
                resp = {'rsNum': -1}
            return HttpResponse(json.dumps(resp), content_type="application/json")

    def changePwd(request):
        try:
            id = request.user.id
            oldPwd = request.POST.get("oldPwd")
            newPwd = request.POST.get("newPwd")
            try:
                user = Users.objects.get(id=id, password=make_password(oldPwd))
                user.password = make_password(newPwd)
                user.save()
                resp = {'rsNum': 1}
            except:
                resp = {'rsNum': -1}
        except:
            resp = {'rsNum': 0}
        return HttpResponse(json.dumps(resp), content_type="application/json")


class search(View):
    # 获取热门内容
    def getHotText(request):
        type = request.GET.get("type")
        if type == "articles":
            searchResult = Articles.objects.order_by('-good_num').all()
        elif type == "books":
            searchResult = Books.objects.order_by('-good_num').all()
        else:
            resp = {"rsNum": 0}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        page = request.GET.get("page")
        p = Paginator(searchResult, 5)
        try:
            result = p.page(page)
        except PageNotAnInteger:
            page = 1
            result = p.page(page)
        except EmptyPage:
            if page <= 0:
                page = 1
                result = p.page(page)
            else:
                page = p.num_pages
                result = p.page(page)

        context = []
        if type == "articles":
            for article in result:
                temp = {'id': article.id, 'title': article.title, 'author': article.author.username,
                        'pub_time': str(article.pub_time),
                        'click_num': article.click_num, 'good_num': article.good_num, 'text': article.text, }
                context.append(temp)
        elif type == "books":
            for book in result:
                temp = {'id': book.id, 'name': book.name, 'author': book.author, 'publisher': book.publisher,
                        'click_num': book.click_num, 'good_num': book.good_num, 'text': book.text, 'src': book.src}
                context.append(temp)
        return HttpResponse(json.dumps(context), content_type="application/json")

    # 搜索
    def searchText(request):
        searchType = request.GET.get("searchType")
        type = request.GET.get("type")
        searchText = request.GET.get("text")
        page = request.GET.get("page")

        if searchType == "articles":
            if type == "title":
                searchResult = Articles.objects.filter(title__contains=searchText).order_by("-good_num")
            elif type == "author":
                searchResult = Articles.objects.filter(author__username__contains=searchText).order_by("-good_num")
            elif type == "text":
                searchResult = Articles.objects.filter(text__contains=searchText).order_by("-good_num")
        elif searchType == "books":
            if type == "name":
                searchResult = Books.objects.filter(name__contains=searchText).order_by("-good_num")
            elif type == "author":
                searchResult = Articles.objects.filter(author__contains=searchText).order_by("-good_num")
            elif type == "text":
                searchResult = Articles.objects.filter(text__contains=searchText).order_by("-good_num")
        else:
            resp = {"rsNum": 0}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        p = Paginator(searchResult, 5)
        try:
            result = p.page(page)
        except PageNotAnInteger:
            page = 1
            result = p.page(page)
        except EmptyPage:
            if page <= 0:
                page = 1

            else:
                page = p.num_pages
            result = p.page(page)

        context = []
        if searchType == "articles":
            for article in result:
                temp = {'id': article.id, 'title': article.title, 'author': article.author.username,
                        'pub_time': str(article.pub_time),
                        'click_num': article.click_num, 'good_num': article.good_num, 'text': article.text, }
                context.append(temp)
        elif searchType == "books":
            for book in result:
                temp = {'id': book.id, 'name': book.name, 'author': book.author, 'publisher': book.publisher,
                        'good_num': book.good_num, 'text': book.text, 'src': book.src}
                context.append(temp)
        return HttpResponse(json.dumps(context), content_type="application/json")

    '''
    搜索 
    searchType为搜索目标种类(book  article)
    type 为搜索类型(name author)
    text 为搜索的内容
    page 为显示的页数

    def bookSearch(self,request):
        type=request.GET.get("searchType")
        searchText=request.GET.get("text")
        page=request.GET.get("page")
        search = func.Search(page, 5)
        if type=="book":
            result = search.book_search(searchText, request.GET.get("type"))
            context = serializers.serialize("json", result["search_result"]["objects"])
        elif type=="article":
            result = search.article_search(searchText, request.GET.get("type"))
            context = serializers.serialize("json", result["search_result"]["objects"])
        else:
            context="False"
        return HttpResponse(context, content_type="application/json")

    '''

    def getDetails(request):
        # search = func.Search(1, 5)
        context = []
        if request.GET.get("type") == "book":
            book = Books.objects.filter(id=request.GET.get("id"))
            book = book[0]
            temp = {'id': book.id, 'name': book.name, 'author': book.author, 'publisher': book.publisher,
                    'good_num': book.good_num, 'text': book.text, 'src': book.src}
            context.append(temp)
        elif request.GET.get("type") == "article":
            article = Articles.objects.filter(id=request.GET.get("id"))
            article = article[0]
            article.click_num = article.click_num + 1
            article.save()
            temp = {'id': article.id, 'title': article.title, 'author': article.author.username,
                    'pub_time': str(article.pub_time),
                    'click_num': article.click_num, 'good_num': article.good_num, 'text': article.text, }
            context.append(temp)
        return HttpResponse(json.dumps(context), content_type="application/json")


class userInfo(View):

    # 根据id获取用户指定信息
    def getPointInfo(request):
        id = request.GET.get("id")
        context = []
        if users.judgeExist(type="id", text=id):
            try:
                user = Users.objects.get(id=id)
                info = {'birthday': user.birthday, 'gender': user.gender, 'address': user.address,
                        'username': user.username}
                context.append(info)
                resp = {'rsNum': 1}
                context.append(resp)
                return HttpResponse(json.dumps(context), content_type="application/json")
            except:
                resp = {'rsNum': 0}  # 未知错误
                return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            resp = {'rsNum': -1}  # 用户不存在
            return HttpResponse(json.dumps(resp), content_type="application/json")

    def getInfo(request):
        id = request.user.id
        context = []
        if users.judgeExist(type="id", text=id):
            try:
                user = Users.objects.get(id=id)
                info = {'birthday': user.birthday, 'gender': user.gender, 'address': user.address,
                        'username': user.username, 'email': user.email}
                context.append(info)
                resp = {'rsNum': 1}
                context.append(resp)
                return HttpResponse(json.dumps(context), content_type="application/json")
            except:
                resp = {'rsNum': 0}  # 未知错误
                return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            resp = {'rsNum': -1}  # 用户不存在
            return HttpResponse(json.dumps(resp), content_type="application/json")

    def changeInfo(request):
        id = request.user.id
        birthday = request.POST.get("birthday")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        if users.judgeExist(type="id", text=id):
            try:
                user = Users.objects.get(id=id)
                user.birthday = birthday
                user.gender = gender
                user.address = address
                user.save()
                resp = {'rsNum': 1}
            except:
                resp = {'rsNum': 0}  # 未知错误
        else:
            resp = {'rsNum': -1}  # 用户不存在
        return HttpResponse(json.dumps(resp), content_type="application/json")

    def getMyGoodBook(request):
        id = request.user.id
        results = GoodLink.objects.filter(userId_id=id).order_by("-time")
        context = []
        for temp in results:
            book = Books.objects.get(id=temp.bookId_id)
            temp = {'id': book.id, 'name': book.name, 'author': book.author, 'publisher': book.publisher,
                    'good_num': book.good_num, 'text': book.text, 'src': book.src}
            context.append(temp)
        return HttpResponse(json.dumps(context), content_type="application/json")

    def getMyArticles(request):
        id = request.user.id
        results = Articles.objects.filter(author_id=id).order_by("-time")
        context = []
        for article in results:
            temp = {'id': article.id, 'title': article.title, 'author': article.author.username,
                    'pub_time': str(article.pub_time),
                    'click_num': article.click_num, 'good_num': article.good_num, 'text': article.text, }
            context.append(temp)
        return HttpResponse(json.dumps(context), content_type="application/json")


class comments(View):
    # 获取指定id书或用户的评论
    def getComments(request):
        type = request.GET.get("type")
        id = request.GET.get("id")
        context = []
        if type == "book":
            results = models.Comments.objects.filter(book_id=id)
            for comment in results:
                temp = {"id": comment.id, "pub_time": comment.pub_time, 'text': comment.text,
                        'commenterId': comment.commenter_id, 'commenterName': comment.commenter_id.username}
                context.append(temp)
        elif type == "user":
            results = models.Comments.objects.filter(commenter_id=id)
            for comment in results:
                temp = {"id": comment.id, "pug_time": comment.pub_time, 'text': comment.text, 'bookId': comment.book_id,
                        'bookName': comment.book_id.name}
                context.append(temp)
        return HttpResponse(json.dumps(context), content_type="application/json")

    # 基本完善 评论
    def toComment(request):
        if request.method!="POST":
            resp = {'rsNum': 0}
        else:
            try:
                id = request.user.id
                bookId = request.POST.get("bookId")
                text = request.POST.get("text")
                time = datetime.datetime.now()
                newInfo = models.Comments.objects.create()
                newInfo.book_id = bookId
                newInfo.commenter_id = id
                newInfo.text = text
                newInfo.pub_time = time
                newInfo.save()
                resp = {'rsNum': 1} # 成功
            except:
                resp = {'rsNum': 0} # 位置错误
        return HttpResponse(json.dumps(resp), content_type="application/json")

    # 基本完善 删除评论
    def toDelComment(request):
        if request.method!="POST":
            resp = {'rsNum': 0}
        else:
            try:
                id = request.user.id
                bookId = request.POST.get("bookId")
                try:
                    info=models.Comments.objects.get(commenter_id=id,book_id=id)
                except:
                    resp = {'rsNum': -1} #没有找到评论
                    HttpResponse(json.dumps(resp), content_type="application/json")
                info.delete()
                resp = {'rsNum': 1} # 成功
            except:
                resp = {'rsNum': 0} #未知错误
        HttpResponse(json.dumps(resp), content_type="application/json")

    # 获取指定id书或用户的点赞信息
    def getGoods(request):
        type = request.GET.get("type")
        id = request.GET.get("id")
        context = []
        if type == "book":
            results = models.GoodLink.objects.filter(bookId=id)
            for comment in results:
                temp = {"id": comment.id, "time": comment.Time,
                        'userId': comment.userId, 'userName': comment.userId.username}
                context.append(temp)
        elif type == "user":
            results = models.GoodLink.objects.filter(commenter_id=id)
            for comment in results:
                temp = {"id": comment.id, "time": comment.Time, 'bookId': comment.bookId,
                        'bookName': comment.bookId.name}
                context.append(temp)
        return HttpResponse(json.dumps(context), content_type="application/json")

    # 点赞
    def toGood(request):
        try:
            id = request.user.id
            bookId = request.POST.get("bookId")
            time = datetime.datetime.now()
            newInfo = models.GoodLink.objects.create()
            newInfo.bookId = bookId
            newInfo.userId = id
            newInfo.Time = time
            newInfo.save()
            book = Books.objects.get(id=bookId)
            book.good_num = book.good_num + 1
            book.save()
            resp = {'rsNum': 1}
        except:
            resp = {'rsNum': 0}
        return HttpResponse(json.dumps(resp), content_type="application/json")


    # 基本完善 取消赞
    def toCancelGood(request):
        if request.method!="POST":
            resp = {'rsNum': 0}
        else:
            try:
                id = request.user.id
                bookId = request.POST.get("bookId")
                try:
                    info=models.GoodLink.objects.get(bookId=bookId,userId=id)
                except:
                    resp = {'rsNum': -1}#没有点赞信息
                    return HttpResponse(json.dumps(resp), content_type="application/json")
                info.delete()
                resp = {'rsNum': 1}  # 成功
            except:
                resp = {'rsNum': 0} # 未知错误
        return HttpResponse(json.dumps(resp), content_type="application/json")
