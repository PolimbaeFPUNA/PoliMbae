from django import forms
from app.mantenimiento.models import Mantenimiento
from app.recurso.models import *
from app.reserva.models import *

class MantForm(forms.ModelForm):


    class Meta:
        model = Mantenimiento
        fields = [

            'fecha_entrega',
            'fecha_fin',
        ]

        labels = {

            'fecha_entrega': 'Fecha de Entrega',
            'fecha_fin': 'Fecha de Devolucion',
        }

        widgets = {
            'fecha_entrega': forms.DateInput(format="%Y-%m-%d", attrs={"class":"form-control"}),
            'fecha_fin': forms.DateInput(format="%Y-%m-%d", attrs={"class":"form-control"}),

        }

class ReservaForm(forms.ModelForm):
    class Meta:
        model =ReservaGeneral
        fields=[
            'fecha_reserva',
            'hora_inicio',
            'hora_fin',
        ]
        labels={
            'fecha_reserva':'Fecha',
            'hora_inicio':'Hora',
            'hora_fin':'Hora',
        }
        widgets={
            'fecha_reserva':forms.DateInput(format="%Y-%m-%d", attrs={"class":"form-control"}),
            'hora_inicio': forms.TimeInput(format="%H:%M",attrs={"class":"form-control"}),
            'hora_fin': forms.TimeInput(format="%H:%M",attrs={"class":"form-control"})
        }

class ReservaForm2(forms.ModelForm):
    class Meta:
        model =ReservaGeneral
        fields=[
            'fecha_reserva',
        ]
        labels={
            'fecha_reserva':'Fecha',
        }
        widgets={
            'fecha_reserva':forms.DateInput(format="%Y-%m-%d", attrs={"class":"form-control"}),
        }