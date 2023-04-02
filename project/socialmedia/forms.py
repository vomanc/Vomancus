""" Forms """
from django.forms import ModelForm
from .models import TwitterModel, MediaTwitterModel


class TwitterModelForm(ModelForm):
    """ Form for TwitterModel """
    class Meta:
        model = TwitterModel
        fields = (
            'id', 'tweet_id', 'screen_name', 'user',
            'tweet_text', 'preview',
        )


class MediaTwitterModelForm(ModelForm):
    """ Create urls in MediaTwitterModel """
    class Meta:
        model = MediaTwitterModel
        fields = ("url",)
