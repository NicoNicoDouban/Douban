from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from Users.models import Articles, Users, Books, Comments, UserCollectionArticles, UserCollectionBooks, GoodLink
import django.contrib.auth as login
from django.db.models import Q
from .func import Search, page_turning, test_user_info, is_login, test_article, add_figure
from DouBan import settings
import os, re
import time
import django.utils.timezone as timezone
from Users.form import ArticleForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.

search = Search(1)


def home_page(request):
    try:
        user_id = is_login(request)

        article_list = Articles.objects.order_by('like_num').all()
        book_list = Books.objects.order_by('like_num').all()
        context = {}
        p = Paginator(article_list,14)
        if p.num_pages == 0:
            context = {
                'login': 1,
                'no_login': 0,
            }
        elif p.num_pages == 1:
            context = {
                'article_left': p.page(1),
                'login': 1,
                'no_login': 0,
            }
        else:
            context = {
                'article_left': p.page(1),
                'article_right': p.page(2),
                'login': 1,
                'no_login': 0,
            }
        for i in book_list:
            i.text = i.text[0: min(len(i.text), 10)] + '...'
        if article_list.count() == 0:
            pass
        elif article_list.count() == 1:
            context['article_left'] = article_list[0]
        elif article_list.count() <= 0:
            context['article_left'] = article_list[0: min(article_list.count(), 10)]
        else:
            context['article_left'] = article_list[0:10]
            context['article_right'] = article_list[10: min(article_list.count(), 20)]
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

        if user_id:
            context['no_login'] = 0
            context['login'] = 1
            context['user_id'] = user_id
            context['user_image'] = Users.objects.get(id=user_id).image
        else:
            context['no_login'] = 1
            context['login'] = 0
        return render(request, 'formal/shouye.html', context)
    except Exception:
        return render(request, 'formal/fourtofour.html')


# def search_start(request):
#     return render(request, 'formal_before/search.html')
#
#
# def search_result_article(request):
#     search_type = request.GET.get('search_type', default=None)
#     search_text = request.GET.get('search_text', default=None)
#     index = request.GET.get('index')
#
#     if search_text == None:
#         search_text = ''
#     if search_type is None:
#         search_type = 'title'
#     if not search.article_searchinfo_safe_test(search_text, search_type):
#         return HttpResponseRedirect(reverse('home'))
#
#     context = search.article_search(search_text, search_type)
#     error = None
#
#     return render(request, 'formal_before/search_result_article.html', {"context": context, "error": error})
#
#
# def search_result_book(request):
#     search_type = request.GET.get('search_type')
#     search_text = request.GET.get('search_text')
#     index = request.GET.get('index')
#
#     if search_text is None:
#         search_text = ''
#     if search_type is None:
#         search_type = 'name'
#     if not search.book_searchinfo_safe_test(search_text, search_type):
#         return HttpResponseRedirect(reverse('home'))
#
#     context = search.book_search(search_text, search_type)
#     error = None
#
#     return render(request, 'formal_before/search_result_book.html', {"context": context, "error": error})


def user_info(request, user_info_id):
    try:
        user_id = is_login(request)
        user = Users.objects.get(id=user_id)

        # 个人信息修改
        error = {
            'error': '',
        }
        if request.method == 'POST' and int(user_info_id) == int(user_id):
            if request.POST.get('type') == 'info':
                user.signature = request.POST.get('signature', default='什么都没有')
                user.username = request.POST.get('username')
                user.gender = request.POST.get('gender')
                user.birthday = request.POST.get('birthday')
                flag = 0
                if len(user.username) <= 0 or len(user.username) > 10:
                    error['error'] += '姓名长度不正确，应少于10个字符'
                    flag = 1
                if len(user.signature) <= 0 or len(user.signature) > 20:
                    error['error'] += '个性签名长度不正确，应少于20个字符'
                    flag = 1
                if str(user.gender) != 'S' and str(user.gender) != 'F' and str(user.gender) != 'M':
                    error['error'] += '性别不正确'
                    flag = 1
                if not re.match(r"(\d{4}-\d{1,2}-\d{1,2})", str(user.birthday)):
                    error['error'] += '生日格式不正确,请按年-月-日填写'
                    flag = 1
                if not flag:
                    try:
                        user.save()
                    except Exception:
                        error['error'] += '信息错误，请仔细检查'
            else:
                old_image_path = os.path.join(settings.BASE_DIR, str(user.image))
                if os.path.exists(old_image_path) and str(user.image)[-len('defalut_avatar.png'):] != 'defalut_avatar.png':
                    os.remove(old_image_path)
                MEDIA_ROOT = os.path.join(settings.BASE_DIR, "media")
                picture = request.FILES['pic1']
                last_name = picture.name.split('.')[len(picture.name.split('.')) - 1]
                time_tag = str(time.time()).replace('.', '-')
                fname = '%s\\pictures\\%s' % (MEDIA_ROOT, time_tag + '.' + last_name)
                with open(fname, 'wb') as pic:
                    for c in picture.chunks():
                        pic.write(c)
                user.image = 'media/pictures/' + time_tag + '.' + last_name
                user.save()
                # image = add_image(request)
                # if image:
                #     user.image = image
                #     user.save()
            '''try:
                user_id = request.user.id
            except:
                return render(request, 404)
            '''
        user_info_query = Users.objects.get(id=user_info_id)
        context = {
            'error': error['error'],
            'user_info_query': user_info_query,
            'signature': user_info_query.signature,
            'username': user_info_query.username,
            'gender': user_info_query.gender,
            'birthday': user_info_query.birthday,
            'image': str(user_info_query.image),
            'user': user,
        }
        # 判断是否本人

        return render(request, 'formal/userinfo.html', context)
    except Exception:
        return render(request, 'formal/fourtofour.html')


def logout(request):
    try:
        login.logout(request)
        return render(request, 'signin.html')
    except Exception:
        return render(request, 'formal/fourtofour.html')


def my_publish(request):
    try:
        user_id = is_login(request)
        if not user_id:
            return HttpResponseRedirect(reverse('login'))
        # 编辑文章
        error = None
        edit = {
            'title': '在此填写标题',
            'text': '在此填写内容',
            'edit_id':0,
        }
        edit_judge = 0
        if not request.GET.get('edit') is None:
            edit_judge = 1
        if not request.POST.get('article_id') is None:
            article_id = request.POST.get('article_id')
            article = Articles.objects.get(id=article_id)
            edit = {
                'text': article.text,
                'title': article.title,
                'edit_id': article_id,
            }
            edit_judge  = 1
        #添加文章
        error = ''

        if request.POST.get('add_article') == 'add_article':
            title = request.POST.get('title')
            text = request.POST.get('text')
            edit_id = request.POST.get('edit_id')
            if edit_id == 0:
                article = Articles(
                    pub_time=timezone.now(),
                    text=text,
                    title=title,
                    author=Users.objects.get(id=user_id),
                )
            else:
                article = Articles.objects.get(id=edit_id)
                article.pub_time = timezone.now()
                article.text = text
                article.title = title
                article.author = Users.objects.get(id=user_id)
            error = test_article(article)
            if not error:
                article.save()
            else:
                edit = {
                    'text': article.text,
                    'title': article.title
                }
                edit_judge = 1
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
            'error': error,
            'title': edit['title'],
            'text': edit['text'],
            'edit_id': edit['edit_id'],
            'edit_judge': edit_judge,
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

        form = ArticleForm()
        context['form'] = form
        return render(request, 'formal/publish.html', context)
    except Exception:
        return render(request, 'formal/fourtofour.html')


def book_details(request, book_id):
    try:
        user_id = is_login(request)
        if not user_id:
            return HttpResponseRedirect(reverse('login'))
        # 检测登入

        # 检测乱点书
        if int(book_id) <= 0:
            return HttpResponseRedirect(reverse('home'))

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
        # 浏览量
        book = Books.objects.get(id=book_id)
        book.click_num = book.click_num + 1
        book.save()

        # 填充内容
        context = {}
        context['book'] = book
        book.src = r'/'+str(book.src)
        comments = Comments.objects.filter(book_id=book_id).order_by('pub_time')
        # 分页

        p = Paginator(comments, 2)
        if True:
            index = 1
            # 判断点了哪个按钮
            if not request.GET.get('first_page') is None:
                index = 1
            if not request.GET.get('before_page') is None:
                index -= 1
            if not request.GET.get('now') is None:
                index = int(request.GET.get('now'))
            if not request.GET.get('next') is None:
                index = int(request.GET.get('next'))
            if not request.GET.get('next_page') is None:
                index = int(request.GET.get('next_page'))
            if not request.GET.get('last_page') is None:
                index = int(p.num_pages)

            context['index'] = index
            context['all_index'] = p.num_pages
            context['next_index'] = str(min(index + 1, p.num_pages))
            context['next_index_2'] = str(min(index + 2, p.num_pages))

        # 分页物件
        index = context['index']
        try:
            context['comment'] = p.page(int(index))
        except (EmptyPage, PageNotAnInteger):
            context['comment'] = p.page(1)
            index = 1
            context['index'] = index
            context['all_index'] = p.num_pages
            context['next_index'] = str(min(index + 1, p.num_pages))
            context['next_index_2'] = str(min(index + 2, p.num_pages))
        # context['book_author'] = book_author[(index-1)*6, min((index-1)*6, book_author.count())]

        # if comments.count() == 0:
        #     context = {
        #         'book': book,
        #         'comment1': None,
        #         'comment2': None,
        #     }
        # elif comments.count() == 1:
        #     context = {
        #         'book': book,
        #         'comment1': comments[min((index - 1) * 2, all_index - 1)],
        #     }
        #     context['commenter1'] = context['comment1'].commenter_id
        # else:
        #     context = {
        #         'book': book,
        #         'comment1': comments[min((index-1)*2, comments.count())],
        #         'comment2': comments[min((index-1)*2+1, comments.count())],
        #     }
        #     context['commenter1'] = context['comment1'].commenter_id
        #     context['commenter2'] = context['comment2'].commenter_id
        context['user'] = Users.objects.get(id=user_id)

        # 收藏处理

        if request.method == 'POST':
            if request.POST.get('like_or_not') == 'no_like':
                good = GoodLink(
                    userId=Users.objects.get(id=user_id),
                    bookId=book,
                    Time=timezone.now(),
                )
                good.save()
            if request.POST.get('like_or_not') == 'like':
                good = GoodLink.objects.get(Q(userId=Users.objects.get(id=user_id))& Q(bookId=book))
                good.delete()

        # 判断是否收藏
        like = GoodLink.objects.filter(Q(userId=user_id) & Q(bookId=book.id))
        if like.count() == 0:
            context['like'] = 0
            context['no_like'] = 1
        else:
            context['like'] = 1
            context['no_like'] = 0
        return render(request, 'formal/bookdetail.html', context)
    except Exception:
        return render(request, 'formal/fourtofour.html')


def article_detail(request, article_id):
    try:
        user_id = is_login(request)
        if not user_id:
            return HttpResponseRedirect(reverse('login'))
        article = Articles.objects.get(id=article_id)
        article.click_num += 1
        article.save()
        article = Articles.objects.get(id=article_id)
        user = Users.objects.get(id=user_id)
        article_list = Articles.objects.filter(author=article.author)
        context = {
            'article': article,
            'user': user,
            'author': article.author,
            'article_list': article_list,
        }
        # 收藏处理

        if request.method == 'POST':
            if request.POST.get('like_or_not') == 'no_like':
                good = UserCollectionArticles(
                    username=Users.objects.get(id=user_id),
                    Articles=Articles.objects.get(id=article_id),
                )
                good.save()
            if request.POST.get('like_or_not') == 'like':
                good = UserCollectionArticles.objects.get(Q(username=Users.objects.get(id=user_id)) & Q(Articles=Articles.objects.get(id=article_id)))
                good.delete()

        # 判断是否收藏
        like = UserCollectionArticles.objects.filter(Q(username=Users.objects.get(id=user_id)) & Q(Articles=Articles.objects.get(id=article_id)))
        if like.count() == 0:
            context['like'] = 0
            context['no_like'] = 1
        else:
            context['like'] = 1
            context['no_like'] = 0
        return render(request, 'formal/textdetail.html', context)
    except Exception:
        return render(request, 'formal/fourtofour.html')


def collection(request):
    try:
        #初始化
        user_id = is_login(request)
        if not user_id:
            return HttpResponseRedirect(reverse('login'))
        # 文章删除
        delete_id = request.GET.get('delete')
        if not delete_id is None:
            collect_article = UserCollectionArticles.objects.get(Q(username=user_id) & Q(Articles=delete_id))
            collect_article.delete()

        articles = Articles.objects.filter(usercollectionarticles__username=user_id).order_by('pub_time')
        books = Books.objects.filter(goodlink__userId_id=user_id).order_by('click_num')
        for i in books:
            i.text = i.text[0:min(len(i.text), 10)] + '...'

        article_list = Paginator(articles, 15)
        book_list = Paginator(books, 8)

        count = 1
        # 分页
        context = {}
        context["user"] = Users.objects.get(id=user_id)
        if True:
            index = 1
            if not request.GET.get('first_page1') is None:
                index = 1
            if not request.GET.get('before_page1') is None:
                index -= 1
            if not request.GET.get('now1') is None:
                index = int(request.GET.get('now1'))
            if not request.GET.get('next1') is None:
                index = int(request.GET.get('next1'))
            if not request.GET.get('next_page1') is None:
                index = int(request.GET.get('next_page1'))
            if not request.GET.get('last_page1') is None:
                index = int(article_list.num_pages)

            context['index1'] = index
            context['all_index1'] = article_list.num_pages
            context['next_index1'] = str(min(index + 1, article_list.num_pages))
            context['next_index_21'] = str(min(index + 2, article_list.num_pages))
        if True:
            index = 1
            if not request.GET.get('first_page2') is None:
                index = 1
            if not request.GET.get('before_page2') is None:
                index -= 1
            if not request.GET.get('now2') is None:
                index = int(request.GET.get('now2'))
            if not request.GET.get('next2') is None:
                index = int(request.GET.get('next2'))
            if not request.GET.get('next_page2') is None:
                index = int(request.GET.get('next_page2'))
            if not request.GET.get('last_page2') is None:
                index = int(book_list.num_pages)

            context['index2'] = index
            context['all_index2'] = book_list.num_pages
            context['next_index2'] = str(min(index + 1, book_list.num_pages))
            context['next_index_22'] = str(min(index + 2, book_list.num_pages))

        try:
            # context["articles"] = []
            # count = 0
            # for i in article_list.page(context['index1']):
            #     context["articles"][count] = i
            #     count += 1
            context['articles'] = article_list.page(int(context['index1']))
        except Exception:
            index = 1
            context['index1'] = index
            context['all_index1'] = article_list.num_pages
            context['next_index1'] = str(min(index + 1, article_list.num_pages))
            context['next_index_21'] = str(min(index + 2, article_list.num_pages))
            context['articles'] = article_list.page(int(context['index1']))
        for i in book_list.page(context['index2']):
            context['book' + str(count)] = i
            count += 1
        return render(request, 'formal/collect.html', context)
    except Exception:
        return render(request, 'formal/fourtofour.html')


def book_list(request):
    try:
        context = {}
        user_id = is_login(request)
        if user_id:
            context['no_login'] = 0
            context['login'] = 1
            context['user_id'] = user_id
            context['user_image'] = Users.objects.get(id=user_id).image
        else:
            context['no_login'] = 1
            context['login'] = 0
        books = Books.objects.order_by('click_num')
        c = 0
        for i in books:
            i.src = '/' + str(i.src)
            c += 1
            if c > 16:
                break

        c = 1
        for i in books:
            context['book' + str(c)] = i
            c += 1
            if c > 16:
                break
        # 判断是是否图书未上架
        if books.count() < 16:
            c = books.count() + 1
            while c <= 16:
                context['book' + str(c)] = {
                    'id': 0,
                    'src': '/media/book_image/defalut.png',
                    'text': '暂时未上架图书',
                }
                c += 1

        # 图书分类列表
        for j in range(0, 8):
            type = None
            type_raw = Books.objects.filter(type=j)
            #分页
            type_page = Paginator(type_raw, 6)
            if True:
                index = 1
                if not request.GET.get('first_page'+str(j)) is None:
                    index = 1
                if not request.GET.get('before_page'+str(j)) is None:
                    index -= 1
                if not request.GET.get('now'+str(j)) is None:
                    index = int(request.GET.get('now'+str(j)))
                if not request.GET.get('next'+str(j)) is None:
                    index = int(request.GET.get('next'+str(j)))
                if not request.GET.get('next_page'+str(j)) is None:
                    index = int(request.GET.get('next_page'+str(j)))
                if not request.GET.get('last_page'+str(j)) is None:
                    index = int(type_page.num_pages)

                try:
                    type = type_page.page(index)
                    context['index'+str(j)] = index
                    context['all_index'+str(j)] = type_page.num_pages
                    context['next_index'+str(j)] = str(min(index + 1, type_page.num_pages))
                    context['next_index_2'+str(j)] = str(min(index + 2, type_page.num_pages))
                except Exception:
                    index = 1
                    type = type_page.page(index)
                    context['index'+str(j)] = index
                    context['all_index'+str(j)] = type_page.num_pages
                    context['next_index'+str(j)] = str(min(index + 1, type_page.num_pages))
                    context['next_index_2'+str(j)] = str(min(index + 2, type_page.num_pages))
            # 绑数据
            c = 0
            for i in type:
                i.src = '/' + str(i.src)
                c += 1
                context['type'+str(j)+str(c)] = i
                if c > 6:
                    break
            if len(type) < 6:
                c = len(type) + 1
                while c <= 6:
                    context['type'+str(j)+str(c)] = {
                        'id': 0,
                        'src': '/media/book_image/defalut.png',
                        'text': '暂时未上架图书',
                    }
                    c += 1
        return render(request, 'formal/booklist.html', context)
    except Exception:
        return render(request, 'formal/fourtofour.html')


def add_image(request):
    try:
        MEDIA_ROOT = os.path.join(settings.BASE_DIR, "media")
        if request.method == "POST":
            picture = request.FILES['pic1']
            last_name = picture.name.split('.')[len(picture.name.split('.'))-1]
            fname = '%s\\pictures\\%s' % (MEDIA_ROOT, str(time.time()) + '.' + last_name)
            with open(fname, 'wb') as pic:
                for c in picture.chunks():
                    pic.write(c)
            return HttpResponse("ok")
        else:
            return HttpResponse("error")
    except Exception:
        return render(request, 'formal/fourtofour.html')


def search_result(request):
    try:
        context = {}
        # 判断登入
        user_id = is_login(request)
        if user_id:
            context['no_login'] = 0
            context['login'] = 1
            context['user_id'] = user_id
            context['user_image'] = Users.objects.get(id=user_id).image
        else:
            context['no_login'] = 1
            context['login'] = 0

        # 判断是找书
        if request.method == 'GET':
            search_text = request.GET.get('search_text', default='')
            index = request.GET.get('index', default=1)
            book_author = Books.objects.filter(author__contains=search_text)
            book_name = Books.objects.filter(name__contains=search_text)

            article_title = Articles.objects.filter(title__contains=search_text)
            article_author = Articles.objects.filter(author__username__contains=search_text)
            article_text = Articles.objects.filter(text__contains=search_text)

            # for i in article_text:
            #     i.text = i.text[0: min(10, len(i.text))]
            # for i in article_author:
            #     i.text = i.text[0: min(10, len(i.text))]
            # for i in article_title:
            #     i.text = i.text[0: min(10, len(i.text))]

            if True:
                objects = book_name
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
                objects = article_title
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

            # 分页物件
            index = context['index1']
            try:
                p = Paginator(book_author, 6)
                context['book_author'] = p.page(int(index))
            except (EmptyPage, PageNotAnInteger):
                context['book_author'] = p.page(1)
            # context['book_author'] = book_author[(index-1)*6, min((index-1)*6, book_author.count())]

            index = context['index1']
            try:
                p = Paginator(book_name, 6)
                context['book_name'] = p.page(int(index))
            except (EmptyPage, PageNotAnInteger):
                context['book_name'] = p.page(1)
            # context['book_name'] = book_name[(index - 1) * 6, min((index - 1) * 6, book_name.count())]
            index = context['index2']
            try:
                p = Paginator(article_author, 5)
                context['article_author'] = p.page(int(index))
            except (EmptyPage, PageNotAnInteger):
                context['article_author'] = p.page(1)
            # context['article_author'] = article_author[(index - 1) * 6, min((index - 1) * 6, article_author.count())]
            index = context['index2']
            try:
                p = Paginator(article_title, 5)
                context['article_title'] = p.page(int(index))
            except (EmptyPage, PageNotAnInteger):
                context['article_title'] = p.page(1)
            # context['article_author'] = article_title[(index - 1) * 6, min((index - 1) * 6, article_title.count())]
            index = context['index2']
            try:
                p = Paginator(article_text, 5)
                context['article_text'] = p.page(int(index))
            except (EmptyPage, PageNotAnInteger):
                context['article_text'] = p.page(1)
            # context['article_author'] = article_text[(index - 1) * 6, min((index - 1) * 6, article_text.count())]

        return render(request, 'formal/search.html', context)
    except Exception:
        return render(request, 'formal/fourtofour.html')


def no_find(request):
    return render(request, 'formal/fourtofour.html')

