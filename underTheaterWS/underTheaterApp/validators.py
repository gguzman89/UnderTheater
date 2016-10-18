# vim: set fileencoding=utf-8 :
import unicodedata
import ast
from django.core.exceptions import ValidationError

dates_dict = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado",
              "Domingo"]


def remove_accent(value):
    return unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')


def periodic_date_validator(value):
    dates = ast.literal_eval(value)
    list_date = []
    for date in dates:
        date = date.strip("  ")
        date = remove_accent(date)
        if date.title() not in dates_dict:
            raise ValidationError('%(value)s no es un dia de la semana',
                                  params={'value': date})
        if date in list_date:
            raise ValidationError('%(value)s  no podes agregar dos veces el mismo dia',
                                  params={'value': date})
        list_date.append(date)


def min_words_validator(value):
    words = value.split(" ")
    if len(words) < 3:
        raise ValidationError('Tiene que escribir una sinopsis mas descriptiva')
