# vim: set fileencoding=utf-8 :
import os
import factory
from factory.django import DjangoModelFactory
from underTheaterApp import models
from datetime import date, timedelta
from address.models import Address
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from underTheaterApp.users import OwnerTheater


TEST_IMAGE = os.path.join(os.path.dirname("static/"), 'test.png')


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address

    raw = factory.Sequence(lambda n: 'address %s' % n)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: 'miEmail%s@midominio.com' % n)
    username = factory.Sequence(lambda n: 'miusername%s' % n)
    password = make_password('miPassword')


class OwnerTheaterFactory(DjangoModelFactory):

    class Meta:
        model = OwnerTheater

    name = factory.Sequence(lambda n: 'name%s' % n)
    surname = factory.Sequence(lambda n: 'surname%s' % n)
    twitter = factory.Sequence(lambda n: 'twitter%s' % n)
    facebook = factory.Sequence(lambda n: 'facebook%s' % n)
    user = factory.SubFactory(UserFactory)


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = models.Contact

    number_phone = factory.Sequence(lambda n: n)
    facebook = "My Facebook"
    address = factory.SubFactory(AddressFactory)
    share_address = True


class TheaterFactory(DjangoModelFactory):
    class Meta:
        model = models.Theater

    name = factory.Sequence(lambda n: 'name-theater%s' % n)
    review = "This isn't a review"
    contact = factory.SubFactory(ContactFactory)
    owner = factory.SubFactory(OwnerTheaterFactory)


class RoomTheaterFactory(DjangoModelFactory):
    class Meta:
        model = models.TheaterRoom

    theater = factory.SubFactory(TheaterFactory)
    capacity = factory.Sequence(lambda n: n)
    room_name = factory.Sequence(lambda n: 'room_name %s' % n)


class ActorFactory(DjangoModelFactory):
    class Meta:
        model = models.Actor

    name = factory.Sequence(lambda n: 'actor%s' % n)


class DateTimeFunctionFactory(DjangoModelFactory):
    class Meta:
        model = models.DateTimeFunction
    hour = "8:30"
    until = date.today() + timedelta(days=3)
    since = date.today()
    periodic_date = ["Lunes", "Martes"]


class PlayTheaterFactory(DjangoModelFactory):
    class Meta:
        model = models.PlayTheater

    play_name = factory.Sequence(lambda n: 'play_theater %s' % n)
    synopsis = "This isn't a synopsis"
    actors = factory.RelatedFactory(ActorFactory)
    picture = File(open(TEST_IMAGE))


class DayFunctionFactory(DjangoModelFactory):
    class Meta:
        model = models.DayFunction

    theater = factory.SubFactory(TheaterFactory)
    room_theater = factory.SubFactory(RoomTheaterFactory)
    play_theater = factory.SubFactory(PlayTheaterFactory)


class TicketFactory(DjangoModelFactory):
    class Meta:
        model = models.Ticket

    ticket_name = factory.Sequence(lambda n: 'play_theater %s' % n)
    price = factory.Sequence(lambda n: 'play_theater %s' % n)
