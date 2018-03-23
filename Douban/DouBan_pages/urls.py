from django.conf.urls import url
from . import views
app_name = 'DouBan_pages'

urlpatterns = [
    url('^search/', views.search_start, name='search'),
    url('^search/result', views.search_result, name='search_result')
]