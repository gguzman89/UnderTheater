# vim: set fileencoding=utf-8 :
import ast
from django import forms
from django.utils import timezone
from django.forms.models import inlineformset_factory, formset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from underTheaterApp.models import PlayTheater, DayFunction, Ticket,\
    Ticketeable, DateTimeFunction, ClassTheater
from underTheaterApp.constant import DayOfWeek, Hour, Durations
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


class BaseActorFormSet(forms.BaseFormSet):

    def __init__(self, *args, **kwargs):
        super(BaseActorFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        """
         Validaciones del form set de DayFunction
        """
        duplicate = False
        actors = []

        for form in self.forms:
            if form.cleaned_data:
                name = form.cleaned_data['name']
                surname = form.cleaned_data['surname']
                actors_dict = {"name": name, "surname": surname}
                duplicate = duplicate or actors_dict in actors
                actors.append(actors_dict)

        if duplicate:
            raise forms.ValidationError('No se pueden agregar actores repetidos')


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
        datetime_function = None
        if hasattr(self.instance, "datetime_function"):
            datetime_function = self.instance.datetime_function
        self.datetime_form = DateTimeFunctionForm(data=kwargs.get('data', None), instance=datetime_function)
        """
        self.ticket = TicketFormSet(data=kwargs.get('data', None),
                                          instance=self.instance)
        """

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
        widgets = {'user': forms.HiddenInput(),
                   'facebook': forms.TextInput(attrs={'placeholder': "my.facebook"}),
                   'twitter': forms.TextInput(attrs={'placeholder': "@mytwitter"}),
                   'name': forms.TextInput(attrs={'placeholder': "Mi nombre"}),
                   'surname': forms.TextInput(attrs={'placeholder': "Mi apellido"}),
                   }
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


class Select2Widget(forms.SelectMultiple):

    def render(self, name, value, attrs=None):
        if value and isinstance(value, basestring):
            value = ast.literal_eval(value)
        return super(Select2Widget, self).render(name, value, attrs)


class DateTimeFunctionForm(forms.ModelForm):
    date_format = '%d/%m/%Y'
    since = forms.DateField(initial=timezone.now().date().strftime(date_format),
                            input_formats=[date_format], label="Desde",
                            widget=forms.widgets.DateInput(format=date_format))
    until = forms.DateField(input_formats=[date_format], required=False, label="Hasta",
                            widget=forms.widgets.DateInput(format=date_format))

    class Meta:
        model = DateTimeFunction
        fields = ("hour", "until", "since", "periodic_date")
        labels = {'hour': 'Horas', 'until': 'Hasta', 'since': 'Desde',
                  'periodic_date': 'Dias de la semana', 'duration': "duracion aproximada"}
        widgets = {"periodic_date": Select2Widget(attrs={'class': 'form-control',
                                                                'style': 'width: 100%;'},
                                                         choices=DayOfWeek),
                   "hour": Select2Widget(attrs={'class': 'form-control',
                                                       'style': 'width: 100%;'},
                                                choices=Hour)}

    def __init__(self, *args, **kwargs):
        super(DateTimeFunctionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def is_valid(self):
        return super(DateTimeFunctionForm, self).is_valid()


class ActorWithoutUserForm(forms.ModelForm):
    photo = forms.ImageField(label="Foto de perfil")

    class Meta:
        model = Actor
        fields = ("name", "surname")
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': "Mi nombre"}),
                   'surname': forms.TextInput(attrs={'class': 'form-control-actors',
                                                     'placeholder': "Mi apellido"})
                   }
        labels = {'name': 'Nombre', 'surname': 'Apellido'}

    def __init__(self, *args, **kwargs):
        super(ActorWithoutUserForm, self).__init__(*args, **kwargs)


ActorFormSet = formset_factory(ActorWithoutUserForm, formset=BaseActorFormSet, extra=1, can_order=False, can_delete=True)


class PlayTheaterForm(forms.ModelForm):
    picture = forms.ImageField(label="Foto de la obra")

    class Meta:
        model = PlayTheater
        synopsis_placeholder = "Una breve descripcion de lo que va a tratar la obra"
        play_name_placeholder = "Nombre de la obra"
        fields = ("play_name", "synopsis", "picture", "actors", "owner")
        labels = {'play_name': 'Nombre de la obra', 'synopsis': 'Sinopsis',
                  'actors': "Actores", 'picture': 'Foto de la obra'}
        widgets = {'owner': forms.HiddenInput(),
                   'synopsis': forms.Textarea(attrs={'class': 'form-control',
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
                                    instance=self.instance, prefix="ticket_prefix")
        self.init_actor_form(kwargs)

    def init_actor_form(self, kwargs):
        self.create_actors = ActorFormSet(data=kwargs.get('data', None), prefix="actors_prefix")
        self.create_actors.is_data = len(kwargs.get('data', {})) > 0
        self.fields['actors'].required = False

    def is_valid(self):
        self.create_actors.files = self.files
        return super(PlayTheaterForm, self).is_valid()\
            and self.ticket.is_valid() and self.day_function.is_valid()\
            and self.create_actors.is_valid()

    def get_errors(self):
        return self.form_errors

    def _check_error(self):
        self.form_errors = self.ticket.non_form_errors()
        self.form_errors += self.create_actors.non_form_errors()

    def clean(self):
        if not self.cleaned_data.get("actors") and len(self.create_actors.forms) == 0:
            raise forms.ValidationError('La obra tiene que tener un actor')

        return super(PlayTheaterForm, self).clean()

    def has_errors(self):
        self._check_error()
        return any(self.form_errors)

    def set_topic(self):
        topic = "%s-%s" % (self.instance.play_name, self.instance.__class__.__name__)
        if len(topic) > 250:
            topic = "%s-%s" % (self.instance.play_name[:100], self.instance.__class__.__name__)
        self.instance.topic = topic

    def _save_actors_formset(self, new_play):
        for form in self.create_actors.forms:
            instance = form.save()
            instance.playtheater_set.add(new_play)

    def save_formsets(self, new_play):
        self.ticket.instance = new_play
        self.day_function.instance = new_play
        self.ticket.save()
        self.day_function.save()
        self._save_actors_formset(new_play)

    def save(self, *args, **kwargs):
        self.set_topic()
        new_play = super(PlayTheaterForm, self).save(*args, **kwargs)
        self.save_formsets(new_play)
        return new_play


class ClassTheaterForm(forms.ModelForm):
    picture = forms.ImageField(label="Foto de la clase")

    class Meta:
        model = ClassTheater
        description_placeholder = "Breve descripcion de la clase"
        fields = ("class_name", "description", "picture", "theater", "room_theater",
                  "duration", "price", "with_interview", "owner", "teacher")
        labels = {'class_name': 'Nombre de la clase', 'description': 'De que trata la clase',
                  'picture': 'Foto de la clase', 'with_interview': 'Con entrevista previa',
                  'duration': "Duracion de la clase", "price": "Precio de la clase",
                  "teacher": 'profesor'}
        widgets = {'owner': forms.HiddenInput(),
                   'class_name': forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': "Nombre de la clase"}),
                   'description': forms.Textarea(attrs={'class': 'form-control',
                                                        'rows': 5, 'col': 2,
                                                        'placeholder': description_placeholder}),
                   'theater': forms.Select(attrs={'class': 'form-control',
                                                  'style': 'width: 100%;'}),
                   'room_theater': forms.Select(attrs={'class': 'form-control',
                                                       'style': 'width: 100%;'}),
                   'duration': forms.Select(attrs={'class': 'form-control',
                                                       'style': 'width: 100%;'},
                                            choices=Durations),
                   'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
                   'teacher': forms.Select(attrs={'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        super(ClassTheaterForm, self).__init__(*args, **kwargs)
        datetime_function = None
        if hasattr(self.instance, "datetime_function"):
            datetime_function = self.instance.datetime_function
        self.datetime_form = DateTimeFunctionForm(data=kwargs.get('data', None), instance=datetime_function)

    def is_valid(self):
        return super(ClassTheaterForm, self).is_valid()\
            and self.datetime_form.is_valid()

    def clean(self):
        if not self.data.get("until", None):
            raise forms.ValidationError('Tiene que haber fecha de fin')
        if not self.data.get("periodic_date", None):
            raise forms.ValidationError('Tiene que haber dias de la semana')
        return super(ClassTheaterForm, self).clean()

    def save(self, *args, **kwargs):
        self.instance.datetime_function = self.datetime_form.save()
        return super(ClassTheaterForm, self).save(*args, **kwargs)
