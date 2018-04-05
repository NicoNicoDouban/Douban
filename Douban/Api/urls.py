from django.conf.urls import url,include
from . import views
app_name="Api"

urlpatterns = [
    #通用
    url('^getCsrf/', views.getCsrf, name='getCsrf'),
    #用户
    url('^checkExist/', views.users.checkExist, name='checkExist'),#判断用户是否存在
    url('^changeInfo/', views.userInfo.changeInfo, name='changeInfo'),#修改用户信息
    url('^getInfo/', views.userInfo.getInfo, name='changeInfo'),#获得登录用户的信息

    url('^getPointInfo/', views.userInfo.getPointInfo, name='getPointInfo'),#根据用户id获取信息
    url('^getMyGoodBook/', views.userInfo.getMyGoodBook, name='getMyGoodBook'),#获取登录的人点赞的图书
    url('^getMyArticles/', views.userInfo.getMyArticles, name='getMyGoodBook'),#获取登录的人的文章

    #获取文章图书
    url('^getHotText/', views.search.getHotText, name='getHotBooks'),#获取热门内容
    url('^search/', views.search.searchText, name='bookSearch'),#搜索
    url('^details/$', views.search.getDetails, name='getDetails'),#按id获取图书,文章详情

    # 注册登录
    url('^login/', views.users.login, name='login'),
    url('^registe/', views.users.createUser, name='createUser'),
    url('^changePwd/', views.users.changePwd, name='changePwd'),

    #评论与点赞
    url('^getComments/', views.comments.getComments, name='getComments'),#获取指定id书或用户的评论
    url('^toComment/', views.comments.toComment, name='toComment'),#登录的用户发表评论
    url('^toDelComment/', views.comments.toDelComment, name='toDelComment'),#登录的用户删除评论

    url('^getGoods/', views.comments.getGoods, name='getGoods'),#获取指定id书或用户的点赞信息
    url('^toGood/', views.comments.toGood, name='toGood'),#登录的用户点赞
    url('^toCancelGood/', views.comments.toCancelGood, name='toCancelGood'),#登录的用户取消点赞

    #测试
    url('^test/', views.test, name='getHotAricles2'),
    url('^test2/', views.test2, name='getHotAricles2'),
    url('^photo/', views.photo, name='login11'),

]