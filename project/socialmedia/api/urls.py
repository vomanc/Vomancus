from django.urls import path
from . import views


urlpatterns = [
  path('twitter/', views.TwitterView.as_view()),
  path('tweet-create/', views.TweetCreateView.as_view()),
  path('tweet-media/', views.MediaTwitterModelView.as_view()),
  path('tweet-clean/', views.ClearTwitter.as_view()),
  path('tweet-update/', views.auto_twitter),
]
