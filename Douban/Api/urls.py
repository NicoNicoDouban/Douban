from django.conf.urls import url,include
from . import views
app_name="Api"

urlpatterns = [
    url('^getCsrf/', views.getCsrf, name='getCsrf'),
    url('^getHotArticles/', views.search.getHotArtcles, name='getHotAricles'),#获取热门文章
    url('^getHotBooks/', views.search.getHotBooks, name='getHotBooks'),#获取热门图书

    url('^bookSearch/', views.search.bookSearch, name='bookSearch'),#图书搜索
    url('^artclesSearch/', views.search.artclesSearch, name='artclesSearch'),#文章搜索

    url('^Details/$', views.search.getDetails, name='getDetails'),#按id获取图书,文章详情


    url('^login/', views.users.createUser, name='getHotAricles2'),
    url('^registe/', views.toRegiste, name='getHotAricles2'),
    url('^test/', views.test, name='getHotAricles2'),

]