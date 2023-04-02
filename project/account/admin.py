""" Register your models here. """
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AccountsModel, TwitterAPIModel


admin.site.register(AccountsModel, UserAdmin)
admin.site.register(TwitterAPIModel)
