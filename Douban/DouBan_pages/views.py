from django.shortcuts import render
from Users.models import Articles, Users, Books
import django.contrib.auth as login
from .func import Search
# Create your views here.

search = Search(1)


def home_page(request):
    article_list = Articles.objects.order_by('good_num').all()
    book_list = Books.objects.order_by('good_num').all()
    context = {
        'books': book_list,
        'article': article_list,
    }
    return render(request, 'formal_before/home.html', context)


def search_start(request):
    return render(request, 'formal_before/search.html')


def search_result_article(request):
    search_type = request.GET.get('search_type')
    search_text = request.GET.get('search_text')
    index = request.GET.get('index')
    context = search.article_search(search_text, search_type)
    error = None
    return render(request, 'formal_before/search_result_article.html', {"context": context, "error": error})


def search_result_book(request):
    search_type = request.GET.get('search_type')
    search_text = request.GET.get('search_text')
    index = request.GET.get('index')
    context = search.book_search(search_text, search_type)
    error = None
    return render(request, 'formal/search_result_book.html', {"context": context, "error": error})

    # try:
        # aricle_or_book = request.GET.get('Article_or_Book', default='article')
        # search_type = request.GET.get('search_type')
        # search_text = request.GET.get('search_text')
        # if aricle_or_book == 'Article':
        #     context = search.article_search(search_text, search_type)
        # elif aricle_or_book == 'book':
        #     context = search.book_search(search_text, search_type)
        # return render(request, 'formal/search_result.html', {"context":context})
    #except:
     #   pass
    #return render(request, 'formal/search_result.html', {"context":context})


def self_home(request):
    self_info = Users.objects.get(id)


def add_article(request):
    return render(request, 'formal_before/add_article.html')


def add_article_result(request):
    text = request.POST.get('article')
    context = {"text": text}
    return render(request, 'formal_before/article_detail.html', context)


def book_detail(request):
    pass


def test(request):
    return render(request, 'formal/publish.html')


def useinfo(request):
    user_id = 0
    try:
        user_id = request.user.id
    except:
        return render(request, 404)
    user = Users.objects.get(id=user_id)
    context = {
        'signature': user.signature,
        'nick_name': user.nick_name,
        'gender': user.gender,
        'birthday': user.birthday,
    }
    return render(request, 'formal/userinfo.html', context)


def logout(request):
    login.logout(request)
    return render(request, 'signin.html')


def myPublish(request):
    user_id = 0
    try:
        user_id = request.user.id
        user = Users.objects.get(id=user_id)
    except:
        pass
    index = 1

    context = {
        # 'signature': user.signature,
        'index': index,
    }
    return render(request, 'formal/publish.html', context)
