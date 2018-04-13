from django.conf.urls import url
from . import views
import django, DouBan
app_name = 'DouBan_pages'

urlpatterns = [
    url(r'(?P<user_info_id>[0-9]+)/user_info', views.user_info, name='user_info'),
    # url('^search/result_book$', views.search_result_book, name='search_result_book'),
    # url('^search/$', views.search_start, name='search'),
    # url('^search/result_article$', views.search_result_article, name='search_result_article'),
    url(r'search', views.search_result, name='search'),
    url(r'my_publish', views.my_publish, name='my_publish'),
    url(r'(?P<book_id>[0-9]+)/book_detail', views.book_details, name='book_detail'),
    url(r'(?P<article_id>[0-9]+)/article_detail', views.article_detail, name='article_detail'),
    url(r'collection', views.collection, name='collection'),
    url(r'book_list', views.book_list, name='book_list'),
    url(r'add_image', views.add_image, name='add_image'),
    url(r'^media/(?P<path>.*)', django.views.static.serve, {'document_root': DouBan.settings.BASE_DIR+r'/media/'}),
    url(r'^media/(?P<path>.*)', django.views.static.serve, {'document_root': DouBan.settings.BASE_DIR+r'/media/'}),
    # url(r'^active/(.+)/$', userVerify)
    # url(r'^active/(.+)/$', userVerify)
    # url(r'^search',, name='search')
]
