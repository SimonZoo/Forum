# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse, QueryDict
from django.views import View
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def posts(request):
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
    return render(request, 'forum/posts.html', {'posts': posts_list,
                                                'post_transaction': post_transaction,
                                                'post_action': post_action,
                                                'post_announcement': post_announcement,
                                                'post_chat': post_chat})


class PostCreate(View):

    def post(self, request):
        post = Post.objects.create(
            partition=request.POST.get('newPostPartition'),
            title=request.POST.get('newPostTitle'),
            content=request.POST.get('newPostContent'),
        )

        return JsonResponse({
            'postID': post.id
        })


def post_detail(request, pid):
    post = Post.objects.get(id=pid)
    return render(request, 'forum/post_detail.html', {'post': post})