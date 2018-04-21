import os

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
# Create your models here.


AVATAR_ROOT = 'forum/media/avatar'
AVATAR_DEFAULT = os.path.join(AVATAR_ROOT, 'default.png')


class Post(models.Model):
    PARTITION = (
        ('Chat', 'Chat'),
        ('Announcement', 'Announcement'),
        ('Transaction', 'Transaction'),
        ('Activity', 'Activity'),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    partition = models.CharField(max_length=50, choices=PARTITION, default='Chat')
    owner = models.ForeignKey(User)
    # owner = models.CharField(max_length=100, default='User')
    content = models.CharField(max_length=1000, blank=True)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, default='New Comment')
    time = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User)
    # owner = models.CharField(max_length=100, default='User')

    def __str__(self):
        return str(self.id)


class Profile(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=20, blank=True, null=True, default='your nickname')
    avatar = models.ImageField(upload_to=AVATAR_ROOT)

    def set_avatar_url(self, src_path):
        print(self.avatar.url)
        old_path = os.path.join(settings.BASE_DIR, self.avatar.url)  # 旧的头像路径
        old_filename = os.path.splitext(os.path.split(old_path)[-1])[0]

        try:
            # 获得起始编号
            start_num = int(old_filename.split('_')[-1]) + 1
        except Exception as e:
            # avatar = Profile(user=self)
            start_num = 0
            # old_path = ''
        print(src_path, 'src!')
        # 根据user id设置新的头像名称
        filename = os.path.split(src_path)[-1]
        img_format = os.path.splitext(filename)[-1]
        print(filename)

        # while True:
        #     new_filename = '%s_64_%s%s' % (self.id, start_num, img_format)
        #     new_path = os.path.join(settings.BASE_DIR, AVATAR_ROOT, new_filename)
        #     if not os.path.isfile(new_path):
        #         break
        #     start_num += 1

        # 保存头像
        # shutil.copy(new_path, src_path)
        self.avatar = os.path.join(AVATAR_ROOT, filename)
        self.save()

        # 删除旧文件
        # if os.path.isfile(old_path):
        #     os.remove(old_path)
        return self


def get_avatar_url(self):
    try:
        user_profile = Profile.objects.get(user=self.id)
        return user_profile.avatar
    except Exception as e:
        return AVATAR_DEFAULT
