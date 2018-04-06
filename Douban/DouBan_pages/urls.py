from django.conf.urls import url
from . import views
app_name = 'DouBan_pages'

urlpatterns = [
    url('^search$', views.search_start, name='search'),
    url('^search/result_book$', views.search_result_book, name='search_result_book'),
    url('^search/$', views.search_start, name='search'),
    url('^search/result_article$', views.search_result_article, name='search_result_article'),
    url(r'^add/article$', views.add_article, name='add_article'),
    url(r'add/article_result', views.add_article_result, name='add_article_result'),
    url(r'test', views.test),
    url(r'myPublish', views.myPublish, name='my_publish'),
]
