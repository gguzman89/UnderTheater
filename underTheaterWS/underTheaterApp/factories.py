# vim: set fileencoding=utf-8 :
import factory
from factory.django import DjangoModelFactory
from underTheaterApp import models
from datetime import datetime
from address.models import Address


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address
    raw = factory.Sequence(lambda n: 'address %s' % n)


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


class DateTimeShowFactory(DjangoModelFactory):
    class Meta:
        model = models.DateTimeShow

    datetime_show = datetime.today()


class PlayPriceFactory(DjangoModelFactory):
    class Meta:
        model = models.PlayPrice

    price_name = factory.Sequence(lambda n: 'price_name %s' % n)
    price = factory.Sequence(lambda n: '$ %s' % n)


class PlayTheaterFactory(DjangoModelFactory):
    class Meta:
        model = models.PlayTheater

    play_name = factory.Sequence(lambda n: 'play_theater %s' % n)
    synopsis = "This isn't a synopsis"
    theater = factory.RelatedFactory(TheaterFactory)
    room_theater = factory.RelatedFactory(RoomTheaterFactory)
    actors = factory.RelatedFactory(ActorFactory)
    picture = factory.django.ImageField(color='blue')
    datetime_show = factory.RelatedFactory(DateTimeShowFactory)
    price = factory.RelatedFactory(PlayPriceFactory)
