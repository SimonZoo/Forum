# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^/$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.login, name='logout'),
    url(r'^signup/$', views.sigh_up, name='signup'),
    url(r'^posts/$', views.posts, name='posts'),
    url(r'^posts/chat/$', views.post_chat, name='post_chat'),
    url(r'^posts/activity/$', views.post_activity, name='post_activity'),
    url(r'^posts/announcement/$', views.post_announcement, name='post_announcement'),
    url(r'^posts/transaction/$', views.post_transaction, name='post_transaction'),
    url(r'^post_create/$', views.PostCreate.as_view(), name='post_create'),
    url(r'^comment_create/$', views.CommentCreate.as_view(), name='comment_create'),
    url(r'^post/(?P<pid>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^profile/(?P<uid>\d+)/$', views.profile, name='profile'),
    url(r'^search/$', views.search, name='search'),
    url(r'^upload/$', views.user_avatar_upload, name='user_avatar_upload'),
]