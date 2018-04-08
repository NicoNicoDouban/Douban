from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .userForm import *
from django.views.decorators.csrf import csrf_exempt
from .emailVerify import *
from Users.models import *
from django.template import RequestContext
from django.contrib.auth.password_validation import validate_password


# Create your views here.


def userVerify(request, code):
    exist = userActive.objects.get(activation_code=code, status='r')
    if exist:
        user = Users.objects.get(username=exist.username)
        user.is_active = True
        user.save()
        exist.delete()
        return HttpResponse('您已完成注册')
    else:
        return HttpResponse('注册失败')

@csrf_exempt
def userRegister(request):
    if request.method == 'POST':
        userform = RegistForm(request.POST)
        password = request.POST['password']
        email = request.POST['email']
        username = email
        isuser = Users.objects.filter(username=username)
        if not isuser:
            isEmail = Users.objects.filter(email=email)
            if(isEmail):
                userform.add_error('email', '邮箱已被注册')
                return render_to_response('Register.html', {'userform': userform})
            user = Users.objects.create_user(username=username, password=password, email=email, is_active=False)
            code = createCode()
            try:
                send_email(username, code, email)
            except:
                userform.add_error('email', '邮箱无效')
                return render_to_response('Register.html', {'userform': userform})
            userActive.objects.create(username=user, activation_code=code, status='r')
            return HttpResponse('请去邮箱激活账号')  # 跳转到主页面
        else:
            userform.add_error('username', '用户名已注册')
            return render_to_response('Register.html', {'userform': userform})
    else:
        userform = RegistForm()
    return render_to_response('Register.html', {'userform': userform})


@csrf_exempt
def userLogin(request):
    if request.user.is_authenticated:
        logout(request)
        userform = LoginForm()
        return render_to_response('signin.html', {'userform': userform})
    else:
        if request.method == 'POST':
            button = request.POST.get('submit')
            if button == '登录':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if not user:
                    userform = LoginForm(request.POST)
                    userform.add_error('username', '用户名或密码错误！')
                    return render_to_response('signin.html', {'userform': userform})
                else:
                    login(request, user)
                    return HttpResponse('登陆成功')  # 跳转到主页面
            elif button == '忘记密码':
                return render_to_response('ForgetPwd.html')
        userform = LoginForm()
        return render_to_response('signin.html', {'userform': userform})


@csrf_exempt
def forget_pwd(request):
    if request.method == 'POST':
        email = request.POST['email']
        exist = User.objects.filter(email=email)
        if not exist:
            form = ForgetForm(request.POST)
            form.add_error('email', '邮箱不存在')
            return render_to_response('ForgetPwd.html', {'ForgetForm': form})
        else:
            code = saveCode(exist[0], 'f')
            try:
                send_mail(
                    '豆瓣（伪）',
                    '亲爱的' + exist[0].username + ',您好！\n豆瓣已经收到了您的忘记密码信息。'
                                                '请点击以下确认链接，完成修改密码\n'
                                                'http://127.0.0.1:8000/change/{0}'.format(
                        code),
                    '1549274402@qq.com',
                    [email],
                    fail_silently=False,
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return HttpResponse('请去您的邮箱查看邮件')
    else:
        form = ForgetForm()
    return render_to_response('ForgetPwd.html', {'ForgetForm': form})


@csrf_exempt
def change_pwd(request, code):
    exist = userActive.objects.filter(activation_code=code, status='f')
    if exist:
        if request.method == 'GET':
            form = ChangeForm2()
            return render_to_response('ChangePwd.html', {'form': form})
        else:
            form = ChangeForm2(request.POST)
            new_pwd = request.POST.get('newPwd')
            con_pwd = request.POST.get('conPwd')
            if new_pwd == con_pwd:
                user = Users.objects.get(username=exist[0].username)
                user.set_password(new_pwd)
                user.save()
                exist.delete()
                return HttpResponse('修改成功')
            else:
                form.add_error('conPwd', '请确认两次输入的密码是否相同')
                return render_to_response('ChangePwd.html', {'form': form})
    else:
        if request.method == 'GET':
            form = ChangeForm()
            return render_to_response('ChangePwd.html', {'form': form})
        else:
            form = ChangeForm(request.POST)
            old_pwd = form['oldPwd']
            user_ = request.user
            if user_.check_passwrod(old_pwd):
                new_pwd = request.POST.get('newPwd')
                con_pwd = request.POST.get('conPwd')
                if new_pwd == con_pwd:
                    user = Users.objects.get(username=user_.username)
                    user.set_password(new_pwd)
                    user.save()
                    return HttpResponse('修改成功')
                else:
                    form.add_error('conPwd', '请确认两次输入的密码是否相同')
                    return render_to_response('ChangePwd.html', {'form': form})
            else:
                form.add_error('oldPwd', '密码错误')
                return render_to_response('ChangePwd.html', {'form': form})
