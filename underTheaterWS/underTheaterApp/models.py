# vim: set fileencoding=utf-8 :
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from address.models import Address
from django.core.urlresolvers import reverse
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
    actors = models.ManyToManyField(Actor, verbose_name=u'actors')
    picture = models.FileField(upload_to="static/playImages")

    @property
    def day_function(self):
        return self.dayfunction_set

    @property
    def picture_url(self):
        return "%s%s" % (settings.MEDIA_URL, self.picture)

    def get_absolute_url(self):
        return reverse('underTheaterApp:playtheater_detail', args=[self.pk])

    def __str__(self):
        return u"%s" % self.play_name

    def __unicode__(self):
        return u"%s" % self.play_name


class DayFunction(models.Model):
    theater = models.ForeignKey(Theater, verbose_name=u'teatro',
                                related_name=u'day_function_theater')
    room_theater = models.ForeignKey(TheaterRoom,
                                     verbose_name=u'sala de la obra',
                                     related_name='day_function_room')
    datetime_show = models.DateTimeField(verbose_name=u'dia y horario de la funcion')

    play_theater = models.ForeignKey(PlayTheater, verbose_name=u'obra')

    def __unicode__(self):
        return u"%s %s %s" % (self.theater.name, self.room_theater.room_name,
                              self.datetime_show.strftime("%y-%m-%d %H:%M"))

    @property
    def tickets(self):
        return self.day_function_ticket


class Ticket(models.Model):
    ticket_name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    day_function = models.ForeignKey(DayFunction, verbose_name=u'day_function',
                                     related_name=u'day_function_ticket')

    def __str__(self):
        return u"%s" % self.ticket_name

    def __unicode__(self):
        return u"%s" % self.ticket_name
