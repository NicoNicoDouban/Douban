from django.contrib import admin

# Register your models here.

from django.conf.urls import url, include
from Users.models import Users
from Users.models import Articles
from Users.models import Books
from Users.models import Comments
from Users.models import goodLink
from Users.models import followLink

admin.site.register(Users)
admin.site.register(Articles)
admin.site.register(Books)
admin.site.register(Comments)
admin.site.register(goodLink)
admin.site.register(followLink)