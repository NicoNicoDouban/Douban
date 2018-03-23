from django import forms


class registForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=12, min_length=3, error_messages={
        'min_length': '用户名至少3个字符'
    })
    password = forms.CharField(label='密码', max_length=16, widget=forms.PasswordInput(), min_length=8, error_messages={
        'min_length': '密码至少为8位'
    })
    email = forms.EmailField(label='邮箱')


class loginForm(forms.Form):
    username = forms.CharField(label='用户名', min_length=3, max_length=12)
    password = forms.CharField(label='密码', max_length=16, widget=forms.PasswordInput(), min_length=8)