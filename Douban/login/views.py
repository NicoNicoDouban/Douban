from Users.models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .userForm import *
from django.views.decorators.csrf import csrf_exempt
from .emailVerify import *


# Create your views here.

'''
def userVerify(request, code):

   exist = userActive.objects.get(activation_code=code)
    if exist:
        user = User.objects.get(username=exist.username)
        user.is_active = True
        user.save()
        exist.delete()
        return HttpResponse('您已完成注册')
    else:
        return HttpResponse('注册失败')
'''


@csrf_exempt
def userRegister(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        isuser = Users.objects.filter(username=username)
        if not isuser:
            user = Users.objects.create_user(username=username, password=password, email=email, is_active=False)
            code = saveCode(user)
            send_email(username, code, email)
            return HttpResponse('请去邮箱激活账号')  # 跳转到主页面
        else:
            userform = registForm(request.POST)
            userform.add_error('username', '用户名已注册')
            return render_to_response('signin.html', {'userform': userform})
    else:
        userform = registForm()
    return render_to_response('signin.html', {'userform': userform})


@csrf_exempt
def userLogin(request):
    if request.user.is_authenticated:
        userform = loginForm()
        return render_to_response('Register.html', {'userform': userform})
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if not user:
                userform = loginForm(request.POST)
                userform.add_error('username', '用户名或密码错误！')
                return render_to_response('signin.html', {'userform': userform})
            else:
                login(request, user)
                return HttpResponse('登陆成功')  # 跳转到主页面
        else:
            userform = loginForm()
            return render_to_response('signin.html', {'userform': userform})
