from django.contrib import admin
from .models import *
from datetime import datetime, timedelta

# Register your models here.


class UserFilterBirthday(admin.SimpleListFilter):
    title = u'生日'
    parameter_name = 'birthday'

    def lookups(self, request, model_admin):
        return (
            ('1', u'1月'),
            ('2', u'2月'),
            ('3', u'3月'),
            ('4', u'4月'),
            ('5', u'5月'),
            ('6', u'6月'),
            ('7', u'7月'),
            ('8', u'8月'),
            ('9', u'9月'),
            ('10', u'10月'),
            ('11', u'11月'),
            ('12', u'12月'),
        )

    def queryset(self, request, queryset):
        month = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        for i in month:
            if self.value() == i:
                return queryset.filter(birthday__month=i)


class UserFilterPubtime(admin.SimpleListFilter):
    title = u'注册时间'
    parameter_name = 'pub_time'

    def lookups(self, request, model_admin):
        return (
            ('0', u'今天'),
            ('1', u'本周'),
            ('2', u'本月'),
            ('3', u'今年'),
            ('4', u'今年之前')
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            start = datetime.now() - timedelta(days=1)
            return queryset.filter(pub_time__gte=start)
        elif self.value() == '1':
            start = datetime.now() - timedelta(days=7)
            return queryset.filter(pub_time__gte=start)
        elif self.value() == '2':
            day = datetime.now().day
            start = datetime.now() - timedelta(days=day)
            return queryset.filter(pub_time__gte=start)
        elif self.value() == '3':
            return queryset.filter(pub_time__year=datetime.now().year)
        elif self.value() == '4':
            return queryset.exclude(pub_time__year=datetime.now().year)


class CommentFilterPubtime(admin.SimpleListFilter):
    title = u'发布时间'
    parameter_name = 'pub_time'

    def lookups(self, request, model_admin):
        return (
            ('0', u'今天'),
            ('1', u'本周'),
            ('2', u'本月'),
            ('3', u'今年'),
            ('4', u'今年之前')
        )
    def queryset(self, request, queryset):
        if self.value() == '0':
            start = datetime.now() - timedelta(days=1)
            return queryset.filter(pub_time__gte=start)
        elif self.value() == '1':
            start = datetime.now() - timedelta(days=7)
            return queryset.filter(pub_time__gte=start)
        elif self.value() == '2':
            day = datetime.now().day
            start = datetime.now() - timedelta(days=day)
            return queryset.filter(pub_time__gte=start)
        elif self.value() == '3':
            return queryset.filter(pub_time__year=datetime.now().year)
        elif self.value() == '4':
            return queryset.exclude(pub_time__year=datetime.now().year)


class ArticleFilterPubtime(admin.SimpleListFilter):
    title = u'发布时间'
    parameter_name = 'pub_time'

    def lookups(self, request, model_admin):
        return (
            ('0', u'今天'),
            ('1', u'本周'),
            ('2', u'本月'),
            ('3', u'今年'),
            ('4', u'今年之前')
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            start = datetime.now() - timedelta(days=1)
            return queryset.filter(pub_time__gte=start)
        elif self.value() == '1':
            start = datetime.now() - timedelta(days=7)
            return queryset.filter(pub_time__gte=start)
        elif self.value() == '2':
            day = datetime.now().day
            start = datetime.now() - timedelta(days=day)
            return queryset.filter(pub_time__gte=start)
        elif self.value() == '3':
            return queryset.filter(pub_time__year=datetime.now().year)
        elif self.value() == '4':
            return queryset.exclude(pub_time__year=datetime.now().year)


class ClickNumFilter(admin.SimpleListFilter):
    title = u'点击数'
    parameter_name = 'click_num'

    def lookups(self, request, model_admin):
        return (
            ('0', u'10000点击以上'),
            ('1', u'5000点击以上'),
            ('2', u'1000点击以上'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(click_num__gte=10000)
        if self.value() == '1':
            return queryset.filter(click_num__gte=5000)
        if self.value() == '2':
            return queryset.filter(click_num__gte=1000)


class LickNumFilter(admin.SimpleListFilter):
    title = u'点赞数'
    parameter_name = 'good_num'

    def lookups(self, request, model_admin):
        return (
            ('0', u'1000以上'),
            ('1', u'500以上'),
            ('2', u'200以上'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(good_num__gte=1000)
        if self.value() == '1':
            return queryset.filter(good_num__gte=500)
        if self.value() == '2':
            return queryset.filter(good_num__gte=200)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'birthday', 'gender',
        'follow_num', 'pub_time', 'address', 'image', 'is_active')
    search_fields = ('username', 'email')
    fields = (
        'username',
        'password', 'signature', 'email', 'is_active', 'birthday', 'gender', 'address', 'image')
    list_per_page = 30
    ordering = ('-pub_time',)
    list_filter = ('gender', UserFilterPubtime, UserFilterBirthday)
    list_editable = ('is_active',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if change:
            obj_original = self.model.objects.get(pk=obj.pk)
            if obj_original.password == form.cleaned_data['password']:
                obj.password = obj_original.password
            else:
                obj.password = obj.user.password
        else:
            obj.password = obj.user.password
        obj.save()


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_time', 'click_num', 'like_num')
    search_fields = ('title', 'author')
    fields = ('title', 'author', 'pub_time', 'text')
    raw_id_fields = ('author',)
    list_per_page = 30
    ordering = ('-pub_time',)
    list_filter = (ArticleFilterPubtime, ClickNumFilter, LickNumFilter)

    class Media:
        js = (
            '/static/js/kindeditor-4.1.11/kindeditor-all.js',
            '/static/js/kindeditor-4.1.11/lang/zh-CN.js',
            '/static/js/kindeditor-4.1.11/config.js'
        )


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'publisher', 'type', 'like_num', 'click_num', 'src')
    search_fields = ('name', 'author', 'publisher', 'text', 'type')
    fields = ('name', 'author', 'publisher', 'type', 'text', 'src')
    list_per_page = 30
    list_filter = (LickNumFilter,)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('commenter_id', 'book_id', 'pub_time')
    search_fields = ('commenter_id__username', 'book_id__name', 'text')
    raw_id_fields = ('commenter_id', 'book_id')
    list_per_page = 30
    list_filter = (CommentFilterPubtime,)

    class Media:
        js = (
            '/static/js/kindeditor-4.1.11/kindeditor-all.js',
            '/static/js/kindeditor-4.1.11/lang/zh-CN.js',
            '/static/js/kindeditor-4.1.11/config.js'
        )


class GoodLinkAdmin(admin.ModelAdmin):
    list_display = ('userId', 'bookId', 'Time')
    search_fields = ('userId__username', 'bookId__name')
    raw_id_fields = ('userId', 'bookId')
    fk_field = ('userId',)
    list_per_page = 30


class FollowLinkAdmin(admin.ModelAdmin):
    list_display = ('userId', 'toId')
    search_fields = ('userId__username', 'toId__username')
    raw_id_fields = ('userId', 'toId')
    list_per_page = 30


class CollectionBooksAdmin(admin.ModelAdmin):
    list_display = ('username', 'book')
    search_fields = ('username', 'book')
    raw_id_fields = ('username', 'book')
    list_per_page = 30


class CollectionArticlesAdmin(admin.ModelAdmin):
    list_display = ('username', 'Articles')
    search_fields = ('username', 'Articles')
    raw_id_fields = ('username', 'Articles')
    list_per_page = 30


admin.site.site_header = '豆瓣管理页面'
admin.site.site_title = '豆瓣管理页面'
admin.site.index_title = '豆瓣'
admin.site.register(Users, UserAdmin)
admin.site.register(Articles, ArticleAdmin)
admin.site.register(Books, BookAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(GoodLink, GoodLinkAdmin)
admin.site.register(FollowLink, FollowLinkAdmin)
admin.site.register(UserCollectionBooks, CollectionBooksAdmin)
admin.site.register(UserCollectionArticles, CollectionArticlesAdmin)
