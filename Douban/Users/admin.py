from django.contrib import admin

# Register your models here.

from django.conf.urls import url, include
from .models import *

admin.site.register(Users)
admin.site.register(Articles)
admin.site.register(Books)
admin.site.register(Comments)
admin.site.register(GoodLink)
admin.site.register(FollowLink)
