"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import login.views  as login
from DouBan_pages.views import home_page, logout
from Users.views import my_image, test
import django.views.static
import DouBan.settings

urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('Api.urls', namespace='Api')),
    url(r'^douban/', include('DouBan_pages.urls', namespace='DouBan_pages')),
<<<<<<< HEAD
    url(r'^regist/$', login.userRegister, name='regist'),
    url(r'^login/$', login.userLogin, name='login'),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'logout/', logout, name='logout'),
=======
    url(r'^ueditor/', include('ueditor.urls')),
    url(r'^logout/', logout, name='logout'),
>>>>>>> e92f851436bb9d6b681ca45e5ce47c43d172baf2
    url(r'^media/pictures/(.+)/$', my_image),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^login/$', login.userLogin, name='login'),
    url(r'^forget', login.forget_pwd, name='forget'),
    url(r'^regist/$', login.userRegister, name='regist'),
    url(r'^media/(?P<path>.*)', django.views.static.serve, {'document_root': DouBan.settings.BASE_DIR+r'/media'}),
    url(r'^ajax_val/', login.ajax_val, name='ajax_val'),
    # url(r'^active/(.+)/$', userVerify)
]
