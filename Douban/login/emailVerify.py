from random import Random
#from .models import userActive
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError

# 生成邮箱激活码


def createCode():
    code = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(15):
        code += chars[random.randint(0, length)]
    return code


def saveCode(user):
    code = createCode()
    #userActive.objects.create(username=user, activation_code=code)
    return code


def send_email(username, code, mail):
    try:
        send_mail(
            '豆瓣（伪）',
            '亲爱的'+username+',您好！\n豆瓣已经收到了您的注册信息。请点击以下确认链接，完成激活\nhttp://127.0.0.1:8000/active/{0}'.format(code),
            '1549274402@qq.com',
            [mail],
            fail_silently=False,
        )
    except BadHeaderError:
        return HttpResponse('Invalid header found')
