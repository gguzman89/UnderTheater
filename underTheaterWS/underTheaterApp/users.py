# vim: set fileencoding=utf-8 :
from __future__ import unicode_literals
from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return u"%s" % self.name

    def __unicode__(self):
        return u"%s" % self.name

