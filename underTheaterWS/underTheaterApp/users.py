# vim: set fileencoding=utf-8 :
from __future__ import unicode_literals
from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=200, unique=True)
