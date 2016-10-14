# vim: set fileencoding=utf-8 :
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from address.models import Address
from django.core.urlresolvers import reverse
from users import Actor
from underTheaterApp.validators import periodic_date_validator, min_words_validator
from underTheaterApp.utils import convert_list_string
from polymorphic.models import PolymorphicModel


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
    email = models.EmailField()

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
    topic = models.CharField(max_length=30)


class PlayTheater(Ticketeable):
    play_name = models.CharField(max_length=200)
    synopsis = models.TextField(max_length=1000,
                                verbose_name="Sinopsis de la obra",
                                validators=[min_words_validator])
    actors = models.ManyToManyField(Actor, verbose_name=u'actors')
    picture = models.FileField(upload_to="static/playImages")

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
            raise ValidationError('%(since)s no puede ser mayor que %(until)s',
                                  params={'since': self.since,
                                          'until': self.until})

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

    @property
    def tickets(self):
        tickets = self.function_tickets
        if tickets.count() == 0:
            tickets = self.play_theater.play_tickets
        return tickets.all()


class Ticket(models.Model):
    ticket_name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    ticketeable = models.ForeignKey(Ticketeable, related_name="%(class)s_related", verbose_name=u'ticketeable')

    def __unicode__(self):
        return u"%s" % self.ticket_name
