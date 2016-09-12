# vim: set fileencoding=utf-8 :
from __future__ import unicode_literals
from django.db import models
from address.models import Address
from users import Actor


class Contact(models.Model):
    number_phone = models.IntegerField(verbose_name=u'Numero de telefono')
    facebook = models.CharField(max_length=128, blank=True,
                                verbose_name=u'usuario en Facebook')
    address = models.OneToOneField(Address, verbose_name=u'address',
                                   related_name=u'address_contact',
                                   )

    share_address = models.BooleanField(default=True,
                                        verbose_name=u"Compartir direccion",
                                        blank=False, null=False,
                                        help_text=u"Compartir la direccion")

    def __str__(self):
        return u"%s" % self.pk

    def __unicode__(self):
        return u"%s" % self.pk


class Theater(models.Model):
    name = models.CharField(max_length=200, unique=True)
    review = models.TextField(max_length=500,
                              verbose_name=u"reseña del teatro")
    contact = models.OneToOneField(Contact, verbose_name=u'contacto',
                                   related_name=u'theater_contact',
                                   primary_key=True)

    def __str__(self):
        return u"%s" % self.name

    def __unicode__(self):
        return u"%s" % self.name


class TheaterRoom(models.Model):
    theater = models.ForeignKey(Theater, verbose_name=u'theater',
                                related_name=u'theater_room')
    capacity = models.IntegerField(verbose_name=u'cantidad de asientos libres')
    room_name = models.CharField(max_length=200)

    def __str__(self):
        return u"%s" % self.room_name

    def __unicode__(self):
        return u"%s" % self.room_name


class PlayPrice(models.Model):
    price_name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)

    def __str__(self):
        return u"%s" % self.price_name

    def __unicode__(self):
        return u"%s" % self.price_name


class DateTimeShow(models.Model):
    datetime_show = models.DateTimeField(verbose_name=u'dia y horario del show')

    def __str__(self):
        return u"%s" % self.datetime_show.strftime("%y-%m-%d %H:%M")

    def __unicode__(self):
        return u"%s" % self.datetime_show.strftime("%y-%m-%d %H:%M")


class PlayTheater(models.Model):
    play_name = models.CharField(max_length=200)
    synopsis = models.TextField(max_length=500,
                                verbose_name="Sinopsis de la obra")
    theater = models.ManyToManyField(Theater, verbose_name=u'theater',
                                     related_name=u'play_theater')
    room_theater = models.ManyToManyField(TheaterRoom,
                                          verbose_name=u'sala de la obra',
                                          related_name='room')
    actors = models.ManyToManyField(Actor, verbose_name=u'actors')
    picture = models.ImageField(upload_to="static/playImages")
    datetime_show = models.ManyToManyField(DateTimeShow,
                                           verbose_name=u'datetime_show')
    price = models.ManyToManyField(PlayPrice, verbose_name=u'price',
                                   related_name=u'play_price')

    def __str__(self):
        return u"%s" % self.play_name

    def __unicode__(self):
        return u"%s" % self.play_name
