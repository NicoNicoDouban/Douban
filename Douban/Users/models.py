from django.db import models
from datetime import datetime,date
import json
# Create your models here.
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin,UserManager,AbstractUser)

# 序列化datetime和date
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


class Users(AbstractUser):
    '''

    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin site.'),
    )
    '''
    objects = UserManager()
    USERNAME_FIELD = 'email'  # 认证标识
    REQUIRED_FIELDS = ['username']
    #username=models.CharField(max_length=20,verbose_name=u"用户名",default="user",null=True, unique=True)
    # password = models.CharField(max_length=20,verbose_name=u"密码",default="123456")
    email = models.EmailField(verbose_name=u"邮箱",default="",null=False,unique=True)
    birthday = models.DateField(verbose_name=u"生日",default="2000-01-01")
    gender = models.CharField(max_length=2, verbose_name=u"性别",default="保密")
    follow_num = models.IntegerField(verbose_name=u"关注数",default=0)
    pub_time = models.DateTimeField(verbose_name=u"注册时间",default=datetime.now)
    address = models.CharField(max_length=100,verbose_name=u"用户地址", default=u"保密")
    image = models.CharField(verbose_name=u"用户头像", default=u"image/default.png", max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    #序列化的
    def toJson(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            d[attr] = getattr(self, attr)

        import json
        return json.dumps(d, cls=DateEncoder)


# score=models.FloatField(verbose_name=u"评分",default=0)
class Articles(models.Model):
    title = models.CharField(max_length=20,verbose_name=u"标题",default="一篇文章")
    author = models.ForeignKey(Users,verbose_name=u"文章作者")
    pub_time = models.DateTimeField(verbose_name=u"发表时间")
    click_num = models.IntegerField(verbose_name=u"点击数", default=0)
    text = models.TextField(verbose_name=u"文章内容", default="")
    good_num = models.IntegerField(verbose_name=u"点赞数", default=0)

    class Meta:
        verbose_name = "文章信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Books(models.Model):
<<<<<<< HEAD
    name = models.CharField(verbose_name=u"图书名", max_length=30, default="")
    writer = models.CharField(verbose_name=u"作者名", max_length=50, default="")
    publisher = models.CharField(verbose_name=u"出版社", max_length=30, default="")
    good_num = models.IntegerField(verbose_name=u"点赞数", default=0)
=======
    name = models.CharField(verbose_name=u"图书名",max_length=30,default="")
    author=models.CharField(verbose_name=u"作者名",max_length=50,default="")
    publisher=models.CharField(verbose_name=u"出版社",max_length=30,default="")
    good_num=models.IntegerField(verbose_name=u"点赞数",default=0)
>>>>>>> e3cd42459dc9b876597de3509bfeb0b47d90cb7f

    class Meta:
        verbose_name = "图书信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Comments(models.Model):
    commenter_id = models.ForeignKey(Users,verbose_name=u"评论者")
    book_id = models.ForeignKey(Books,verbose_name=u"图书")
    pub_time = models.DateTimeField(verbose_name=u"发表时间")
    text = models.TextField(verbose_name=u"评论内容", default="")

    class Meta:
        verbose_name = "评论信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.text


class GoodLink(models.Model):
    userId=models.ForeignKey(Users,verbose_name=u"点赞者")
    bookId=models.ForeignKey(Books,verbose_name=u"图书")
    Time = models.DateTimeField(verbose_name=u"点赞时间")

    class Meta:
        verbose_name = "图书点赞关联信息"
        verbose_name_plural = verbose_name


class FollowLink(models.Model):
    userId=models.ForeignKey(Users,verbose_name=u"关注者",related_name=u"关注者")
    toId=models.ForeignKey(Users,verbose_name=u"被关注者",related_name=u"被关注者")

    class Meta:
        verbose_name = "用户关注关联信息"
        verbose_name_plural = verbose_name


class userActive(models.Model):
    username = models.ForeignKey(Users, on_delete=models.CASCADE)
    activation_code = models.CharField(max_length=30)
    status = models.CharField(max_length=1, default='r')

    def __str__(self):
        return self.username.username
