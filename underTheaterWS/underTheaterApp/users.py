# vim: set fileencoding=utf-8 :
from __future__ import unicode_literals
from django.db import models
from address.models import Address
from django.contrib.auth.models import User


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
        return u"%s" % self.pk


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    facebook = models.CharField(max_length=128, blank=True,
                                verbose_name=u'usuario en Facebook')
    twitter = models.CharField(max_length=128, blank=True,
                                verbose_name=u'twitter')

    def __unicode__(self):
        return u"%s %s" % (self.name, self.surname)


class Actor(Profile):
    pass


class OwnerTheater(Profile):
    pass


class Spectators(Profile):
    pass
