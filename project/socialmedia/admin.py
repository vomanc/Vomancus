from django.contrib import admin
from .models import TwitterModel, MediaTwitterModel


class MediaTwitterInline(admin.TabularInline):
    """ MediaTwitter model Inline """
    model = MediaTwitterModel


class MediaTwitterRelated(admin.ModelAdmin):
    """ Show MediaTwitter in TwitterModel """
    inlines = [
        MediaTwitterInline,
    ]


admin.site.register(TwitterModel, MediaTwitterRelated)
admin.site.register(MediaTwitterModel)
