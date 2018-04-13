from django import forms
from captcha.fields import CaptchaField


class RegistFormR(forms.Form):
    username = forms.EmailField(label='用户名', max_length=20, min_length=3, error_messages={
        'required': '邮箱不得为空',
        'min_length': '请输入正确的邮箱',
        'invalid': '请输入正确的邮箱',
        'max_length': '请输入正确的邮箱'
    })
    password = forms.CharField(label='密码', max_length=16, widget=forms.PasswordInput(), min_length=8, error_messages={
        'min_length': '密码至少为8位',
        'required': '密码不得为空',
        'max_length': '密码最多16位'
    })
    verification = forms.CharField(label='验证码', max_length=10, min_length=10, error_messages={
        'max_length': '请输入正确的验证码',
        'required': '验证码不得为空',
        'min_length': '请输入正确的验证码'
    })


class RegistFormS(forms.Form):
    username = forms.EmailField(label='用户名', max_length=20, min_length=3, error_messages={
        'required': '邮箱不得为空',
        'min_length': '请输入正确的邮箱',
        'invalid': '请输入正确的邮箱',
        'max_length': '请输入正确的邮箱'
    })


class LoginForm(forms.Form):
    username = forms.EmailField(label='用户名', min_length=3, max_length=20, error_messages={
        'required': '邮箱不得为空',
        'min_length': '请输入正确的邮箱',
        'invalid': '请输入正确的邮箱',
        'max_length': '请输入正确的邮箱'
    })
    password = forms.CharField(label='密码', max_length=16, widget=forms.PasswordInput(), min_length=8, error_messages={
        'min_length': '密码至少为8位',
        'required': '密码不得为空',
        'max_length': '密码最多16位'
    })
    captcha = CaptchaField()


class ForgetFormS(forms.Form):
    username = forms.EmailField(label='用户名', min_length=3, max_length=20, error_messages={
        'required': '邮箱不得为空',
        'min_length': '请输入正确的邮箱',
        'invalid': '请输入正确的邮箱',
        'max_length': '请输入正确的邮箱'
    })


class ForgetFormR(forms.Form):
    username = forms.EmailField(label='用户名', min_length=3, max_length=20, error_messages={
        'required': '邮箱不得为空',
        'min_length': '请输入正确的邮箱',
        'invalid': '请输入正确的邮箱',
        'max_length': '请输入正确的邮箱'
    })
    password = forms.CharField(label='新密码', min_length=8, max_length=16, widget=forms.PasswordInput(), error_messages={
        'min_length': '密码至少为8位',
        'required': '密码不得为空',
        'max_length': '密码最多16位'
    })
    verification = forms.CharField(label='验证码', max_length=10, min_length=10, error_messages={
        'max_length': '请输入正确的验证码',
        'required': '验证码不得为空',
        'min_length': '请输入正确的验证码'
    })
