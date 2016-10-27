# vim: set fileencoding=utf-8 :
from django import forms
from django.utils import timezone
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from underTheaterApp.models import PlayTheater, DayFunction, Ticket,\
    Ticketeable, DateTimeFunction
from underTheaterApp.constant import DayOfWeek, Hour
from underTheaterApp.users import Actor, OwnerTheater, Spectators
from underTheaterWS.utils import regex_account_twitter, regex_url_facebook


class BaseDayFuntionFormSet(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.extra = 0 if kwargs["instance"].id else 1
        super(BaseDayFuntionFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        """
         Validaciones del form set de DayFunction
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
    def __init__(self, *args, **kwargs):
        self.extra = 0 if kwargs["instance"].id else 1
        super(BaseTicketFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        """
        Validaciones de los formularios de tickets
        """
        duplicate = False
        tickets = []

        if any(self.errors):
            return

        if len(self.forms) < 1:
            raise forms.ValidationError('Tiene que haber al menos una entrada')

        for form in self.forms:
            if form.cleaned_data:
                ticket_name = form.cleaned_data['ticket_name']
                duplicate = ticket_name in tickets
                tickets.append(ticket_name)
            elif len(self.forms) == 1:
                raise forms.ValidationError('Tiene que haber al menos una entrada')

        if duplicate:
            raise forms.ValidationError('No se puede agregar dos veces la misma'
                                        ' entrada')


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ("ticket_name", "price")
        labels = {'ticket_name': 'Nombre de la entrada', 'price': 'Precio'}
        widgets = {'ticket_name': forms.TextInput(attrs={'class': 'form-control width-custom',
                                                         'placeholder': "nombre de la entrada",
                                                         'required': 'true'}),
                   'price': forms.TextInput(attrs={'class': 'form-control-ticket',
                                                   'placeholder': "2x1 o $200 o %50",
                                                   'required': 'true'})}


class DayFunctionForm(forms.ModelForm):

    class Meta:
        model = DayFunction
        fields = ("theater", "room_theater")
        widgets = {"theater": forms.Select(attrs={'class': 'form-control',
                                                  'style': 'width: 100%;'}),
                   "room_theater": forms.Select(attrs={'class': 'form-control',
                                                       'style': 'width: 100%;'})}

    def __init__(self, *args, **kwargs):
        super(DayFunctionForm, self).__init__(*args, **kwargs)
        """
        self.ticket = TicketFormSet(data=kwargs.get('data', None),
                                          instance=self.instance)
        """
        self.datetime_form = DateTimeFunctionForm(data=kwargs.get('data', None))

    def is_valid(self):
        return super(DayFunctionForm, self).is_valid()\
            and self.datetime_form.is_valid()

    def set_topic(self):
        self.instance.topic = "%s-%s" % (self.instance, self.instance.__class__.__name__)

    def save(self, *args, **kwargs):
        self.instance.datetime_function = self.datetime_form.save()
        self.set_topic()
        return super(DayFunctionForm, self).save(*args, **kwargs)

TicketFormSet = inlineformset_factory(Ticketeable, Ticket,
                                      form=TicketForm,
                                      formset=BaseTicketFormSet,
                                      can_order=False,
                                      can_delete=True)

DayFunctionFormSet = inlineformset_factory(PlayTheater,
                                           DayFunction,
                                           fk_name='play_theater',
                                           form=DayFunctionForm,
                                           formset=BaseDayFuntionFormSet,
                                           can_order=False,
                                           can_delete=True)


class ProfileCreateForm(forms.ModelForm):
    photo = forms.ImageField(label="Foto de perfil")

    class Meta:
        fields = ("user", "name", "surname", "facebook", "twitter", "photo")
        widgets = {'user': forms.HiddenInput()}
        labels = {'name': 'Nombre', 'surname': 'Apellido'}

    def __init__(self, *args, **kwargs):
        super(ProfileCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_twitter(self):
        if self.cleaned_data["twitter"]:
            self.cleaned_data["twitter"] = regex_account_twitter(self.cleaned_data["twitter"])
            if self.cleaned_data["twitter"] is None:
                raise forms.ValidationError('El usuario de twitter no es valido')
        return self.cleaned_data["twitter"]

    def clean_facebook(self):
        if self.cleaned_data["facebook"]:
            self.cleaned_data["facebook"] = regex_url_facebook(self.cleaned_data["facebook"])
            if self.cleaned_data["facebook"] is None:
                raise forms.ValidationError('El usuario de facebook no es valido')
        return self.cleaned_data["facebook"]


class ActorCreateForm(ProfileCreateForm):
    class Meta(ProfileCreateForm.Meta):
        model = Actor


class TheaterCreateForm(ProfileCreateForm):
    class Meta(ProfileCreateForm.Meta):
        model = OwnerTheater


class SpectatorCreateForm(ProfileCreateForm):
    class Meta(ProfileCreateForm.Meta):
        model = Spectators


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


class DateTimeFunctionForm(forms.ModelForm):
    date_format = '%d/%m/%Y'
    since = forms.DateField(initial=timezone.now().date().strftime(date_format),
                            input_formats=[date_format], label="Desde")
    until = forms.DateField(input_formats=[date_format], required=False, label="Hasta")

    class Meta:
        model = DateTimeFunction
        fields = ("hour", "until", "since", "periodic_date")
        labels = {'hour': 'Horas', 'until': 'Hasta', 'since': 'Desde',
                  'periodic_date': 'Dias de la semana'}
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
    picture = forms.ImageField(label="Foto de la obra")

    class Meta:
        model = PlayTheater
        synopsis_placeholder = "Una breve descripcion de lo que va a tratar la obra"
        play_name_placeholder = "Nombre de la obra"
        fields = ("play_name", "synopsis", "picture", "actors")
        labels = {'play_name': 'Nombre de la obra', 'synopsis': 'Sinopsis',
                  'actors': "Actores", 'picture': 'Foto de la obra'}
        widgets = {'synopsis': forms.Textarea(attrs={'class': 'form-control',
                                                     'rows': 5, 'col': 2,
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

    def is_valid(self):
        return super(PlayTheaterForm, self).is_valid()\
            and self.ticket.is_valid() and self.day_function.is_valid()

    def get_errors(self):
        return self.form_errors

    def _check_error(self):
        self.form_errors = self.ticket.non_form_errors()

    def has_errors(self):
        self._check_error()
        return any(self.form_errors)

    def set_topic(self):
        topic = "%s-%s" % (self.instance.play_name, self.instance.__class__.__name__)
        if len(topic) > 250:
            topic = "%s-%s" % (self.instance.play_name[:100], self.instance.__class__.__name__)
        self.instance.topic = topic

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
