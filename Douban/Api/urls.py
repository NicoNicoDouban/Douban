from django.conf.urls import url,include
from . import views
app_name="Api"

urlpatterns = [
    url('^getCsrf/', views.getCsrf, name='getCsrf'),
]