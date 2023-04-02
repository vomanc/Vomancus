# Create your models here.
from django.db import models
from account.models import AccountsModel


class TwitterModel(models.Model):
    """ For tweets """
    owner = models.ForeignKey(AccountsModel, on_delete=models.CASCADE, related_name='owners')
    tweet_id = models.BigIntegerField('Tweet id')
    screen_name = models.CharField('Screen name', max_length=50)
    user = models.CharField('Username', max_length=250)
    tweet_text = models.CharField('Tweet', max_length=300, blank=True, null=True)
    preview = models.URLField('Preview', max_length=400, blank=True, null=True)

    class Meta:
        verbose_name = 'Tweet'
        ordering = ['-tweet_id']

    def __str__(self):
        return str(self.id)


class MediaTwitterModel(models.Model):
    """ For tweet media URL """
    owner = models.ForeignKey(TwitterModel, on_delete=models.CASCADE, related_name='media_url')
    url = models.URLField('URL', max_length=500)

    class Meta:
        verbose_name = 'Tweet_media_url'

    def __str__(self):
        return self.url
