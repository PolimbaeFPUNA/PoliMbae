from django import forms
from app.recurso_pr.models import TipoRecurso1, Recurso1
from app.usuario.models import Profile
from django.core.validators import ValidationError
from app.reserva_new.models import Solicitud, Reserva
from django.contrib.auth.models import User
Confirmada = 'CONFIRMADA'
Cancelada = 'CANCELADA'
ESTADO_CHOICE = ((Confirmada, 'Confirmada'),
                     (Cancelada, 'Cancelada'),
                     )

class SolicitudForm(forms.ModelForm):
    tipo_recurso = forms.ModelChoiceField(queryset=TipoRecurso1.objects.all(),
                                          widget=forms.Select(attrs={"class": "form-control"}))

    class Meta:
        model= Solicitud
        exclude= ['usuario','recurso']
        fields=[
            'fecha_reserva',
            'hora_inicio',
            'hora_fin',
        ]

        label= {
            'fecha_reserva': 'Fecha',
            'hora_inicio': 'Hora Inicio',
            'hora_fin': 'Hora Finalizacion',
        }
        widgets= {
            'fecha_reserva': forms.DateInput(format="%Y-%m-%d", attrs={"class":"form-control"}),
            'hora_inicio': forms.TimeInput(format="%H:%M", attrs={"class":"form-control"}),
            'hora_fin': forms.TimeInput(format="%H:%M", attrs={"class":"form-control"}),
        }

class SolicitudConfirmForm(forms.ModelForm):

    class Meta:
        model= Solicitud
        exclude=['recurso','usuario']
        fields=[
            'recurso',
            'fecha_reserva',
            'hora_inicio',
            'hora_fin',
        ]
        label= {
            'recurso':'Recurso',
            'fecha_reserva': 'Fecha',
            'hora_inicio': 'Hora Inicio',
            'hora_fin': 'Hora Finalizacion',
        }
        widgets= {
            'fecha_reserva': forms.DateInput(format="%Y-%m-%d", attrs={"class":"form-control", "readonly":"readonly"}),
            'hora_inicio': forms.TimeInput(format="%H:%M", attrs={"class":"form-control","readonly":"readonly"}),
            'hora_fin': forms.TimeInput(format="%H:%M", attrs={"class":"form-control","readonly":"readonly"}),
        }



