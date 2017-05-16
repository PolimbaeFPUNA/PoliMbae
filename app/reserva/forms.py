from django import forms
from app.recurso_pr.models import TipoRecurso1, Recurso1
from django.core.validators import ValidationError
from app.reserva.models import ReservaGeneral, ListaReservaGeneral, ReservaEspecifica, ListaReservaEspecifica

ESTADO_CHOICE = (('Disponible', 'Disponible'),
                     ('Reservado', 'Reservado'),
                     ('En Mantenimiento', 'En Mantenimiento'),
                     ('Solicitado', 'Solicitado'),
                     ('Fuera de Uso', 'Fuera de Uso'),
                     ('En Uso', 'En Uso'),
                 )


class ReservaGeneralForm(forms.ModelForm):
    profile = forms.TextInput()
    class Meta:
        model = ReservaGeneral
        exclude = ['recurso','profile']
        fields = [
            'fecha_reserva',
            'hora_inicio',
            'hora_fin',
        ]
        labels = {
            'fecha_reserva': 'Indique la Fecha de Reserva ',
            'hora_inicio': 'Hora de Inicio de Reserva',
            'hora_fin': 'Hora de Finalizacion de Reserva',
        }
        widgets = {
            'fecha_reserva': forms.DateInput(format="%Y-%m-%d"),
            'hora_inicio': forms.TimeInput(format="%H:%M"),
            'hora_fin': forms.TimeInput(format="%H:%M"),
        }


class ReservaGeneralForm2(forms.ModelForm):
    class Meta:
        model = ReservaGeneral
        exclude = ['profile']
        fields = [
            'recurso',
            'fecha_reserva',
            'hora_inicio',
            'hora_fin',
        ]
        labels = {

            'recurso': 'Tipo de recurso',
            'fecha_reserva': 'Indique la Fecha de Reserva ',
            'hora_inicio': 'Hora de Inicio de Reserva',
            'hora_fin': 'Hora de Finalizacion de Reserva',
        }
        widgets = {
            'recurso': forms.Select(),
            'fecha_reserva': forms.DateInput(format="%Y-%m-%d"),
            'hora_inicio': forms.TimeInput(format="%H:%M"),
            'hora_fin': forms.TimeInput(format="%H:%M"),
        }


class ListaReservaGeneralForm(forms.ModelForm):
    class Meta:
        model = ListaReservaGeneral
        fields = [
            'recurso_reservado',
            'estado_reserva',
            'fecha_reserva',
            'hora_inicio',
            'hora_fin',
        ]
        labels = {
            'recurso_reservado': 'Recurso a Reservar',
            'estado_reserva': 'Estado de la Reserva',
            'fecha_reserva': 'Fecha de Reserva',
            'hora_inicio': 'Hora de Inicio',
            'hora_fin': 'Hora de Finalizacion',
        }
        widgets = {
            'recurso_reservado': forms.NumberInput(),
            'estado_reserva': forms.Select(choices=ESTADO_CHOICE),
            'fecha_reserva': forms.DateInput(format="%Y-%m-%d"),
            'hora_inicio': forms.TimeInput(format="%H:%M"),
            'hora_fin': forms.TimeInput(format="%H:%M"),
        }


class ReservaEspecificaForm(forms.ModelForm):
    class Meta:
        model = ReservaEspecifica
        exclude = ['recurso']
        fields = [
            'profile',
            'fecha_reserva',
            'hora_inicio',
            'hora_fin',
        ]
        labels = {
            'profile': 'Ingrese su numero de CI',
            'fecha_reserva': 'Indique la Fecha de Reserva ',
            'hora_inicio': 'Hora de Inicio de Reserva',
            'hora_fin': 'Hora de Finalizacion de Reserva',
        }
        widgets = {
            'profile': forms.TextInput(),
            'fecha_reserva': forms.DateInput(format="%Y-%m-%d"),
            'hora_inicio': forms.TimeInput(format="%H:%M"),
            'hora_fin': forms.TimeInput(format="%H:%M"),
        }


class ListaReservaEspecificaForm(forms.ModelForm):
    class Meta:
        model = ListaReservaEspecifica
        exclude = ['prioridad']
        fields = [
            'recurso_reservado',
            'estado_reserva',
            'fecha_reserva',
            'hora_inicio',
            'hora_fin',
        ]
        labels = {
            'recurso_reservado': 'Recurso a Reservar',
            'estado_reserva': 'Estado de la Reserva',
            'fecha_reserva': 'Fecha de Reserva',
            'hora_inicio': 'Hora de Inicio',
            'hora_fin': 'Hora de Finalizacion',
        }
        widgets = {
            'recurso_reservado': forms.NumberInput(),
            'estado_reserva': forms.Select(choices=ESTADO_CHOICE),
            'fecha_reserva': forms.DateInput(format="%Y-%m-%d"),
            'hora_inicio': forms.TimeInput(format="%H:%M"),
            'hora_fin': forms.TimeInput(format="%H:%M"),
        }
