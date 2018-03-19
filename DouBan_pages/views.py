from django.shortcuts import render
from Users.models import Articles, Users, Books
# Create your views here.
def home_page(request):
    passage_list = Articles.objects.order_by('good_num')
    