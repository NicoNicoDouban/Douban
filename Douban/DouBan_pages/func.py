from Users.models import Articles, Books
from . import setting
from DouBan import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import re, os
from django.utils import timezone


class Search:
    index = 1
    page_items = 5

    def __init__(self, index, page_items=5):
        self.index = index
        self.page_items = page_items

    def __str__(self):
        return self.index

    def book_search(self, search_text='', search_type='name'):
        """
        对图书进行搜索
        :param search_text: 搜索的文本内容
        :param search_type: 搜索类型，分为name， author， 两种
        :return: 搜索结果字典 'search_result'里有要的结果， 'search_correct'是搜索的正确性
        search_result里的东西{'objects': 返回的内容, 'page_error': 搜索问题提示信息, 'index': 页码, 'index_all': 所有页面数
        """
        search_correct = True
        search_result = None
        if search_type == 'name':
            search_result = Books.objects.filter(name__contains=search_text)
        elif search_type == 'author':
            search_result = Books.objects.filter(author__contains=search_text)
        context = {
            'search_result': self.__objects_list(search_result),
            'search_correct': search_correct,
        }
        return context

    def article_search(self, search_text='', search_type='title'):
        """
        根据文章搜索
        :param search_text: 搜索文本内容
        :param search_type: 搜索类型：title， text，author
        :return: 搜索结果字典 'search_result'里有要的结果， 'search_correct'是搜索的正确性
        search_result里的东西{'objects': 返回的内容, 'page_error': 搜索问题提示信息, 'index': 页码, 'index_all': 所有页面数
        """
        search_correct = True
        search_result = None
        if search_type == 'title':
            search_result = Articles.objects.filter(title__contains=search_text)
        elif search_type == 'text':
            search_result = Articles.objects.filter(text__contains=search_text)
        elif search_type == 'author':
            search_result = Articles.objects.filter(writer__nick_name__contains=search_text)
        context = {
            'search_result': self.__objects_list(search_result),
            'search_correct': search_correct,
        }
        return context

    def good_article(self):
        """
        返回热门文章
        :return: 搜索结果字典 'search_result'里有要的结果， 'search_correct'是搜索的正确性
        """
        articles = Articles.objects.order_by('like_num').all()
        return {
            'search_result': self.__objects_list(articles),
            'search_correct': True,
        }

    def good_book(self):
        books = Books.objects.order_by('like_num').all()
        return {
            'search_result': self.__objects_list(books),
            'search_correct': True,
        }

    def book_searchinfo_safe_test(self, search_text='', search_type='name'):
        """
        根据传入值判断安全性
        :param search_text:
        :param search_type:
        :return:
        """
        if search_type != 'name' and search_type != 'author':
            return False
        if len(search_text) > 30:
            return False
        if search_text is None:
            return False
        return True

    def article_searchinfo_safe_test(self, search_text='', search_type='title'):
        """
        根据传入值判断安全性
        :param search_text:
        :param search_type:
        :return:
        """
        if search_type != 'title' and search_type != 'author' and search_type != 'text':
            return False
        if len(search_text) > 10:
            return False
        if search_text is None:
            return False
        return True


    def __objects_list(self, p_objects, page_items=page_items):
        """
        返回相应的文章列表，页码, 总页数
        :param p_objects:
        :param page_items:
        :return: {'passages': 返回的内容, 'page_error': 搜索问题提示信息, 'index': 页码, 'index_all': 所有页面
        """
        p = Paginator(p_objects, page_items)
        context = {}
        try:
            context['objects'] = p.page(self.index)
        except PageNotAnInteger:
            self.index = 1
            context['objects'] = p.page(1)
        except EmptyPage:
            if self.index <= 0:
                self.index = 1
                context['objects'] = p.page(1)
                context['page_error'] = "已经到首页了"
            else:
                index = p.num_pages
                context['objects'] = p.page(p.num_pages)
                context['page_error'] = '已经到末页了'
        context['index'] = str(self.index)
        context['index_all'] = str(p.num_pages)
        return context


def page_turning(request, objects, page_items, context):
    """
    分页器，要求传入的request中有first_page，now，next_page，last_page
    返回context 有 all_index，next_index，next_index_2,index四项
    :param request: 请求
    :param objects: 分页项，为queryset
    :param page_items: 每页项数
    :param context: 被添加入的字典
    :return: context 有 all_index，next_index，next_index_2,index四项
    """
    objects_num = objects.count()
    all_index = int(objects_num / page_items) + 1
    if objects_num % page_items == 0:
        all_index -= 1
    if objects_num == 0:
        all_index += 1
    index = 1
    if not request.GET.get('first_page') is None:
        index = 1
    if not request.GET.get('now') is None:
        index = int(request.GET.get('now'))
    if not request.GET.get('next') is None:
        index = int(request.GET.get('next'))
    if not request.GET.get('next_page') is None:
        index = int(request.GET.get('next_page'))
    if not request.GET.get('last_page') is None:
        index = int(all_index)

    context['index'] = index
    context['all_index'] = all_index
    context['next_index'] = str(min(index + 1, all_index))
    context['next_index_2'] = str(min(index + 2, all_index))
    return context


def is_login(request):
    '''
    如未登入，返回False,若登入返回用户id
    :param request:
    :return:
    '''
    user = request.user
    if user is None:
        return False
    else:
        return user.id


def test_user_info(user):
    flag = 0
    context = {
        'error': '',
    }
    if len(user.signature) == 0 and len(user.signature) > 20:
        context['error'] += '个性签名长度不正确</br>'
        flag = 1
    if user.gender != 'S' or user.gender != 'F' or user.gender != 'S':
        context['error'] += '性别不正确'
        flag = 1
    if not re.match(r"(\d{4}-\d{1,2}-\d{1,2})",user.birthday):
        context['error'] += '生日格式不正确'
        flag = 1
    if flag:
        context['flag'] = True
        return context
    else:
        context['flag'] = False
        return context


def add_image(request):
    MEDIA_ROOT = os.path.join(settings.BASE_DIR, "media")
    if request.method == "POST":
        f1 = request.FILES.get('image_file')
        f1_save_name = str(timezone.now()) + f1.name.split('.')[1]
        fname = '%s\\pictures\\%s' % (MEDIA_ROOT, f1_save_name)
        with open(fname, 'wb') as pic:
            for c in f1.chunks():
                pic.write(c)
        return 'media/pictures/%s' % f1_save_name
    else:
        return False
