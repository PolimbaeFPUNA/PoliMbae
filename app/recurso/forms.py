from django import forms
from app.recurso.models import Recurso
from app.recurso.models import TipoRecurso


class RecForm(forms.ModelForm):
    class Meta:
        model = Recurso
        # Lista los campos que se desea tener en el formulario
        exclude = ['codigo_rec']
        fields = [
            'nombre_rec'
            'tipo_rec'
            'estado'
        ]
        # Escribir un diccionario para tener los nombres asociados a los atributos del modelo Recurso

        labels = {
            'nombre_rec': 'Nombre del Recurso',
            'tipo_rec': 'Tipo de Recurso',
            'estado': 'Estado',
            }
        # Se define la forma en que se van a presentar los datos del formulario en etiquetas html

        widgets = {
            'nombre_rec': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_rec': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
        }
