from django.urls import path
from . import views


urlpatterns = [
  path('', views.index, name='social-media'),
  path('twitter', views.TwitterListViews.as_view(), name='twitter'),
  path('create-tweet', views.create_tweet, name='create-tweet'),
  path('tweet/<int:pk>', views.TweetDetailView.as_view(), name='tweet'),
  path('twitter-update/', views.auto_twitter, name='twitter-update'),
  path('my-translate/', views.MyTranslater.as_view(), name='my-translate'),
  path('tweet-clean/', views.twitter_clean, name='twitter-clean')
]
