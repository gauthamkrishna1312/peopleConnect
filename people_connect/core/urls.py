from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('upload', views.upload, name='upload'),
    path('account/<str:usnm>', views.account, name='account'),
    path('accounts_settings', views.accounts_settings, name='settings'),
    path('like-post', views.like, name='like-post'),
    path('logout', views.logout, name='logout'),
]