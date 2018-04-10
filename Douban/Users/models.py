from django.db import models
from datetime import datetime,date
import json
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin,UserManager,AbstractUser)
from  DouBan import settings

# 序列化datetime和date
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

'''
class Users(AbstractUser):
    AbstractUser.username=
    Gender_Choice = (
        ('F', u'女'),
        ('M', u'男'),
        ('S', u'保密')
    )
    objects = UserManager()
    #USERNAME_FIELD = 'email'  # 认证标识
    #REQUIRED_FIELDS = ['username', ]
    #username=models.CharField(max_length=20,verbose_name=u"用户名",default="user",null=True, unique=True)
    password = models.CharField(max_length=20,verbose_name=u"密码", validators=[validate_password])
    email = models.EmailField(verbose_name=u"邮箱",default="",null=False,unique=True)
    birthday = models.DateField(verbose_name=u"生日",default="2000-01-01")
    gender = models.CharField(max_length=1, verbose_name=u"性别",default="S", choices=Gender_Choice)
    follow_num = models.IntegerField(verbose_name=u"被关注数",default=0)
    pub_time = models.DateTimeField(verbose_name=u"注册时间",default=datetime.now)
    address = models.CharField(max_length=100,verbose_name=u"用户地址", default=u"保密")
    image = models.CharField(verbose_name=u"用户头像", default=u"image/default.png", max_length=100)
    signature = models.CharField(verbose_name=u"个性签名", default="这个人很懒，还什么都没说", max_length=30)
    nick_name = models.CharField(verbose_name=u'昵称', default='小豆瓣', max_length=30)
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

'''


class Users(AbstractBaseUser, PermissionsMixin):
    Gender_Choice = (
        ('F', u'女'),
        ('M', u'男'),
        ('S', u'保密')
    )
    objects = UserManager()
    USERNAME_FIELD = 'email'  # 认证标识
    REQUIRED_FIELDS = ["username"]
    username=models.CharField(max_length=20,verbose_name=u"昵称",default="user",null=True, unique=False)
    email = models.EmailField(verbose_name=u"邮箱",default="",null=False,unique=True)
    birthday = models.DateField(verbose_name=u"生日",default="2000-01-01")
    gender = models.CharField(max_length=1, verbose_name=u"性别",default="S", choices=Gender_Choice)
    follow_num = models.IntegerField(verbose_name=u"被关注数",default=0)
    pub_time = models.DateTimeField(verbose_name=u"注册时间",default=datetime.now)
    address = models.CharField(max_length=100,verbose_name=u"用户地址", default=u"保密")
    image = models.ImageField(verbose_name=u"用户头像", default='/media/pictures/defalut_avatar.png', max_length=100,
                              upload_to='media/pictures/')
    signature = models.CharField(verbose_name=u"个性签名", default=u"这个人很懒什么都没写", max_length=50)
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    def get_short_name(self):
        "Returns the username for the user."
        return self.username

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
    title = models.CharField(max_length=20,verbose_name=u"标题", default="一篇文章")
    author = models.ForeignKey(Users,verbose_name=u"文章作者")
    pub_time = models.DateTimeField(verbose_name=u"发表时间", default=datetime.now)
    click_num = models.IntegerField(verbose_name=u"点击数", default=0)
    text = models.TextField(verbose_name='文章内容', default="")
    like_num = models.IntegerField(verbose_name=u"点赞数", default=0)

    class Meta:
        verbose_name = "文章信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Books(models.Model):
    BookType = (
        ('0', u'推理悬疑'),
        ('1', u'科学真实'),
        ('2', u'社会民生'),
        ('3', u'世界未来'),
        ('4', u'宇宙天体'),
        ('5', u'历史讲古'),
        ('6', u'美丽文学'),
        ('7', u'其他神秘')
    )
    name = models.CharField(verbose_name=u"图书名", max_length=30, default="")
    author = models.CharField(verbose_name=u"作者名", max_length=50, default="")
    author_introduction = models.CharField(verbose_name=u'作者简介', max_length=50, default='暂无介绍')
    author_picture = models.CharField(verbose_name=u"作者照片", default="/media/book_image/defalut_author.png", max_length=100)
    publisher = models.CharField(verbose_name=u"出版社", max_length=30, default="")
    like_num = models.IntegerField(verbose_name=u"点赞数", default=0)
    click_num = models.IntegerField(verbose_name=u"点击数", default=0)
    text = models.TextField(verbose_name=u"简介", default="暂无介绍")
    src = models.ImageField(verbose_name=u"封面url地址", default='/media/pictures/defalut_avatar.png', max_length=100,
                              upload_to='media/pictures/')
    type = models.CharField(verbose_name=u'图书分类', max_length=3, default=u'其他', choices=BookType)

    class Meta:
        verbose_name = "图书信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Comments(models.Model):
    commenter_id = models.ForeignKey(Users,verbose_name=u"评论者")
    book_id = models.ForeignKey(Books, verbose_name=u"图书")
    pub_time = models.DateTimeField(verbose_name=u"发表时间")
    text = models.TextField(verbose_name='评论内容', default="")

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
    username = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name=u"用户")
    activation_code = models.CharField(max_length=30, verbose_name=u"激活码")
    status = models.CharField(max_length=1, default='r', verbose_name=u"状态")

    def __str__(self):
        return self.username.username

    class Meta:
        verbose_name = "用户激活验证码"
        verbose_name_plural = verbose_name


class UserCollectionBooks(models.Model):
    username = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name=u'用户')
    book = models.ForeignKey(Books, on_delete=models.CASCADE, verbose_name=u'书籍')

    class Meta:
        verbose_name = "用户收藏书籍"
        verbose_name_plural = verbose_name


class UserCollectionArticles(models.Model):
    username = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name=u'用户')
    Articles = models.ForeignKey(Articles, on_delete=models.CASCADE, verbose_name=u'文章')

    class Meta:
        verbose_name = "用户收藏文章"
        verbose_name_plural = verbose_name
