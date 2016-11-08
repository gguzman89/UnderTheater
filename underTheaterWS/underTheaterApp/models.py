# vim: set fileencoding=utf-8 :
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from users import Actor, Contact, OwnerTheater
from underTheaterApp.validators import periodic_date_validator, min_words_validator
from underTheaterApp.utils import convert_list_string
from underTheaterApp.managers import PlayTheaterManager
from polymorphic.models import PolymorphicModel


class Theater(models.Model):
    name = models.CharField(max_length=200, unique=True)
    review = models.TextField(max_length=500,
                              verbose_name=u"reseña del teatro")
    contact = models.OneToOneField(Contact, verbose_name=u'contacto',
                                   related_name=u'theater_contact')
    owner = models.OneToOneField(OwnerTheater, verbose_name=u'dueño',
                                   related_name=u'owner',
                                   primary_key=True)

    def __unicode__(self):
        return u"%s" % self.name


class TheaterRoom(models.Model):
    theater = models.ForeignKey(Theater, verbose_name=u'theater',
                                related_name=u'theater_room')
    capacity = models.IntegerField(verbose_name=u'cantidad de asientos libres')
    room_name = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % self.room_name


class Ticketeable(PolymorphicModel):
    topic = models.CharField(max_length=250)

    def __unicode__(self):
        return u"%s" % self.topic


class PlayTheater(Ticketeable):
    play_name = models.CharField(max_length=200)
    synopsis = models.TextField(max_length=1000,
                                verbose_name="Sinopsis de la obra",
                                validators=[min_words_validator])
    actors = models.ManyToManyField(Actor, verbose_name=u'actors')
    picture = models.FileField(upload_to="static/playImages")
    objects = PlayTheaterManager()

    @property
    def day_function(self):
        return self.dayfunction_related

    @property
    def picture_url(self):
        return "%s%s" % (settings.MEDIA_URL, self.picture)

    def get_absolute_url(self):
        return reverse('underTheaterApp:playtheater_detail', args=[self.pk])

    def tickets(self):
        return self.ticket_related.all()

    def all_actors(self):
        return self.actors.all()

    def day_functions(self):
        return self.day_function.all()

    def get_address(self, theater_name):
        theater = self.objects.filter(day_function__theater__name=theater_name)[0]
        return theater.contact.raw

    def __unicode__(self):
        return u"%s" % self.play_name


class DateTimeFunction(models.Model):
    date_format = '%d/%m/%Y'
    hour = models.CharField(max_length=300)
    until = models.DateField(null=True, blank=True)
    since = models.DateField()
    periodic_date = models.CharField(max_length=200,
                                     validators=[periodic_date_validator],
                                     null=True, blank=True)

    def clean(self):
        if not self.until and self.periodic_date:
            raise ValidationError('No podes tener un dia periodico si la fecha es unica')

        if self.until and self.since > self.until:
            date_format = '%d/%m/%Y'
            raise ValidationError('Desde "%(since)s" no puede ser mayor que hasta "%(until)s"',
                                  params={'since': self.since.strftime(date_format),
                                          'until': self.until.strftime(date_format)})

    def hours(self):
        return convert_list_string(self.hour)

    def periodic_dates(self):
        return convert_list_string(self.periodic_date or "[]")

    def __unicode__(self):
        return u"%s %s" % (self.id, self.since.strftime("%d-%m-%Y"))


class DayFunction(Ticketeable):
    theater = models.ForeignKey(Theater, verbose_name=u'teatro',
                                related_name=u'day_function_theater')
    room_theater = models.ForeignKey(TheaterRoom,
                                     verbose_name=u'sala de la obra',
                                     related_name='day_function_room')
    datetime_function = models.OneToOneField(DateTimeFunction,
                                             verbose_name=u'dia y horario de la funcion')

    play_theater = models.ForeignKey(PlayTheater, related_name="%(class)s_related", verbose_name=u'obra')

    def __unicode__(self):
        return u"%s %s" % (self.theater.name, self.room_theater.room_name)

    def tickets(self):
        tickets = self.ticket_related
        if tickets.count() == 0:
            tickets = self.play_theater.ticket_related
        return tickets.all()


class Ticket(models.Model):
    ticket_name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    ticketeable = models.ForeignKey(Ticketeable, related_name="%(class)s_related", verbose_name=u'ticketeable')

    def __unicode__(self):
        return u"%s" % self.ticket_name
