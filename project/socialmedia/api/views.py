import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import generics
from socialmedia.models import TwitterModel, MediaTwitterModel
from account.models import TwitterAPIModel
from socialmedia.utils import twitter_api
from .serializers import TwitterModelSerializers, MediaTwitterModelSerializers


class TwitterView(generics.ListAPIView):
    """
    GET tweet list [params = {'twitter_list': 'True'}]
    OR
    GET tweet [params = {'tweet': '50'}]
    """
    serializer_class = TwitterModelSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        if self.request.query_params.get('twitter_list', None) == 'True':
            return TwitterModel.objects.filter(owner__id=self.request.user.id)
        if self.request.query_params.get('tweet', None) is not None:
            return TwitterModel.objects.filter(id=self.request.query_params.get('tweet'))
        return None


class TweetCreateView(generics.ListCreateAPIView):
    """ Create Tweet """
    queryset = TwitterModel.objects.all()
    serializer_class = TwitterModelSerializers
    permission_classes = [IsAuthenticated]


class MediaTwitterModelView(generics.ListCreateAPIView):
    """ Create TweetMedia """
    queryset = MediaTwitterModel.objects.all()
    serializer_class = MediaTwitterModelSerializers
    permission_classes = [IsAuthenticated]


class ClearTwitter(APIView):
    """ Clear user's tweets """
    queryset = TwitterModel.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Return a list of all users """
        return TwitterModel.objects.filter(owner__id=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        """
        Call the delete method on the fetched object and then redirect to the
        success URL.
        """
        self.get_queryset().delete()
        return Response({"message": "Successful twitter cleanup"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def auto_twitter(request, format=None):
    """ Automatic twitter update by api """
    def response_decode(data):
        """ Decoding the response to determine the ID """
        data = JSONRenderer().render(data).decode()
        data = json.loads(data)
        id_list = {}
        for i in data:
            id_list.update({i['tweet_id']: i['id']})
        return id_list

    def media_sort(resp, med_list):
        """ Preparing data for sending media links """
        data = []
        for media in med_list:
            id_media = list(media)[0]
            id_media = resp[int(id_media)]
            url_media = list(media.values())[0]
            data.append({"owner": id_media, "url": url_media})
        return data

    if request.method == 'GET':
        api_keys = get_object_or_404(TwitterAPIModel, owner__id=request.user.id)
        twitter_list, media_list = twitter_api(api_keys, '200')
        if twitter_list is False:
            return Response({'content': 'Rate limit exceeded'})
        # Send Tweets
        serializer = TwitterModelSerializers(
            data=twitter_list, many=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = response_decode(serializer.data)
            # Send Media
            media_data = media_sort(response, media_list)
            serializer = MediaTwitterModelSerializers(
                data=media_data, many=True, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({'content': 'True'})
        return Response({'content': serializer.errors})
    return Response({'content': 'only GET'})
