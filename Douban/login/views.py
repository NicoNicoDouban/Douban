from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .userForm import *
from django.views.decorators.csrf import csrf_exempt
from .emailVerify import *
from Users.models import *
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from django.template import RequestContext
from django.contrib.auth.password_validation import validate_password


# Create your views here.


def ajax_val(request):
    if request.is_ajax():
        cs = CaptchaStore.objects.filter(response=request.GET['response'], hashkey=request.GET['hashkey'])
        if cs:
            json_data = {'status': 1}
        else:
            json_data = {"status": 0}
        return JsonResponse(json_data)
    else:
        json_data = {"status": 0}
        return JsonResponse(json_data)

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
        button = request.POST['submit']
        email = request.POST['username']
        password = request.POST['password']
        verification = request.POST['verification']
        if button == 'send':
            userform = RegistFormS(request.POST)
            if userform.is_valid():
                isuser = Users.objects.filter(email=email)
                if not isuser:
                    code = createCode()
                    exist = userActive.objects.filter(email=email, status='r')
                    if exist:
                        userform.add_error('username', '验证码已发送，请去邮箱查看')
                        return render_to_response('signin2.html',
                                                  {'userform': userform,
                                                   'username': email,
                                                   'verification': verification, })
                    try:
                        send_email('豆瓣新用户', code, email)
                    except BadHeaderError:
                        userform.add_error('username', '邮箱无效')  # 错误信息
                        return render_to_response('signin2.html',
                                                  {'userform': userform,
                                                   'username': email,
                                                   'verification': verification,})
                    userActive.objects.create(email=email, activation_code=code, status='r')
                    return render_to_response('signin2.html',
                                              {'userform': userform,
                                               'username': email,
                                               'verification': verification,})  # 跳转到主页面
                else:
                    userform.add_error('username', '邮箱已被注册')  # 错误信息
                    return render_to_response('signin2.html',
                                              {'userform': userform,
                                               'username': email,
                                               'verification': verification,})
            else:
                return render_to_response('signin2.html',
                                          {'userform': userform,
                                           'username': email,
                                           'verification': verification, })
        elif button == 'regist':
            userform = RegistFormR(request.POST)
            if userform.is_valid():
                exist = userActive.objects.filter(activation_code=verification, status='r')
                if exist and email == exist[0].email:
                    exist[0].delete()
                    user = Users.objects.create(email=email, password=password)
                    user.set_password(password)
                    user.save()
                    hashkey = CaptchaStore.generate_key()
                    image_url = captcha_image_url(hashkey)
                    return render_to_response('signin.html', {'userform': userform, 'username': email,
                                                              'hashkey': hashkey,
                                                              'image_url': image_url })
                else:
                    userform.add_error('verification', '验证码未发送或验证码错误')
                    return render_to_response('signin2.html',
                                              {'userform': userform, 'username': email,
                                               'verification': verification,})
            else:
                return render_to_response('signin2.html',
                                          {'userform': userform,
                                           'username': email,
                                           'verification': verification,})
    return render_to_response('signin2.html')


@csrf_exempt
def userLogin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')  # 主页面
    else:
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            userform = LoginForm(request.POST)
            if userform.is_valid():
                user = authenticate(request, email=username, password=password)
                if not user:
                    userform.add_error('username', '用户名或密码错误！')
                    return render_to_response('signin.html', {'userform': userform, 'username': username,
                                                              'hashkey': hashkey,
                                                              'image_url': image_url})
                else:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))  # 跳转到主页面
            else:
                return render_to_response('signin.html', {'userform': userform, 'username': username,
                                                          'hashkey': hashkey,
                                                          'image_url': image_url})
        userform = LoginForm()
        return render_to_response('signin.html', {'userform': userform, 'hashkey': hashkey,
                                                  'image_url': image_url})



@csrf_exempt
def forget_pwd(request):
    if request.method == 'POST':
        button = request.POST.get('submit')
        email = request.POST['username']
        verification = request.POST['verification']
        new_pwd = request.POST.get('password')
        if button == 'send':
            form = RegistFormS(request.POST)
            if form.is_valid():
                exist = Users.objects.filter(email=email)
                if not exist:
                    form.add_error('username', '邮箱不存在')  # error信息
                    return render_to_response('signin3.html', {'userform': form, 'username': email,
                                                               'verification': verification})
                else:
                    active = userActive.objects.filter(email=email, status='f')
                    if active:
                        form.add_error('username', '验证码已发送，请去邮箱查看')
                        return render_to_response('signin3.html', {'userform': form, 'username': email,
                                                                   'verification': verification, })
                    code = saveCode(email, 'f')
                    try:
                        send_mail(
                            '豆瓣（伪）',
                            '亲爱的' + exist[0].username + ',您好！\n豆瓣已经收到了您的忘记密码请求。'
                                                        '请复制以下验证码，完成修改密码\n' + code,
                            '1549274402@qq.com',
                            [email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse('Invalid header found')
                    return render_to_response('signin3.html', {'userform': form,
                                                               'username': email,
                                                               'verification': verification})
            else:
                return render_to_response('signin3.html', {'userform': form,
                                                           'username': email, 'verification': verification})
        elif button == 'change':
            form = RegistFormR(request.POST)
            if form.is_valid():
                flag = userActive.objects.filter(activation_code=verification, status='f', email=email)
                if flag:
                    flag[0].delete()
                    user = Users.objects.get(email=email)
                    user.set_password(new_pwd)
                    user.save()
                    hashkey = CaptchaStore.generate_key()
                    image_url = captcha_image_url(hashkey)
                    return render_to_response('signin.html', {'userform': form, 'username': email,
                                                              'hashkey': hashkey,
                                                              'image_url': image_url})
                else:
                    form.add_error('verification', '请确认验证码和邮箱是否正确')
                    return render_to_response('signin3.html', {'userform': form,
                                                               'username': email, 'verification': verification})
            else:
                return render_to_response('signin3.html', {'userform': form,
                                                           'username': email, 'verification': verification})
    else:
        form = RegistFormS()
    return render_to_response('signin3.html', {'userform': form})
