# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse, QueryDict
from django.views import View
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from datetime import datetime
from django.utils import timezone

# Create your views here.


def login(request):
    if request.method == 'POST':
        user_email = request.POST['email']
        user_password = request.POST['password']
        user = authenticate(username=user_email, password=user_password)
        if user is not None:
            django_login(request, user)
            request.session['username'] = user
            request.session['uid'] = User.objects.get(username=user).id
            # request.session.set_expiry(6000)
            return redirect(reverse('forum:posts'))
        else:
            return render(request, 'forum/login.html')
    return render(request, 'forum/login.html')


def logout(request):
    django_logout(request)
    return redirect(reverse('forum:login'))


def posts(request):
    if not request.user.is_authenticated:
        return redirect(reverse('forum:login'))
    posts_list = Post.objects.all().order_by('-id')
    post_paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')

    try:
        posts_list = post_paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        posts_list = post_paginator.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        posts_list = post_paginator.page(post_paginator.num_pages)

    post_transaction = Post.objects.filter(partition='Transaction').count()
    post_action = Post.objects.filter(partition='Activity').count()
    post_announcement = Post.objects.filter(partition='Announcement').count()
    post_chat = Post.objects.filter(partition='Chat').count()
    # user_name = User.objects.get(id=request.session.user_id).username
    return render(request, 'forum/posts.html', {'posts': posts_list,
                                                'post_transaction': post_transaction,
                                                'post_action': post_action,
                                                'post_announcement': post_announcement,
                                                'post_chat': post_chat
                                                })


class PostCreate(View):

    def post(self, request):
        post_owner = request.session['username']
        post = Post.objects.create(
            partition=request.POST.get('newPostPartition'),
            title=request.POST.get('newPostTitle'),
            content=request.POST.get('newPostContent'),
            owner=post_owner,
            time=timezone.now(),
        )
        return JsonResponse({
            'postID': post.id
        })


def post_detail(request, pid):
    post = Post.objects.get(id=pid)
    comments = post.comment_set.all()
    request.session['pid'] = pid
    return render(request, 'forum/post_detail.html', {'post': post,
                                                      'comments': comments})


class CommentCreate(View):

    def post(self, request):
        belong_post = Post.objects.get(id=request.session['pid'])
        comment_owner = request.session['username']
        comment = Comment.objects.create(
            post=belong_post,
            content=request.POST.get('newComment'),
            time=timezone.now(),
            owner=comment_owner
        )
        return JsonResponse({
            'comment_id': comment.id
        })


def profile(request, uid):
    user = User.objects.get(id=uid)
    avatar = user.get_avatar_url()
    return render(request, 'forum/profile.html', { 'avatar': avatar })