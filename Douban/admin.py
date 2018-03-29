from django.contrib import admin
from .models import *

# Register your models here.


class UserCode(admin.ModelAdmin):
    list_display = ('username', 'activation_code', 'status')


admin.site.register(userActive, UserCode)
