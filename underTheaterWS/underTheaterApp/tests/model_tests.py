# vim: set fileencoding=utf-8 :
from django.test import TestCase
from datetime import date, time, timedelta
from underTheaterApp.factories import TheaterFactory, RoomTheaterFactory,\
    PlayTheaterFactory, TicketFactory
from underTheaterApp.models import DayFunction, DateTimeFunction


class PlayTheaterTestCase(TestCase):

    def test_play_theater_creation(self):
        self.assertTrue(True)


class DayFunctionTest(TestCase):

    def _setup_with_periodic_date(self):
        theater = TheaterFactory.create()
        room_theater = RoomTheaterFactory(theater=theater)
        play_theater = PlayTheaterFactory.create()
        since = date.today()
        until = since + timedelta(days=5)
        periodic_date = "Lunes, Martes"
        periodic_date = DateTimeFunction(since=date.today(), until=until,
                                        periodic_date=periodic_date,
                                        hour=time(hour=1))
        periodic_date.save()
        return theater, room_theater, play_theater, periodic_date

    def test_create_day_function_with_only_date(self):
        theater = TheaterFactory.create()
        room_theater = RoomTheaterFactory(theater=theater)
        play_theater = PlayTheaterFactory.create()
        datetime_function = DateTimeFunction(since=date.today(), hour="[8:00]")
        datetime_function.save()
        day_function = DayFunction(theater=theater, room_theater=room_theater,
                                   play_theater=play_theater,
                                   datetime_function=datetime_function)
        day_function.save()

        self.assertEqual(day_function.theater, theater)
        self.assertEqual(day_function.room_theater, room_theater)
        self.assertEqual(day_function.play_theater, play_theater)
        self.assertEqual(day_function.datetime_function, datetime_function)

    def test_create_day_function_with_periodic_date(self):
        theater, room_theater, play_theater, periodic_date = self._setup_with_periodic_date()
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
        TicketFactory.create(ticketeable=play_theater)
        since = date.today()
        until = since + timedelta(days=5)
        periodic_date = "Lunes, Martes"
        periodic_date = DateTimeFunction(since=date.today(), until=until,
                                         periodic_date=periodic_date,
                                         hour=time(hour=1))
        periodic_date.save()
        day_function = DayFunction(theater=theater, room_theater=room_theater,
                                   play_theater=play_theater,
                                   datetime_function=periodic_date)
        day_function.save()

        self.assertEqual(day_function.tickets()[0],
                         play_theater.tickets()[0])

    def test_create_day_function_with_custom_tickets(self):
        theater = TheaterFactory.create()
        room_theater = RoomTheaterFactory(theater=theater)
        play_theater = PlayTheaterFactory.create()
        since = date.today()
        until = since + timedelta(days=5)
        periodic_date = "Lunes, Martes"

        periodic_date = DateTimeFunction(since=date.today(), until=until,
                                         periodic_date=periodic_date,
                                         hour=time(hour=1))
        periodic_date.save()
        day_function = DayFunction(theater=theater, room_theater=room_theater,
                                   play_theater=play_theater,
                                   datetime_function=periodic_date)
        day_function.save()

        self.assertEqual(day_function.tickets().count(),
                         play_theater.tickets().count())
