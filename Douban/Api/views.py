from django.template.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render

#对request加csrftoken并返回
def getCsrf(request):
    csrf_tok=csrf(request)
    csrf_token=str(csrf_tok.get("csrf_token"))
    return HttpResponse(csrf_token,content_type="application/json")

