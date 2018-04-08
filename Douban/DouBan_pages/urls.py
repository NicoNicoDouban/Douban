from django.conf.urls import url
from . import views
app_name = 'DouBan_pages'

urlpatterns = [
    url(r'(?P<user_info_id>[0-9]+)/user_info', views.user_info, name='user_info'),
    url('^search$', views.search_start, name='search'),
    url('^search/result_book$', views.search_result_book, name='search_result_book'),
    url('^search/$', views.search_start, name='search'),
    url('^search/result_article$', views.search_result_article, name='search_result_article'),
    url(r'^add/article$', views.add_article, name='add_article'),
    url(r'add/article_result', views.add_article_result, name='add_article_result'),
    url(r'my_publish', views.my_publish, name='my_publish'),
    url(r'add_image_page', views.add_image_page, name='addImage'),
    url(r'add_image', views.add_image, name='createInfo'),
    url(r'(?P<book_id>[0-9]+)/book_detail', views.book_details, name='book_detail'),
    url(r'(?P<article_id>[0-9]+)/article_detail', views.article_detail, name='article_detail'),
    url(r'collection', views.collection, name='collection'),
    url(r'test', views.test, name='test')
]
