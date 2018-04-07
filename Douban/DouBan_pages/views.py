from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from Users.models import Articles, Users, Books, Comments
import django.contrib.auth as login
from .func import Search
from DouBan import settings
import os
# Create your views here.

search = Search(1)


def home_page(request):
    article_list = Articles.objects.order_by('good_num').all()
    book_list = Books.objects.order_by('good_num').all()
    context = {}
    context = {
        'article1': article_list[0],
        'article2': article_list[1],
        'article1_text_10': article_list[0].text[0:min(len(article_list[0].text), 10)],
        'article2_text_10': article_list[0].text[0:min(len(article_list[1].text), 10)],
        'article_left': article_list[0:1],
        'article_right': article_list[1:2],
    }
    count = 1
    for i in book_list[0: min(len(book_list), 8)]:
        context['book'+str(count)] = i
        count += 1
    return render(request, 'formal/shouye.html', context)


def search_start(request):
    return render(request, 'formal_before/search.html')


def search_result_article(request):
    search_type = request.GET.get('search_type', default=None)
    search_text = request.GET.get('search_text', default=None)
    index = request.GET.get('index')

    if search_text == None:
        search_text = ''
    if search_type is None:
        search_type = 'title'
    if not search.article_searchinfo_safe_test(search_text, search_type):
        return HttpResponseRedirect(reverse('home'))

    context = search.article_search(search_text, search_type)
    error = None

    return render(request, 'formal_before/search_result_article.html', {"context": context, "error": error})


def search_result_book(request):
    search_type = request.GET.get('search_type')
    search_text = request.GET.get('search_text')
    index = request.GET.get('index')

    if search_text is None:
        search_text = ''
    if search_type is None:
        search_type = 'name'
    if not search.book_searchinfo_safe_test(search_text, search_type):
        return HttpResponseRedirect(reverse('home'))

    context = search.book_search(search_text, search_type)
    error = None

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
    user_id = 2
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
        'image': user.image
    }
    return render(request, 'formal/userinfo.html', context)


def logout(request):
    login.logout(request)
    return render(request, 'signin.html')


def my_publish(request):
    if not request.POST.get('delete') is None:
        delete = request.POST.get('delete')
        passage_id = request.POST.get('passage_id')
        if delete == 'delete':
            passage = Articles.objects.get(id=passage_id)
            passage.delete()
    user_id = 2
    user = Users.objects.get(id=user_id)
    # 确定页数
    passages = Articles.objects.filter(author=user_id)
    all_index = int(len(passages) / 4) + 1
    if len(passages) % 4 == 0:
        all_index -= 1
    index = 1
    if not request.GET.get('first') is None:
        index = 1
    if not request.GET.get('now') is None:
        index = int(request.GET.get('now'))
    if not request.GET.get('next') is None:
        index = int(request.GET.get('next'))
    if not request.GET.get('next_page') is None:
        index = int(request.GET.get('next_page'))
    if not request.GET.get('last_page') is None:
        index = int(all_index)

    context = {
        'signature': user.signature,
        'index': index,
        'image': user.image,
        'username': user.username,
        'all_index': all_index,
        'next_index': str(min(index+1, all_index)),
        'next_index_2': str(min(index+2, all_index)),
    }
    count = 1

    for i in passages[(index-1)*4: min(index*4, len(passages))]:
        context['p'+str(count)] = i
        count += 1
        if count > 4:
            break
    return render(request, 'formal/publish.html', context)


def add_image(request):
    MEDIA_ROOT = os.path.join(settings.BASE_DIR, "media")
    if request.method == "POST":
        f1 = request.FILES['pic1']
        fname = '%s\\pictures\\%s' % (MEDIA_ROOT, f1.name)
        with open(fname, 'wb') as pic:
            for c in f1.chunks():
                pic.write(c)
        return HttpResponse("ok")
    else:
        return HttpResponse("error")


def add_image_page(request):
    return render(request, 'formal_before/add_image.html')


def book_detail(request, book_id):
    user_id = 2
    if not request.POST.get('comment_submit') is None:
        comment_text = request.POST.get('comment')
        comment = Comments.objects.get(book_id=book_id)
        comment.text = comment_text
        comment.commenter_id = user_id
        comment.save()
    index = 1
    book = Books.objects.get(id=book_id)
    comments = Comments.objects.filter(book_id=book_id)
    all_index = int(len(comments) / 2) + 1
    if len(comments) % 2 == 0:
        all_index -= 1
    if len(comments) == 0:
        context = {
            'book': book,
            'comment1': None,
            'comment2': None,
        }
    else:
        context = {
            'book': book,
            'comment1': comments[min((index-1)*2, all_index-1)],
            'comment2': comments[min((index-1)*2+1, all_index)],
        }
        context['commenter1'] = Users.objects.get(id=context['comment1'].author)
        context['commenter2'] = Users.objects.get(id=context['comment1'].author)
    return render(request, 'formal/bookdetail.html', context)
