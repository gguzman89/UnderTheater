# vim: set fileencoding=utf-8 :
from __future__ import unicode_literals
from django.db import models
from address.models import Address
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse


class Contact(models.Model):
    number_phone = models.IntegerField(verbose_name=u'Numero de telefono')
    facebook = models.CharField(max_length=128, blank=True,
                                verbose_name=u'usuario en Facebook')
    address = models.OneToOneField(Address, verbose_name=u'address',
                                   related_name=u'address_contact')
    share_address = models.BooleanField(default=True,
                                        verbose_name=u"Compartir direccion",
                                        blank=False, null=False,
                                        help_text=u"Compartir la direccion")
    email = models.EmailField()

    def __str__(self):
        return u"%s" % self.pk

    def __unicode__(self):
        return u"%s" % self.address


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    facebook = models.CharField(max_length=128, blank=True,
                                verbose_name=u'usuario en Facebook')
    twitter = models.CharField(max_length=128, blank=True,
                                verbose_name=u'twitter')
    photo = models.FileField(upload_to="static/profileImages",
                             default='static/logo.png')

    @property
    def photo_url(self):
        return "%s%s" % (settings.MEDIA_URL, self.photo)

    def facebook_url(self):
        return "//facebook.com/%s" % self.facebook

    def twitter_url(self):
        return "//twitter.com/%s" % self.twitter

    @property
    def get_complete_name(self):
        return u"%s %s" % (self.name, self.surname)

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.pk})

    def __unicode__(self):
        return self.get_complete_name


class Actor(Profile):
    def get_role(self):
        return u"Actor"


class OwnerTheater(Profile):
    def get_role(self):
        return u"Dueño del teatro"


class Spectators(Profile):
    def get_role(self):
        return u"Espectador"
