# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from djng.forms import NgModelFormMixin, NgFormValidationMixin, NgModelForm
from djng.styling.bootstrap3.forms import Bootstrap3Form, Bootstrap3FormMixin

from .models import Room


class RoomForm(NgModelFormMixin, Bootstrap3FormMixin, NgModelForm):
    scope_prefix = 'room'
    form_name = 'room_create'

    test = forms.CharField()

    def __init__(self, *args, **kwargs):
        # kwargs.update(scope_prefix='room')
        super(RoomForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Room
        exclude = ['slug', 'admin']
