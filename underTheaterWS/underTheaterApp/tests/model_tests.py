# vim: set fileencoding=utf-8 :
from django.test import TestCase
from datetime import date, time, timedelta
from underTheaterApp.factories import TheaterFactory, RoomTheaterFactory,\
    PlayTheaterFactory, TicketFactory, DateTimeFunctionFactory, DayFunctionFactory
from underTheaterApp.models import DayFunction, DateTimeFunction, PlayTheater


class PlayTheaterTestCase(TestCase):

    def test_play_theater_creation(self):
        self.assertTrue(True)

    def _create_n_play_theaters(self, n, since=None):
        list_play = []
        kwargs = {"since": since} if since else {}
        for x in range(0, n):
            play_theater = PlayTheaterFactory.create()
            date = DateTimeFunctionFactory.create(**kwargs)
            DayFunctionFactory(play_theater=play_theater, datetime_function=date)
            list_play.append(play_theater)
        return list_play

    def test_get_next_releases_plays(self):
        list_plays = self._create_n_play_theaters(5)
        old_plays = self._create_n_play_theaters(3, date(2015, 11, 03))

        next_releases_play = PlayTheater.objects.next_releases()

        self.assertEqual(next_releases_play.count(), len(list_plays))
        for play in list_plays:
            self.assertTrue(play in next_releases_play)
        self.assertFalse(old_plays in next_releases_play)


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
