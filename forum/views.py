# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse, QueryDict
from django.views import View
from .models import Post


# Create your views here.
def posts(request):
    posts_list = Post.objects.all()
    return render(request, 'forum/posts.html', {'posts': posts_list})


class PostCreate(View):

    def post(self, request):
        post = Post.objects.create(
            partition=request.POST.get('newPostPartition'),
            title=request.POST.get('newPostTitle'),
            content=request.POST.get('newPostContent'),
        )
        return JsonResponse({
            'postID': post.id})

def post_detail(request, pid):
    post = Post.objects.get(id=pid)
    return render(request, 'forum/post_detail.html', {'post': post})