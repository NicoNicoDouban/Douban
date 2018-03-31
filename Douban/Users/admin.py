from django.contrib import admin

# Register your models here.

from django.conf.urls import url, include
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'birthday', 'gender', 'follow_num', 'pub_time', 'address', 'image', 'is_active')
    search_fields = ('username', 'email')
    list_per_page = 10


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_time', 'click_num', 'good_num')
    search_fields = ('title', 'author')
    list_per_page = 10


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'publisher', 'good_num')
    search_fields = ('name', 'author')
    list_per_page = 10


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('commenter_id', 'book_id', 'pub_time')
    search_fields = ('commenter_id__username', 'book_id__name')
    list_per_page = 10


class GoodLinkAdmin(admin.ModelAdmin):
    list_display = ('userId', 'bookId', 'Time')
    search_fields = ('userId__username', 'bookId__username')
    list_per_page = 10


class FollowLinkAdmin(admin.ModelAdmin):
    list_display = ('userId', 'toId')
    search_fields = ('userId__username', 'toId__username')
    list_per_page = 10


admin.site.register(Users, UserAdmin)
admin.site.register(Articles, ArticleAdmin)
admin.site.register(Books, BookAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(GoodLink, GoodLinkAdmin)
admin.site.register(FollowLink, FollowLinkAdmin)
