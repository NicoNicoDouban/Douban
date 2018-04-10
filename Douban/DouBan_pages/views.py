from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from Users.models import Articles, Users, Books, Comments, UserCollectionArticles, UserCollectionBooks, GoodLink
import django.contrib.auth as login
from django.db.models import Q
from .func import Search, page_turning, test_user_info, is_login, add_image
from DouBan import settings
import os
import time
import django.utils.timezone as timezone
# Create your views here.

search = Search(1)


def home_page(request):
    article_list = Articles.objects.order_by('like_num').all()
    book_list = Books.objects.order_by('like_num').all()
    context = {}
    context = {
        'article1': article_list[0],
        'article2': article_list[1],
        'article1_text_10': article_list[0].text[0:min(len(article_list[0].text), 10)],
        'article2_text_10': article_list[0].text[0:min(len(article_list[1].text), 10)],
        'article_left': article_list[0:1],
        'article_right': article_list[1:2],
        'login': 1,
        'no_login': 0,
    }
    count = 1
    for i in book_list[0: min(book_list.count(), 8)]:
       # i.src = '/media/'+str(i.src)
        context['book'+str(count)] = i
        count += 1
    # 内容赋值结束

    # 判断是是否图书未上架
    if book_list.count() < 8:
        c = book_list.count() + 1
        while(c <= 8):
            context['book' + str(c)] = {
                'id': 0,
                'src': '/media/book_image/defalut.png',
                'text': '暂时未上架图书',
            }
            c += 1

    if is_login(request):
        context['no_login'] = 0
        context['login'] = 1
    else:
        context['no_login'] = 1
        context['login'] = 0
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


def add_article(request):
    return render(request, 'formal_before/add_article.html')


def add_article_result(request):
    text = request.POST.get('article')
    context = {"text": text}
    return render(request, 'formal_before/article_detail.html', context)


def test(request):
    return render(request, 'formal/fourtofour.html')


def user_info(request, user_info_id):
    user_id = 2
    user = Users.objects.get(id=user_id)
    # 修改个人信息
    error = {
        'flag': False,
    }
    # 个人信息修改
    if request.method == 'POST' and int(user_info_id) == int(user_id):
        if request.POST.get('type') == 'image':
            MEDIA_ROOT = os.path.join(settings.BASE_DIR, "media")
            if request.method == "POST":
                f1 = request.FILES.get('image_file')
                f1_save_name = str(timezone.now()) + f1.name.split('.')[1]
                fname = '%s\\pictures\\%s' % (MEDIA_ROOT, f1_save_name)
                with open(fname, 'wb') as pic:
                    for c in f1.chunks():
                        pic.write(c)
                user.image = 'media/pictures/%s' % f1_save_name
                user.save()

            # image = add_image(request)
            # if image:
            #     user.image = image
            #     user.save()
        else:
            user.signature = request.POST.get('signature')
            user.username = request.POST.get('username')
            user.gender = request.POST.get('gender')
            user.birthday = request.POST.get('birthday')
            error = test_user_info(user)
            if not error['flag']:
                user.save()
        '''try:
            user_id = request.user.id
        except:
            return render(request, 404)
        '''
    user_info_query = Users.objects.get(id=user_info_id)
    context = {
        'error': error,
        'user_info_query': user_info_query,
        'signature': user_info_query.signature,
        'username': user_info_query.username,
        'gender': user_info_query.gender,
        'birthday': user_info_query.birthday,
        'image': user_info_query.image,
        'user': user,
    }
    # 判断是否本人
    if user.id == user_info_id:
        context['is_user_self'] = True
    return render(request, 'formal/userinfo.html', context)


def logout(request):
    login.logout(request)
    return render(request, 'signin.html')


def my_publish(request):
    user_id = 2 ### 测试用
    # 编辑文章
    if request.POST.get('edit') == 'edit':
        context = {

        }
    #添加文章
    if request.POST.get('add_article') == 'add_article':
        title = request.POST.get('title')
        text = request.POST.get('text')
        article = Articles(
            pub_time=timezone.now(),
            text=text,
            title=title,
            author=Users.objects.get(id=user_id),
        )
        article.save()
    # 删除功能
    if not request.POST.get('delete') is None:
        delete = request.POST.get('delete')
        passage_id = request.POST.get('passage_id')
        if delete == 'delete':
            passage = Articles.objects.get(id=passage_id)
            passage.delete()

    user = Users.objects.get(id=user_id)

    context = {
        'signature': user.signature,
        'image': user.image,
        'username': user.username,
        "user":user,
    }
    # 确定页数
    articles = Articles.objects.filter(author=user_id)
    page_turning(request, articles, 4, context)

    index = context['index']
    count = 1

    for i in articles[(index-1)*4: min(index*4, len(articles))]:
        context['p'+str(count)] = i
        count += 1
        if count > 4:
            break

    return render(request, 'formal/publish.html', context)


def book_details(request, book_id):
    user_id = 2
    # 检测登入
    # if not is_login(request):
    #     return HttpResponseRedirect(reverse('login'))

    # 获得评论
    if not request.POST.get('comment_submit') is None:
        comment_text = request.POST.get('comment')
        comment = Comments(
            book_id=Books.objects.get(id=book_id),
            text=comment_text,
            commenter_id=Users.objects.get(id=user_id),
            pub_time=timezone.now(),
        )
        comment.save()
    # 内容处理
    index = 1
    book = Books.objects.get(id=book_id)
    book.click_num = book.click_num + 1
    book.save()
    comments = Comments.objects.filter(book_id=book_id)
    all_index = int(len(comments) / 2) + 1
    if comments.count() % 2 == 0:
        all_index -= 1
    if comments.count() == 0:
        context = {
            'book': book,
            'comment1': None,
            'comment2': None,
        }
    elif comments.count() == 1:
        context = {
            'book': book,
            'comment1': comments[min((index - 1) * 2, all_index - 1)],
        }
        context['commenter1'] = context['comment1'].commenter_id
    else:
        context = {
            'book': book,
            'comment1': comments[min((index-1)*2, comments.count())],
            'comment2': comments[min((index-1)*2+1, comments.count())],
        }
        context['commenter1'] = context['comment1'].commenter_id
        context['commenter2'] = context['comment2'].commenter_id
    context['user'] = Users.objects.get(id=user_id)

    #点赞处理


    # 判断是否收藏
    like = GoodLink.objects.filter(Q(userId=context['user'].id) | Q(bookId=book.id))
    if like.count() == 0:
        context['like'] = 0
        context['no_like'] = 1
    else:
        context['like'] = 1
        context['no_like'] = 0
    return render(request, 'formal/bookdetail.html', context)


def article_detail(request, article_id):
    user_id = 2
    article = Articles.objects.get(id=article_id)
    user = Users.objects.get(id=user_id)
    article_list = Articles.objects.filter(author=article.author)
    context={
        'article': article,
        'user': user,
        'author':article.author,
        'article_list':article_list,
    }
    return render(request, 'formal/textdetail.html', context)


def collection(request):
    #初始化
    user_id = 2  ### 测试用
    articles = Articles.objects.filter(usercollectionarticles__username=user_id)
    context = {
        "articles": articles[0: int(min(15, articles.count()))],
        "user": Users.objects.get(id=user_id),
    }
    # 分页


    book_list = Books.objects.filter(usercollectionbooks__username=user_id)
    count = 1
    if True:
        objects = articles
        page_items = 15
        objects_num = objects.count()
        all_index = int(objects_num / page_items) + 1
        if objects_num % page_items == 0:
            all_index -= 1
        if objects_num == 0:
            all_index += 1
        index = 1
        if not request.GET.get('first_page1') is None:
            index = 1
        if not request.GET.get('now1') is None:
            index = int(request.GET.get('now1'))
        if not request.GET.get('next1') is None:
            index = int(request.GET.get('next1'))
        if not request.GET.get('next_page1') is None:
            index = int(request.GET.get('next_page1'))
        if not request.GET.get('last_page1') is None:
            index = int(all_index)

        context['index1'] = index
        context['all_index1'] = all_index
        context['next_index1'] = str(min(index + 1, all_index))
        context['next_index_21'] = str(min(index + 2, all_index))
    if True:
        objects = book_list
        page_items = 8
        objects_num = objects.count()
        all_index = int(objects_num / page_items) + 1
        if objects_num % page_items == 0:
            all_index -= 1
        if objects_num == 0:
            all_index += 1
        index = 1
        if not request.GET.get('first_page2') is None:
            index = 1
        if not request.GET.get('now2') is None:
            index = int(request.GET.get('now2'))
        if not request.GET.get('next2') is None:
            index = int(request.GET.get('next2'))
        if not request.GET.get('next_page2') is None:
            index = int(request.GET.get('next_page2'))
        if not request.GET.get('last_page2') is None:
            index = int(all_index)

        context['index2'] = index
        context['all_index2'] = all_index
        context['next_index2'] = str(min(index + 1, all_index))
        context['next_index_22'] = str(min(index + 2, all_index))
    for i in book_list[0: min(book_list.count(), 8)]:
        context['book' + str(count)] = i
        count += 1
    return render(request, 'formal/collect.html', context)


def book_list(request):
    books = Books.objects.order_by('click_num')
    context = {
        'book1': books[0],
        'book2': books[1],
        'book3': books[2],
        'book4': books[3],
    }

    return render(request, 'formal/booklist.html', context)
