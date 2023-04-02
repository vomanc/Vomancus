""" My serializers """
from rest_framework import serializers
from socialmedia.models import TwitterModel, MediaTwitterModel


class TwitterModelSerializers(serializers.ModelSerializer):
    """ Serializers for TwitterModel """
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TwitterModel
        fields = (
            'id', 'tweet_id', 'owner', 'screen_name', 'user',
            'tweet_text', 'preview', 'media_url'
        )


class MediaTwitterModelSerializers(serializers.ModelSerializer):
    """ Create urls in MediaTwitterModel """
    class Meta:
        model = MediaTwitterModel
        fields = ("owner", "url")
