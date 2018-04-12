from django.http import HttpResponse
from django.shortcuts import render
from .form import ArticleForm
# Create your views here.


def my_image(request, filename):
    image_data = open('media/pictures/' + filename, 'rb').read()
    return HttpResponse(image_data, content_type='image/png')


def test(request):
    form = ArticleForm()
    return render(request, 'test.html', {'form': form})
