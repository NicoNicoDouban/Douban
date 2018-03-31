from django.conf.urls import url
from . import views
app_name = 'DouBan_pages'

urlpatterns = [
    url('^search$', views.search_start, name='search'),
    url('^search/result_book$', views.search_result_book, name='search_result_book'),
    url('^search/$', views.search_start, name='search'),
    url('^search/result_article$', views.search_result_article, name='search_result_article'),
    url(r'^add/article$', views.add_article, name='add_article'),
]