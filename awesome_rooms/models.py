# -*- coding: utf-8 -*-
import itertools

from awesome_staff.fields import IntegerRangeField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.translation import ugettext as _


@python_2_unicode_compatible
class AbstractRoom(models.Model):

    name = models.CharField("Nazwa pokoju", max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    max_players = IntegerRangeField("Maksymalna liczba graczy", default=4, min_value=2, max_value=6)

    class Meta:
        db_table = 'rooms'
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.pk:
            self.slug = orig = slugify(self.name)

            for x in itertools.count(1):
                if not self.__class__.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (orig, x)

        return super(AbstractRoom, self).save(*args, **kwargs)
