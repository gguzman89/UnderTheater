from django.contrib import admin
from underTheaterApp import models, users


@admin.register(models.Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('name', 'review', 'owner', 'contact')
    ordering = ('name', 'owner')
    search_fields = ('name', 'owner')


@admin.register(users.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('number_phone', 'facebook', 'address')
    ordering = ('number_phone', )
    search_fields = ('number_phone',)


@admin.register(users.OwnerTheater)
class OwnerTheaterAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname')
    ordering = ('name', )
    search_fields = ('name',)


@admin.register(users.Spectators)
class SpectatorsAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname')
    ordering = ('name', )
    search_fields = ('name',)


@admin.register(users.Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname')
    ordering = ('name', )
    search_fields = ('name', )


@admin.register(models.TheaterRoom)
class TheaterRoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'theater', 'capacity')
    ordering = ('room_name', )
    search_fields = ('room_name',)


@admin.register(models.PlayTheater)
class PlayTheaterAdmin(admin.ModelAdmin):
    list_display = ('play_name', 'synopsis', )
    ordering = ('play_name', )
    search_fields = ('play_name',)


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticketeable', 'ticket_name', 'price')
    ordering = ('ticket_name', )
    search_fields = ('ticketeable', 'ticketeable')


@admin.register(models.DateTimeFunction)
class PeriodicDateAdmin(admin.ModelAdmin):
    list_display = ('id', 'since', 'periodic_date', 'until')


@admin.register(models.DayFunction)
class DayFunctionAdmin(admin.ModelAdmin):
    list_display = ('play_theater', 'theater', 'room_theater', 'datetime_function')
    ordering = ('play_theater', 'theater')
    search_fields = ('play_theater', 'theater')
