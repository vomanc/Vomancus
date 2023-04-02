from django.urls import path
from . import views


urlpatterns = [
  path('', views.index, name='home'),
  path('about/', views.about, name='about'),
  path('account/<int:pk>', views.account, name='account'),
  path('signin/', views.signin, name='signin'),
  path('logout/', views.logout_, name='logout_'),
  path('signup/', views.signup, name='signup'),
  path('account-update/', views.account_update, name='account-update'),
  path('account-social/', views.SocialMediaDetailView.as_view(), name='social_media-update'),
  path('account-delete/', views.AccountDeleteView.as_view(), name='account-delete'),
  path('email-verification/<udb_64>/<token>/', views.verification_email, name='email-verification'),
  path('password/', views.change_password, name='password'),
]
