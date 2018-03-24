from Users.models import Articles, Books
from . import  setting
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class Search:
    index = 1

    def __init__(self, index):
        self.index = index

    def __str__(self):
        return self.index

    def book_search(self, search_text='', search_type='title'):
        """
        对图书进行搜索
        :param search_text: 搜索的文本内容
        :param search_type: 搜索类型，分为title， writer， 两种
        :return: 搜索结果字典 'search_result'里有要的结果， 'search_correct'是搜索的正确性
        """
        search_correct = True
        search_result = None
        try:
            if search_type == 'title':
                search_result = Books.objects.filter(title__contains=search_text)
            elif search_type == 'writer':
                search_result = Books.objects.filter(writer__contains=search_text)
        except:
            search_correct = False
        context = {
            'search_result': self.__objects_list(search_result),
            'search_correct': search_correct,
        }
        return context

    def article_search(self, search_text='', search_type='title'):
        """
        根据文章搜索
        :param search_text: 搜索文本内容
        :param search_type: 搜索类型：title， text，writer
        :return: 搜索结果字典 'search_result'里有要的结果， 'search_correct'是搜索的正确性
        """
        search_correct = True
        search_result = None
        try:
            if search_type == 'title':
                search_result = Articles.objects.filter(title__contains = search_text)
            elif search_type == 'text':
                search_result = Articles.objects.filter(text__contains= search_text)
            elif search_type == 'writer':
                search_result = Articles.objects.filter(writer__nick_name__contains= search_text)
        except:
            search_correct = False
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
        try:
            articles = Articles.objects.order_by('good_num').all()
            return {
                'search_result': self.__objects_list(articles),
                'search_correct': True,
            }
        except:
            return {
                'search_result': None,
                'search_correct': False,
            }

    def good_book(self):
        try:
            books = Books.objects.order_by('good_num').all()
            return {
                'search_result': self.__objects_list(books),
                'search_correct': True,
            }
        except:
            return {
                'search_result': None,
                'search_correct': False,
            }

    def __objects_list(self, p_objects, page_items=setting.the_number_of_items_in_each_page):
        """
        返回相应的文章列表，页码, 总页数
        :param p_objects:
        :param page_items:
        :return:
        """
        p = Paginator(p_objects, page_items)
        context = {}
        try:
            context['passages'] = p.page(self.index)
        except PageNotAnInteger:
            self.index = 1
            context['passages'] = p.page(1)
        except EmptyPage:
            if self.index <= 0:
                self.index = 1
                context['passages'] = p.page(1)
                context['page_error'] = "已经到首页了"
            else:
                index = p.num_pages
                context['passages'] = p.page(p.num_pages)
                context['page_error'] = '已经到末页了'
        context['index'] = str(self.index)
        context['index_all'] = str(p.num_pages)
        return context