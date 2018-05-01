import json
import os
import uuid

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.http import JsonResponse, HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from PIL import Image

from .models import Post, Comment, Profile

# Create your views here.


def get_post_number():
    posts = Post.objects.all().count()
    post_transaction = Post.objects.filter(partition='Transaction').count()
    post_action = Post.objects.filter(partition='Activity').count()
    post_announcement = Post.objects.filter(partition='Announcement').count()
    post_chat = Post.objects.filter(partition='Chat').count()
    arr = {
        'all': posts,
        'chat': post_chat,
        'transaction': post_transaction,
        'action': post_action,
        'announcement': post_announcement
    }
    return arr


def login(request):
    if request.method == 'POST':
        user_email = request.POST['email']
        user_password = request.POST['password']
        user = authenticate(username=user_email, password=user_password)
        if user is not None:
            django_login(request, user)
            nickname = user.profile.nickname
            request.session['username'] = nickname
            request.session['uid'] = user.id
            print(user.id)
            # request.session.set_expiry(6000)
            return redirect(reverse('forum:posts'))
        else:
            print('error')
            return render(request, 'forum/login.html')
    return render(request, 'forum/login.html')


def logout(request):
    django_logout(request)
    return redirect(reverse('forum:login'))


def sign_up(request):
    if request.method == 'POST':
        new_user = User.objects.create_user(
            username=request.POST.get('newAccountEmail'),
            password=request.POST.get('newAccountPassword')
        )
        Profile.objects.create(
            user=new_user,
            nickname=request.POST.get('newAccountName'),
        )
        print(request.POST.get('newAccountName'))
        return JsonResponse({"create_user": "yes"})


def posts(request):
    if not request.user.is_authenticated:
        return redirect(reverse('forum:login'))
    posts_list = Post.objects.all().order_by('-id')

    post_number = posts_list.__len__()

    post_paginator = Paginator(posts_list, 7)
    page = request.GET.get('page')
    try:
        posts_list = post_paginator.page(page)
    except PageNotAnInteger:
        # show first page if input page is not int
        posts_list = post_paginator.page(1)
    except EmptyPage:
        # show last page if input page is too large
        posts_list = post_paginator.page(post_paginator.num_pages)

    array = get_post_number()
    print(array)
    # user_name = User.objects.get(id=request.session.user_id).username
    return render(request, 'forum/posts.html', {'posts': posts_list,
                                                'post_number': array
                                                })


def post_chat(request):
    if not request.user.is_authenticated:
        return redirect(reverse('forum:login'))
    posts_list = Post.objects.filter(partition='Chat')
    array = get_post_number()
    return render(request, 'forum/posts.html', {'posts': posts_list,
                                                'post_number': array})


def post_transaction(request):
    if not request.user.is_authenticated:
        return redirect(reverse('forum:login'))
    posts_list = Post.objects.filter(partition='Transaction')
    array = get_post_number()
    return render(request, 'forum/posts.html', {'posts': posts_list,
                                                'post_number': array})


def post_announcement(request):
    if not request.user.is_authenticated:
        return redirect(reverse('forum:login'))
    posts_list = Post.objects.filter(partition='Announcement')
    array = get_post_number()
    return render(request, 'forum/posts.html', {'posts': posts_list,
                                                'post_number': array})


def post_activity(request):
    if not request.user.is_authenticated:
        return redirect(reverse('forum:login'))
    posts_list = Post.objects.filter(partition='Activity')
    array = get_post_number()
    return render(request, 'forum/posts.html', {'posts': posts_list,
                                                'post_number': array})


class PostCreate(View):

    def post(self, request):
        post_owner = request.session['username']
        user = User.objects.get(id=request.session['uid'])
        post = Post.objects.create(
            partition=request.POST.get('newPostPartition'),
            title=request.POST.get('newPostTitle'),
            content=request.POST.get('newPostContent'),
            owner=user,
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
        user = User.objects.get(id=request.session['uid'])
        comment = Comment.objects.create(
            post=belong_post,
            content=request.POST.get('newComment'),
            time=timezone.now(),
            owner=user
        )
        return JsonResponse({
            'comment_id': comment.id
        })


def profile(request, uid):
    if not request.user.is_authenticated:
        return redirect(reverse('forum:login'))
    user = User.objects.get(id=uid)
    avatar = user.profile.avatar
    nickname = user.profile.nickname
    email = user.username
    my_post = Post.objects.filter(owner=user)
    my_comment = Comment.objects.filter(owner=user)
    return render(request, 'forum/profile.html', {'avatar': avatar,
                                                  'nickname': nickname,
                                                  'email': email,
                                                  'my_post': my_post,
                                                  'my_comment': my_comment})


def search(request):
    if not request.user.is_authenticated:
        return redirect(reverse('forum:login'))
    content = request.GET.get('search')
    posts_list = Post.objects.filter(title__icontains=content)
    post_number = get_post_number()
    # posts_list.exclude(Post.objects.filter(content__icontains=content))
    return render(request, 'forum/search.html', {'results': posts_list,
                                                 'post_number': post_number})


def user_avatar_upload(request):
    if request.method == 'POST':
        data = {}
        if 'avatar_file' in request.FILES:
            # upload
            avatar_file = request.FILES['avatar_file']
            temp_folder = os.path.join(settings.BASE_DIR, 'forum/static/forum/media', 'avatar')
            print(settings.BASE_DIR, 'base')
            if not os.path.isdir(temp_folder):
                os.makedirs(temp_folder)

            temp_filename = uuid.uuid1().hex + os.path.splitext(avatar_file.name)[-1]
            temp_path = os.path.join(temp_folder, temp_filename)

            # save file
            with open(temp_path, 'wb') as f:
                for chunk in avatar_file.chunks():
                    f.write(chunk)
            try:
                top = int(float(request.POST['avatar_y']))
                buttom = top + int(float(request.POST['avatar_height']))
                left = int(float(request.POST['avatar_x']))
                right = left + int(float(request.POST['avatar_width']))
            except:
                top = 10
                buttom = 10
                left = 10
                right = 10
            im = Image.open(temp_path)
            # adjust file
            crop_im = im.convert("RGBA").crop((left, top, right, buttom)).resize((64, 64), Image.ANTIALIAS)

            # background color is white
            out = Image.new('RGB', crop_im.size, (255, 255, 255))
            out.paste(crop_im, (0, 0, 64, 64), crop_im)

            # save avatar
            out.save(temp_path)

            # save recorder
            avatar = request.user.profile.set_avatar_url(temp_path)
            # os.remove(temp_path)

            data['success'] = True
            data['avatar_url'] = avatar.avatar.url
            return HttpResponse(json.dumps(data), content_type="application/json")
