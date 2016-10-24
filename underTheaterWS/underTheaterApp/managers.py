# vim: set fileencoding=utf-8 :
from datetime import date, timedelta
from polymorphic.manager import PolymorphicManager


class PlayTheaterManager(PolymorphicManager):

    def next_releases(self, limit=6):
        today = date.today()
        until = today + timedelta(days=7)
        kwargs = {"dayfunction_related__datetime_function__since__range": (today, until)}
        return self.filter(**kwargs).order_by("dayfunction_related__datetime_function__since")[:limit]
