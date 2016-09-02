from django.contrib import admin
from underTheaterApp import models, users


@admin.register(models.Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name', )
    search_fields = ('name',)


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('number_phone', 'facebook', 'address')
    ordering = ('number_phone', )
    search_fields = ('number_phone',)


@admin.register(models.TheaterRoom)
class TheaterRoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'theater', 'capacity')
    ordering = ('room_name', )
    search_fields = ('room_name',)


@admin.register(models.PlayTheater)
class PlayTheaterAdmin(admin.ModelAdmin):
    list_display = ('play_name', )
    ordering = ('play_name', )
    search_fields = ('play_name',)


@admin.register(models.PlayPrice)
class PlayPriceAdmin(admin.ModelAdmin):
    list_display = ('price_name', 'price', 'play')
    ordering = ('price_name', )
    search_fields = ('play', )


@admin.register(models.DateShow)
class DateShowAdmin(admin.ModelAdmin):
    list_display = ('date_show', )
    ordering = ('date_show', )
    search_fields = ('play__play_name', )


@admin.register(users.Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', )
    ordering = ('name', )
    search_fields = ('name', )
