from django.shortcuts import render
from Users.models import Articles, Users, Books
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
    return render(request, 'formal/home.html', context)


def search_start(request):
    return render(request,'formal/search.html')


def search_result(request):
    #try:
        aricle_or_book = request.GET.get('Article_or_Book', default='article')
        search_type = request.GET.get('search_type')
        search_text = request.GET.get('search_text')
        if aricle_or_book == 'Article':
            context = search.article_search(search_text, search_type)
        elif aricle_or_book == 'book':
            context = search.book_search(search_text, search_type)
        return render(request, 'formal/search_result.html', {"context":context})
    #except:
     #   pass
    #return render(request, 'formal/search_result.html', {"context":context})




