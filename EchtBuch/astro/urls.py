from django.urls import path

from . import views

urlpatterns = [
    path('search', views.search, name='search'),
    path('unfriend', views.unfriend, name='unfriend'),
    path('post_on_wall', views.post_on_wall, name='post_on_wall'),
    path('accept_friend_request', views.accept_friend_request, name='accept_friend_request'),
    path('deny_friend_request', views.deny_friend_request, name='deny_friend_request'),
    path('friend_request', views.friend_request, name='friend_request'),
    path('set_last_seen', views.set_last_seen, name='set_last_seen'),
    path('', views.index, name='index'),
    path('upload_profile_pic', views.upload_profile_pic, name='upload_profile_pic'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('signup', views.signup, name='signup'),
    path('process_signup', views.process_signup, name='process_signup'),
    path('login', views.login, name='login'),
    path('logout', views.process_logout, name='logout'),
    path('process_login', views.process_login, name='process_login'),
]
