from django import forms
from app.mantenimiento.models import Mantenimiento
from app.recurso_pr.models import TipoRecurso1, Recurso1

TIPOS = (

    ('Preventivo', 'Preventivo'),
    ('Correctivo', 'Correctivo'),

)

class MantForm(forms.ModelForm):
    tipo_recurso = forms.ModelChoiceField(queryset= TipoRecurso1.objects.all(), widget=forms.Select(attrs={"class":"form-control"}))

    class Meta:
        model = Mantenimiento
        exclude = ['tipo_recurso', 'recurso']
        fields = [

            'fecha_entrega',
            'fecha_fin',
            'hora_entrega',
            'hora_fin',
            'tipo',
        ]

        labels = {

            'fecha_entrega': 'Fecha de Entrega',
            'fecha_fin': 'Fecha de Devolucion',
            'hora_entrega': 'Hora de Entrega',
            'hora_fin': 'Hora de Devolucion',
            'tipo': 'Tipo',
        }

        widgets = {
            'fecha_entrega': forms.DateInput(format="%d-%m-%Y", attrs={"class":"form-control form_datetime"}),
            'fecha_fin': forms.DateInput(format="%d-%m-%Y", attrs={"class":"form-control form_datetime"}),
            'hora_entrega': forms.TimeInput(format="%H:%M", attrs={"class":"form-control form_time"}),
            'hora_fin': forms.TimeInput(format="%H:%M", attrs={"class": "form-control form_time"}),
            'tipo': forms.Select(choices=TIPOS, attrs={"class":"form-control"}),
        }

class ListRecursoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        tipo = kwargs.pop('tipo')
        super(ListRecursoForm, self).__init__(*args, **kwargs)
        self.fields['lista'] = forms.ModelChoiceField(queryset=Recurso1.objects.filter(tipo_id=tipo), widget=forms.Select(attrs={"class":"form-control"}))

class ChoiceForm(forms.ModelForm):
    class Meta:
        model= Mantenimiento
        exclude = ['tipo_recurso', 'recurso']
        fields = [
            'fecha_entrega',
            'fecha_fin',
            'hora_entrega',
            'hora_fin',
            'tipo',
        ]
        labels = {
            'fecha_entrega': 'Fecha de Entrega',
            'fecha_fin': 'Fecha de Devolucion',
            'hora_entrega': 'Hora de Entrega',
            'hora_fin': 'Hora de Devolucion',
            'tipo': 'Tipo',
        }
        widgets= {
            'fecha_entrega': forms.DateInput(format="%d-%m-%Y", attrs={"class": "form-control form_datetime"}),
            'fecha_fin': forms.DateInput(format="%d-%m-%Y", attrs={"class": "form-control form_datetime"}),
            'hora_entrega': forms.TimeInput(format="%H:%M", attrs={"class": "form-control form_time"}),
            'hora_fin': forms.TimeInput(format="%H:%M", attrs={"class": "form-control form_time"}),
            'tipo': forms.Select(choices=TIPOS, attrs={"class":"form-control"}),
        }