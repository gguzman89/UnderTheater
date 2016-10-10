# vim: set fileencoding=utf-8 :
from django import forms
from django.utils import timezone
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from underTheaterApp.models import PlayTheater, DayFunction, Ticket,\
    Ticketeable, DateTimeFunction


class BaseDayFuntionFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        duplicate = False
        dayFuntions = []

        if any(self.errors):
            return
        for form in self.forms:
            if form.cleaned_data:
                theater = form.cleaned_data['theater']
                room_theater = form.cleaned_data['room_theater']
                dic_day_function = {"theater": theater,
                                    "room_theater": room_theater,
                                    }
                duplicate = dic_day_function in dayFuntions
                dayFuntions.append(dic_day_function)

        if duplicate:
            raise forms.ValidationError('No se agregar funciones repetidas')


class BaseTicketFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        duplicate = False
        tickets = []

        if any(self.errors):
            return

        for form in self.forms:
            if form.cleaned_data:
                ticket_name = form.cleaned_data['ticket_name']
                duplicate = ticket_name in tickets
                tickets.append(ticket_name)

        if duplicate:
            raise forms.ValidationError('No se puede agregar dos veces la misma'
                                        ' entrada')


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ("ticket_name", "price")
        widgets = {'ticket_name': forms.TextInput(attrs={'class': 'form-control',
                                                         'rows': 5, 'col': 2,
                                                         'placeholder': "nombre de la entrada",
                                                         'required': 'true'}),
                   'price': forms.TextInput(attrs={'size': 25,
                                                   'class': 'form-control',
                                                   'placeholder': "2x1 o $200 o %50",
                                                   'required': 'true'})}

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, *args, **kwargs):
        new_play = super(TicketForm, self).save(*args, **kwargs)
        return new_play


class DayFunctionForm(forms.ModelForm):

    class Meta:
        model = DayFunction
        fields = ("theater", "room_theater")

    def __init__(self, *args, **kwargs):
        super(DayFunctionForm, self).__init__(*args, **kwargs)
        """
        self.ticket = TicketFormSet(data=kwargs.get('data', None),
                                          instance=self.instance)
        """
        self.datetime_form = DateTimeFunctionForm(data=kwargs.get('data', None))
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def is_valid(self):
        return super(DayFunctionForm, self).is_valid()\
            and self.datetime_form.is_valid()

    def set_topic(self):
        self.instance.topic = "%s-%s" % (self.instance, self.instance.pk)

    def save(self, *args, **kwargs):
        self.instance.datetime_function = self.datetime_form.save()
        self.set_topic()
        return super(DayFunctionForm, self).save(*args, **kwargs)

TicketFormSet = inlineformset_factory(Ticketeable, Ticket,
                                      form=TicketForm,
                                      formset=BaseTicketFormSet,
                                      extra=1, can_order=False,
                                      can_delete=True)

DayFunctionFormSet = inlineformset_factory(PlayTheater,
                                           DayFunction,
                                           fk_name='play_theater',
                                           form=DayFunctionForm,
                                           formset=BaseDayFuntionFormSet,
                                           extra=1,
                                           can_order=False,
                                           can_delete=True)


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError(u"This email already used.")
        return data

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


DayOfWeek = (
    ('Lunes', 'Lunes'),
    ('Martes', 'Martes'),
    ('Miercoles', 'Miercoles'),
    ('Jueves', 'Jueves'),
    ('Viernes', 'Viernes'),
    ('Sabado', 'Sabado'),
    ('Domingo', 'Domingo'),
)

Hour = tuple([("%d:%s" % (x / 60, "00" if x % 60 == 0 else x % 60),
               "%d:%s" % (x / 60, "00" if x % 60 == 0 else x % 60))
              for x in range(0, 96 * 15, 15)])


class DateTimeFunctionForm(forms.ModelForm):
    since = forms.DateField(initial=timezone.now().date())

    class Meta:
        model = DateTimeFunction
        fields = ("hour", "until", "since", "periodic_date")
        widgets = {"periodic_date": forms.SelectMultiple(attrs={'class': 'form-control',
                                                                'style': 'width: 100%;'},
                                                         choices=DayOfWeek),
                   "hour": forms.SelectMultiple(attrs={'class': 'form-control',
                                                       'style': 'width: 100%;'},
                                                choices=Hour)}

    def __init__(self, *args, **kwargs):
        super(DateTimeFunctionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def is_valid(self):
        return super(DateTimeFunctionForm, self).is_valid()


class PlayTheaterForm(forms.ModelForm):
    picture = forms.ImageField()

    class Meta:
        model = PlayTheater
        synopsis_placeholder = "Una breve descripcion de lo que va a tratar la obra"
        play_name_placeholder = "Nombre de la obra"
        fields = ("play_name", "synopsis", "picture", "actors")
        widgets = {'synopsis': forms.Textarea(attrs={'class': 'form-control',
                                                     'rows': 3, 'col': 2,
                                                     'placeholder': synopsis_placeholder}),
                   'play_name': forms.TextInput(attrs={'size': 25,
                                                       'class': 'form-control',
                                                       'placeholder': play_name_placeholder}),
                   'actors': forms.SelectMultiple(attrs={'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        super(PlayTheaterForm, self).__init__(*args, **kwargs)
        self.day_function = DayFunctionFormSet(data=kwargs.get('data', None),
                                               instance=self.instance)
        self.ticket = TicketFormSet(data=kwargs.get('data', None),
                                    instance=self.instance)
        self.fields["play_name"].widget.attrs['class'] = 'form-control'

    def is_valid(self):
        return super(PlayTheaterForm, self).is_valid()\
            and self.ticket.is_valid() and self.day_function.is_valid()

    @property
    def get_errors(self):
        return self.form_errors

    def _check_error(self):
        errors = self.day_function.non_form_errors()
        errors += [f1.ticket.non_form_errors() for f1 in self.day_function.forms]
        self.form_errors = errors

    @property
    def has_errors(self):
        self._check_error()
        return any(self.form_errors)

    def set_topic(self):
        self.instance.topic = "%s-%s" % (self.instance, self.instance.pk)

    def save_formsets(self, new_play):
        self.ticket.instance = new_play
        self.day_function.instance = new_play
        self.ticket.save()
        self.day_function.save()

    def save(self, *args, **kwargs):
        self.set_topic()
        new_play = super(PlayTheaterForm, self).save(*args, **kwargs)
        self.save_formsets(new_play)
        return new_play
