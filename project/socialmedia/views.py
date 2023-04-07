import json
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.contrib import messages
from django.http import JsonResponse
from pylingva import pylingva
from account.models import TwitterAPIModel
from .forms import TwitterModelForm, MediaTwitterModelForm
from .models import TwitterModel, MediaTwitterModel
from .utils import twitter_api


def index(requests):
    """ Home page for Social Media"""
    return render(requests, 'socialmedia/social.html')


class TwitterListViews(LoginRequiredMixin, ListView):
    """ List of Tweets """
    paginate_by = 10
    template_name = 'socialmedia/twitter.html'
    context_object_name = 'tweets_list'

    def get_queryset(self):
        return TwitterModel.objects.filter(owner=self.request.user.id).select_related()


class TweetDetailView(LoginRequiredMixin, DetailView):
    """ Tweet view """
    login_url = 'signin'
    model = TwitterModel
    template_name = 'socialmedia/get_tweet.html'
    context_object_name = 'tweet'


@login_required(login_url='signin')
def create_tweet(request):
    """ Create and publication New """
    media_twitter_model_form_set = formset_factory(MediaTwitterModelForm, max_num=4, extra=1)

    if request.method == 'POST':
        tweet_form = TwitterModelForm(request.POST, request.FILES)
        media_form = media_twitter_model_form_set(request.POST)

        if tweet_form.is_valid() and media_form.is_valid():
            tweet = tweet_form.save(commit=False)
            tweet.owner = request.user
            tweet.save()
            # Save media url
            for instance in media_form:
                instance = instance.save(commit=False)
                if instance.url:
                    instance.owner = tweet_form.instance
                    instance.save()
            return redirect('twitter')
        messages.error(request, 'Form error')

    context = {
        "tweet_form": TwitterModelForm(),
        "media_form": media_twitter_model_form_set()
    }
    return render(request, 'socialmedia/create_twitter.html', {"context": context})


@login_required(login_url='signin')
def twitter_clean(request):
    """ For delete all user's tweets """
    TwitterModel.objects.filter(owner=request.user.id).select_related().delete()
    messages.success(request, "Successful twitter cleanup")
    return redirect('twitter')


@login_required(login_url='signin')
def auto_twitter(request):
    """ Automatic twitter update """
    def media_sort(resp, med_list):
        """ Preparing data for sending media links """
        media_data = {}
        for i in resp:
            media_data.update({i.tweet_id: i.id})

        data = []
        for media in med_list:
            id_media = list(media)[0]
            id_media = media_data[id_media]
            url_media = list(media.values())[0]
            data.append({"owner": id_media, "url": url_media})
        return data

    if request.method == 'GET':
        api_keys = TwitterAPIModel.objects.filter(owner__id=request.user.id)
        # if not API Key
        if api_keys.exists() is False:
            messages.error(request, 'You need to add an API key')
            return redirect('social_media-update')

        twitter_list, media_list = twitter_api(api_keys.get(), '200')
        if twitter_list is None:
            messages.error(request, media_list)
            return redirect('twitter')
        # Add Tweets
        objs = TwitterModel.objects.bulk_create([
            TwitterModel(
                owner=request.user,
                tweet_id=i['tweet_id'],
                screen_name=i['screen_name'],
                user=i['user'],
                tweet_text=i['tweet_text'],
                preview=i['preview_url'],
            ) for i in twitter_list
        ])
        # Add Media
        media_list = media_sort(objs, media_list)
        MediaTwitterModel.objects.bulk_create([
            MediaTwitterModel(
                owner_id=i['owner'],
                url=i['url'],
            ) for i in media_list
        ])
        messages.success(request, 'Twitter successfully updated')
    return redirect('twitter')


class MyTranslater(View):
    """ Translater """
    def get(self, request, format=None):
        return JsonResponse({'num': 1})

    def post(self, request):
        lang = request.META['HTTP_ACCEPT_LANGUAGE'].split('-')[0]
        text = json.loads(request.body)
        trans = pylingva()
        tr_txt = trans.translate(
            "auto", lang, text.replace('_', ' ').replace('/', ' ').replace('#', ' '))
        return JsonResponse({'text': tr_txt})
