from django.shortcuts import render, HttpResponse
from Users.models import Articles, Users, Books
import django.contrib.auth as login
from .func import Search
from DouBan import settings
# Create your views here.

search = Search(1)


def home_page(request):
    article_list = Articles.objects.order_by('good_num').all()
    book_list = Books.objects.order_by('good_num').all()
    context = {
        'books': book_list,
        'article': article_list,
    }
    return render(request, 'formal/shouye.html', context)


def search_start(request):
    return render(request, 'formal_before/search.html')


def search_result_article(request):
    search_type = request.GET.get('search_type')
    search_text = request.GET.get('search_text')
    index = request.GET.get('index')
    context = search.article_search(search_text, search_type)
    error = None
    if search.article_searchinfo_safe_test(search_text, search_type):
        return render(request, 'formal/shouye.html')
    return render(request, 'formal_before/search_result_article.html', {"context": context, "error": error})


def search_result_book(request):
    search_type = request.GET.get('search_type')
    search_text = request.GET.get('search_text')
    index = request.GET.get('index')
    context = search.book_search(search_text, search_type)
    error = None
    if search.book_searchinfo_safe_test(search_text, search_type):
        return render(request, 'formal/shouye.html')
    return render(request, 'formal_before/search_result_book.html', {"context": context, "error": error})


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


def user_info(request):
    user_id = 1
    '''try:
        user_id = request.user.id
    except:
        return render(request, 404)
    '''
    user = Users.objects.get(id=user_id)
    context = {
        'signature': user.signature,
        'username': user.username,
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


def catinfo(request):
    if request.method == "POST":
        f1 = request.FILES['pic1']
        fname = '%s\\pictures\\%s' % (settings.MEDIA_ROOT, f1.name)
        with open(fname, 'wb') as pic:
            for c in f1.chunks():
                pic.write(c)
        return HttpResponse("ok")
    else:
        return HttpResponse("error")


def addImage(request):
    return render(request, 'formal_before/add_image.html')
