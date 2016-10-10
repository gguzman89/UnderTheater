# vim: set fileencoding=utf-8 :
from django.test import TestCase
from datetime import date, time, timedelta
from underTheaterApp.factories import TheaterFactory, RoomTheaterFactory,\
    PlayTheaterFactory, TicketFactory
from underTheaterApp.models import DayFunction, OnlyDate, PeriodicDate


class PlayTheaterTestCase(TestCase):

    def test_play_theater_creation(self):
        self.assertTrue(True)


class DayFunctionTest(TestCase):

    def test_create_day_function_with_only_date(self):
        theater = TheaterFactory.create()
        room_theater = RoomTheaterFactory(theater=theater)
        play_theater = PlayTheaterFactory.create()
        only_date = OnlyDate(only_date=date.today(), hour=time(hour=1))
        only_date.save()
        day_function = DayFunction(theater=theater, room_theater=room_theater,
                                   play_theater=play_theater,
                                   datetime_function=only_date)
        day_function.save()

        self.assertEqual(day_function.theater, theater)
        self.assertEqual(day_function.room_theater, room_theater)
        self.assertEqual(day_function.play_theater, play_theater)
        self.assertEqual(day_function.datetime_function, only_date)

    def test_create_day_function_with_periodic_date(self):
        theater = TheaterFactory.create()
        room_theater = RoomTheaterFactory(theater=theater)
        play_theater = PlayTheaterFactory.create()
        since = date.today()
        until = since + timedelta(days=5)
        periodic_date = "Lunes, Martes"
        periodic_date = PeriodicDate(since=date.today(), until=until,
                                     periodic_date=periodic_date,
                                     hour=time(hour=1))
        periodic_date.save()
        day_function = DayFunction(theater=theater, room_theater=room_theater,
                                   play_theater=play_theater,
                                   datetime_function=periodic_date)
        day_function.save()

        self.assertEqual(day_function.theater, theater)
        self.assertEqual(day_function.room_theater, room_theater)
        self.assertEqual(day_function.play_theater, play_theater)

    def test_create_day_function_without_custom_tickets(self):
        theater = TheaterFactory.create()
        room_theater = RoomTheaterFactory(theater=theater)
        play_theater = PlayTheaterFactory.create()
        TicketFactory.create(play_theater=play_theater)
        since = date.today()
        until = since + timedelta(days=5)
        periodic_date = "Lunes, Martes"
        periodic_date = PeriodicDate(since=date.today(), until=until,
                                     periodic_date=periodic_date,
                                     hour=time(hour=1))
        periodic_date.save()
        day_function = DayFunction(theater=theater, room_theater=room_theater,
                                   play_theater=play_theater,
                                   datetime_function=periodic_date)
        day_function.save()

        self.assertEqual(day_function.tickets[0],
                         play_theater.play_tickets.all()[0])

    def test_create_day_function_with_custom_tickets(self):
        theater = TheaterFactory.create()
        room_theater = RoomTheaterFactory(theater=theater)
        play_theater = PlayTheaterFactory.create()
        since = date.today()
        until = since + timedelta(days=5)
        periodic_date = "Lunes, Martes"


        periodic_date = PeriodicDate(since=date.today(), until=until,
                                     periodic_date=periodic_date,
                                     hour=time(hour=1))
        periodic_date.save()
        day_function = DayFunction(theater=theater, room_theater=room_theater,
                                   play_theater=play_theater,
                                   datetime_function=periodic_date)
        day_function.save()


        self.assertEqual(day_function.tickets[0],
                         play_theater.play_tickets.all()[0])
