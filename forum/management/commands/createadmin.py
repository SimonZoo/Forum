import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'create superuser directly'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        try:
            username = options['username']
            email = options['email']
            password = options['password']
        except KeyError:
            raise CommandError('username, email, password is all required')
        else:
            if User.objects.count() == 0:
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                )
                user.save()
            else:
                raise CommandError('superuser exists')
