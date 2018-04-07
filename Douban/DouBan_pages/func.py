from Users.models import Articles, Books
from . import setting
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import re

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
        :param search_type: 搜索类型，分为name， writer， 两种
        :return: 搜索结果字典 'search_result'里有要的结果， 'search_correct'是搜索的正确性
        search_result里的东西{'objects': 返回的内容, 'page_error': 搜索问题提示信息, 'index': 页码, 'index_all': 所有页面数
        """
        search_correct = True
        search_result = None
        if search_type == 'name':
            search_result = Books.objects.filter(name__contains=search_text)
        elif search_type == 'writer':
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
        :param search_type: 搜索类型：title， text，writer
        :return: 搜索结果字典 'search_result'里有要的结果， 'search_correct'是搜索的正确性
        search_result里的东西{'objects': 返回的内容, 'page_error': 搜索问题提示信息, 'index': 页码, 'index_all': 所有页面数
        """
        search_correct = True
        search_result = None
        if search_type == 'title':
            search_result = Articles.objects.filter(title__contains=search_text)
        elif search_type == 'text':
            search_result = Articles.objects.filter(text__contains=search_text)
        elif search_type == 'writer':
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
        articles = Articles.objects.order_by('good_num').all()
        return {
            'search_result': self.__objects_list(articles),
            'search_correct': True,
        }

    def good_book(self):
        books = Books.objects.order_by('good_num').all()
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
        if search_type != 'name' and search_type != 'writer':
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
        if search_type != 'title' and search_type != 'writer' and search_type != 'text':
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