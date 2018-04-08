from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def my_image(request, filename):
    image_data = open('media/pictures/' + filename, 'rb').read()
    return HttpResponse(image_data, content_type='image/png')
