from django.urls import path, include, re_path
from . import views


urlpatterns = [
  path('auth/', include('rest_framework.urls')),
  path('users-list/', views.AccountsListView.as_view()),
  path('user/<int:pk>/', views.AccountView.as_view()),
  path('auth/', include('djoser.urls')),
  re_path(r'^auth/', include('djoser.urls.authtoken')),
]
