from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .userForm import *
from django.views.decorators.csrf import csrf_exempt
from .emailVerify import *
from Users.models import *
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.contrib.auth.hashers import make_password,check_password
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
        if userform.is_valid():
            email = request.POST['username']
            password = request.POST['password']
            verification = request.POST['verification']
            button = request.POST['submit']
            if button == 'send':
                isuser = Users.objects.filter(email=email)
                if not isuser:
                    code = createCode()
                    try:
                        send_email('豆瓣新用户', code, email)
                    except:
                        userform.add_error('username', '邮箱无效')  # 错误信息
                        return render_to_response('Register.html', {'userform': userform})
                    user = Users.objects.create(email=email, password=password, is_active=False)
                    user.set_password(password)
                    userActive.objects.create(username=user, activation_code=code, status='r')
                    context = {'username': email}
                    return render_to_response('signin.html', {'userform': userform}, context)  # 跳转到主页面
                else:
                    userform.add_error('username', '邮箱已被注册')  # 错误信息
                    return render_to_response('Register.html', {'userform': userform})
            elif button == 'regist':
                exist = userActive.objects.get(activation_code=verification, status='r')
                user = Users.objects.filter(email=email)
                print(user.id)
                print(exist.username_id)
                if user:
                    userform.add_error('username', '邮箱已被注册')  # 错误信息
                    return render_to_response('Register.html', {'userform': userform})
                else:
                    if user.id == exist.username_id:
                        user[0].is_active = True
                        user[0].save()
                        exist.delete()
                        return HttpResponse('您已完成注册')
                    else:
                        return HttpResponse('注册失败')
        else:
            # 错误信息
            return render_to_response('signin.html', {'userform': userform})
    else:
        userform = RegistForm()
    return render_to_response('Register.html', {'userform': userform})


@csrf_exempt
def userLogin(request):
    if request.user.is_authenticated:
        logout(request)
        return render_to_response('signin.html',)
    else:
        if request.method == 'POST':
            print('Step 2')
            button = request.POST.get('submit')
            if button == '欢迎回来':
                username = request.POST['username']
                password = request.POST['password']
                print(username)
                userform = LoginForm(request.POST)
                if userform.is_valid():
                    user = authenticate(request, email=username, password=password)
                    if not user:
                        # userform.add_error('username', '用户名或密码错误！')
                        context = {'username': username}
                        return render_to_response('signin.html', context)
                    else:
                        login(request, user)
                        return HttpResponse('登陆成功')  # 跳转到主页面
                else:
                    return render_to_response('signin.html',)
            elif button == '忘记密码':
                return render_to_response('ForgetPwd.html')
        # hashkey = CaptchaStore.generate_key()
        # image_url = captcha_image_url(hashkey)
        # context = {'hashkey': hashkey, 'image_url': image_url}
        userform = LoginForm()
        print('Step 1')
        # print(hashkey)
        # print(image_url)
        return render_to_response('signin.html', {'userform': userform})


@csrf_exempt
def forget_pwd(request):
    if request.method == 'POST':
        button = request.POST.get('submit')
        print(button)
        email = request.POST['username']
        if button == 'send':
            exist = Users.objects.filter(email=email)
            if not exist:
                form = ForgetForm(request.POST)
                form.add_error('email', '邮箱不存在')  # error信息
                print('邮箱不存在')
                return render_to_response('signin.html', {'ForgetForm': form})
            else:
                code = saveCode(exist[0], 'f')
                try:
                    send_mail(
                        '豆瓣（伪）',
                        '亲爱的' + exist[0].username + ',您好！\n豆瓣已经收到了您的忘记密码请求。'
                                                    '请复制以下验证码，完成修改密码\n'
                                                    + code,
                        '1549274402@qq.com',
                        [email],
                        fail_silently=False,
                    )
                except BadHeaderError:
                    return HttpResponse('Invalid header found')
                return HttpResponse('请去您的邮箱查看邮件')
        elif button == 'change':
            verification = request.POST['verification']
            flag = userActive.objects.filter(activation_code=verification, status='f', username__email__exact=email)
            if flag:
                new_pwd = request.POST.get('password')
                form = ChangeForm(request.POST)
                if form.is_valid():
                    user = Users.objects.get(email=email)
                    user.set_password(new_pwd)
                    user.save()
                    return HttpResponse('修改完成！')
                else:
                    return HttpResponse('验证码错误！')
            else:
                return HttpResponse('请确认验证码和邮箱是否正确！')
    else:
        form = ForgetForm()
    print('hello world')
    return render_to_response('signin.html', {'ForgetForm': form})


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
