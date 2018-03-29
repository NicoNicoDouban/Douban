from django.conf.urls import url,include
from . import views
app_name="Api"

urlpatterns = [
    url('^getCsrf/', views.getCsrf, name='getCsrf'),
    url('^getHotArticles/', views.getHotAricles, name='getHotAricles'),
    url('^registe/', views.toRegiste, name='getHotAricles2'),
    url('^test/', views.test, name='getHotAricles2'),

]