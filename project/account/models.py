""" Create your models here. """
from django.db import models
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete, pre_save


class AccountsModel(AbstractUser):
    """ Create user profile """
    GENDERS = (
        ('male', 'male'),
        ('woman', 'woman')
    )
    confirm_email = models.BooleanField(default=False)
    gender = models.CharField('Gender', max_length=5, choices=GENDERS, default='-')
    twitter = models.CharField('Twitter', max_length=50, default='@', blank=True, null=True)
    mastodon = models.CharField('Mastodon', max_length=50, default='@', blank=True, null=True)
    signal = models.CharField('Signal', max_length=15, default='+', blank=True, null=True)
    github = models.CharField('Github', max_length=50, default='@', blank=True, null=True)
    telegram = models.CharField('Telegram', max_length=50, default='@', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d', blank=True, null=True)

    REQUIRED_FIELDS = ['email']

    class Meta:
        constraints = [models.UniqueConstraint(fields=('email',), name='email_unique')]
        verbose_name = 'Account'

    def __str__(self):
        return self.username


@receiver(pre_delete, sender=AccountsModel)
def delete_image_pre_delete(sender, instance, **kwargs):
    """ To delete the file itself """
    if instance.avatar:
        instance.avatar.delete(False)


@receiver(pre_save, sender=AccountsModel)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = AccountsModel.objects.get(pk=instance.pk).avatar
    except Exception:
        return False

    new_file = instance.avatar
    if old_file != new_file:
        try:
            import os
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        except ValueError:
            pass


class TwitterAPIModel(models.Model):
    """ API keys for twitter """
    owner = models.ForeignKey(AccountsModel, on_delete=models.CASCADE, default='Twitter API',
                              related_name='twitter_api')
    consumer_key = models.CharField('Consumer key', max_length=250)
    consumer_secret = models.CharField('Consumer secret', max_length=250)
    access_token = models.CharField('Access token', max_length=250)
    access_token_secret = models.CharField('Access token secret', max_length=250)

    class Meta:
        verbose_name = 'API KEY'

    def __str__(self):
        return str(self.owner)
