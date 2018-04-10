from django import forms
from captcha.fields import CaptchaField

class RegistForm(forms.Form):
    username = forms.EmailField(label='用户名', max_length=20, min_length=3, error_messages={
        'min_length': '用户名至少3个字符'
    })
    password = forms.CharField(label='密码', max_length=16, widget=forms.PasswordInput(), min_length=8, error_messages={
        'min_length': '密码至少为8位'
    })


class LoginForm(forms.Form):
    username = forms.EmailField(label='用户名', min_length=3, max_length=12)
    password = forms.CharField(label='密码', max_length=16, widget=forms.PasswordInput(), min_length=8)
    captcha = CaptchaField()


class ForgetForm(forms.Form):
    email = forms.EmailField(label='邮箱', max_length=20, min_length=6, error_messages={
        'min_length': '请输入正确的邮箱'
    })


class ChangeForm(forms.Form):
    username = forms.EmailField(label='用户名', min_length=8, max_length=16, widget=forms.PasswordInput())
    password = forms.CharField(label='新密码', min_length=8, max_length=16, widget=forms.PasswordInput(), error_messages={
        'min_length': '密码最少8位'
    })


class ChangeForm2(forms.Form):
    newPwd = forms.CharField(label='新密码', min_length=8, max_length=16, widget=forms.PasswordInput(), error_messages={
        'min_length': '密码最少8位'
    })
    conPwd = forms.CharField(label='重复密码', min_length=8, max_length=16, widget=forms.PasswordInput(), error_messages={
        'min_length': '密码最少8位'
    })
