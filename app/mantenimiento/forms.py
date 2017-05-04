from django import forms
from app.mantenimiento.models import Mantenimiento
from app.recurso.models import TipoRecurso1, Recurso1

TIPOS = (

    ('Preventivo', 'Preventivo'),
    ('Correctivo', 'Correctivo'),

)
RESULTADO = (
        ('Funcional', 'Funcional'),
        ('No Funcional', 'No Funcional'),
        ('Pendiente', 'Pendiente'),
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
            'resultado',
            'tipo',
        ]

        labels = {

            'fecha_entrega': 'Fecha de Entrega',
            'fecha_fin': 'Fecha de Devolucion',
            'hora_entrega': 'Hora de Entrega',
            'hora_fin': 'Hora de Devolucion',
            'resultado': 'Resultado',
            'tipo': 'Tipo',
        }

        widgets = {
            'fecha_entrega': forms.DateInput(format="%Y-%m-%d", attrs={"class":"form-control"}),
            'fecha_fin': forms.DateInput(format="%Y-%m-%d", attrs={"class":"form-control"}),
            'hora_entrega': forms.TimeInput(format="%H:%M", attrs={"class":"form-control"}),
            'hora_fin': forms.TimeInput(format="%H:%M", attrs={"class": "form-control"}),
            'resultado': forms.Select(choices=RESULTADO, attrs={"class":"form-control"}),
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
            'resultado',
            'tipo',
        ]
        labels = {
            'fecha_entrega': 'Fecha de Entrega',
            'fecha_fin': 'Fecha de Devolucion',
            'hora_entrega': 'Hora de Entrega',
            'hora_fin': 'Hora de Devolucion',
            'resultado': 'Resultado',
            'tipo': 'Tipo',
        }
        widgets= {
            'fecha_entrega': forms.DateInput(format="%Y-%m-%d", attrs={"class":"form-control"}),
            'fecha_fin': forms.DateInput(format="%Y-%m-%d", attrs={"class":"form-control"}),
            'hora_entrega': forms.TimeInput(format="%H:%M", attrs={"class":"form-control"}),
            'hora_fin': forms.TimeInput(format="%H:%M", attrs={"class": "form-control"}),
            'resultado': forms.Select(choices=RESULTADO, attrs={"class":"form-control"}),
            'tipo': forms.Select(choices=TIPOS, attrs={"class":"form-control"}),
        }