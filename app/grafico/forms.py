from django import forms
from app.mantenimiento.models import Mantenimiento
from app.recurso.models import TipoRecurso1, Recurso1


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
