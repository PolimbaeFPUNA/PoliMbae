from django import forms
from app.recurso_pr.models import TipoRecurso1, Recurso1
from app.usuario.models import Profile
from django.core.validators import ValidationError
from app.reserva_new.models import Solicitud, Reserva
from django.contrib.auth.models import User

Confirmada = 'CONFIRMADA'
Cancelada = 'CANCELADA'
EnCurso = 'EN CURSO'
Finalizada= 'FINALIZADA'
ESTADO_CHOICE = ((Confirmada, 'Confirmada'),
                (Cancelada, 'Cancelada'),
                 (EnCurso,'ENCURSO'),
                 (Finalizada, 'Finalizada')
                )

class SolicitudForm(forms.ModelForm):
    tipo_recurso = forms.ModelChoiceField(queryset=TipoRecurso1.objects.filter(reservable=True),
                                          widget=forms.Select(attrs={"class": "form-control"}))
    recurso= forms.ModelChoiceField(queryset=Recurso1.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))
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

            'fecha_reserva': forms.DateInput(format="%Y-%m-%d", attrs={"class":"form-control form_datetime"}),
            'hora_inicio': forms.TimeInput(format="%H:%M", attrs={"class":"form-control form_time"}),
            'hora_fin': forms.TimeInput(format="%H:%M", attrs={"class":"form-control form_time"}),
        }

    def clean_recurso(self):
     recurso = self.cleaned_data["recurso"]
     if recurso != None:
        try:
            Recurso1._default_manager.get(recurso1 = recurso.recurso_id, TipoRecurso1 = self.cleaned_data["tipo_recurso"])
        except Recurso1.DoesNotExist:
            raise forms.ValidationError('Recurso con el codigo y tipo especificado no existen')
            return recurso

class SolicitudConfirmForm(forms.ModelForm):

    class Meta:
        model= Solicitud
        exclude=['recurso','usuario']
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
            'fecha_reserva': forms.DateInput(format="%Y-%m-%d", attrs={"class":"form-control", "readonly":"readonly"}),
            'hora_inicio': forms.TimeInput(format="%H:%M", attrs={"class":"form-control","readonly":"readonly"}),
            'hora_fin': forms.TimeInput(format="%H:%M", attrs={"class":"form-control","readonly":"readonly"}),
        }

class Reservaform(forms.ModelForm):

    class Meta:
        model= Reserva
        exclude = ['recurso_reservado', 'usuario']
        fields = [
            'fecha_reserva',
            'hora_inicio',
            'hora_fin',
            'estado_reserva',
        ]
        label = {

            'fecha_reserva': 'Fecha',
            'hora_inicio': 'Hora Inicio',
            'hora_fin': 'Hora Finalizacion',
            'estado_reserva':'Estado'
        }
        widgets = {
            'fecha_reserva': forms.DateInput(format="%Y-%m-%d",
                                             attrs={"class": "form-control form_datetime", "readonly": "readonly"}),
            'hora_inicio': forms.TimeInput(format="%H:%M", attrs={"class": "form-control form_time", "readonly": "readonly"}),
            'hora_fin': forms.TimeInput(format="%H:%M", attrs={"class": "form-control form_time", "readonly": "readonly"}),
            'estado_reserva': forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
        }

