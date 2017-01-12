# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import random
import string

from awesome_rooms.models import Room
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, AbstractUser
from django.core import validators
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.crypto import salted_hmac
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class GameUser(AbstractUser):

    # username = models.CharField(
    #     _('username'), max_length=30, unique=True,
    #     help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    #     validators=[
    #         validators.RegexValidator(
    #             r'^[\w.@+-]+$',
    #             _('Enter a valid username. This value may contain only '
    #               'letters, numbers ' 'and @/./+/-/_ characters.')
    #         ),
    #     ],
    #     error_messages={
    #         'unique': _("A user with that username already exists."),
    #     },
    # )
    # first_name = models.CharField(_('first name'), max_length=30, blank=True)
    # last_name = models.CharField(_('last name'), max_length=30, blank=True)
    # email = models.EmailField(_('email address'), blank=True)

    is_guest = models.BooleanField(default=False)

    room = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL, related_name='users')
    is_admin = models.BooleanField(default=False)
    ready_to_play = models.BooleanField(default=False)

    login_token = models.CharField(max_length=256, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

    @property
    def token(self):
        self.login_token = get_random_string(length=32)
        self.save(update_fields=['login_token'])
        return self.login_token

    def save(self, *args, **kwargs):
        if not self.login_token:
            self.login_token = get_random_string(length=32)

        super(GameUser, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_session_auth_hash(self):
        key_salt = "awesome_users.models.GameUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.login_token).hexdigest()


    @staticmethod
    def create_guest():
        total_count = GameUser.objects.filter(is_guest=True).count()

        random_number = ''.join(random.choice(string.digits) for _ in range(5))
        random_username = "guest_" + random_number
        random_email = "guest_%s@awesomegame.pl" % random_number

        guard = 0
        while GameUser.objects.filter(username=random_username, email=random_email).exists():
            random_number = ''.join(random.choice(string.digits) for _ in range(5))
            random_username = "guest_" + random_number
            random_email = "guest_%s@awesomegame.pl" % random_number

            guard += 1
            if guard == 10:
                raise Exception('Nie mogę utworzyć unikalnego gracza gościa!')

        return GameUser.objects.create(
            username=random_username,
            email=random_email,
            password="!",
            is_guest=True,

        )
