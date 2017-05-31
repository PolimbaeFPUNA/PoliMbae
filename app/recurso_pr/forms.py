from django import forms
from app.recurso_pr.models import  *

ESTADO_CHOICE = (('Disponible', 'Disponible'),
                     ('Reservado', 'Reservado'),
                     ('En Mantenimiento', 'En Mantenimiento'),
                     ('Solicitado', 'Solicitado'),
                     ('Fuera de Uso', 'Fuera de Uso'),
                     ('En Uso', 'En Uso'),
                 )


class RecursoForm(forms.ModelForm):
    class Meta:
        model = Recurso1
        exclude = ['estado']
        fields = [
            'tipo_id',
            'descripcion',
        ]
        labels = {
            'tipo_id': 'Tipo de Recurso',
            'descripcion': 'Identificador del Recurso',
        }
        widgets = {
            'tipo_id': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }




class TipoRecursoForm(forms.ModelForm):
    caracteristica= forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    class Meta:
        model = TipoRecurso1
        fields = [
            'nombre_recurso',
            'reservable',
        ]
        labels = {
            'nombre_recurso': 'Nombre del Recurso',
            'reservable': 'Indique si es reservable',
        }
        widgets = {
            'nombre_recurso': forms.TextInput(attrs={'class': 'form-control'}),
            'reservable': forms.CheckboxInput(),
        }


class TipoRecursoForm2(forms.ModelForm):
    class Meta:
        model = TipoRecurso1
        fields = [
            'nombre_recurso',
            'reservable',

        ]
        labels = {
            'nombre_recurso': 'Nombre del Recurso',
            'reservable': 'Indique si es reservable',

        }
        widgets = {
            'nombre_recurso': forms.TextInput(attrs={'class': 'form-control'}),
            'reservable': forms.CheckboxInput(),

        }


class ListCaracteristicaForm(forms.ModelForm):
    caracts = forms.ModelChoiceField(queryset=Caracteristica.objects.filter(tipo_recurso__isnull=True),
                                     widget=forms.CheckboxSelectMultiple())
    class Meta:
        model= Caracteristica
        exclude = '__all__'


class DescripcionForm(forms.ModelForm):
    class Meta:
        model= DescripCarac
        fields = [
            'ctra_id',
            'descripcion',
            'recurso',
        ]
        labels = {
            'ctra_id': 'Caracteristica',
            'descripcion': 'Descripcion',
            'recurso': 'Recurso',
        }
        widgets= {
            'ctra_id': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'recurso': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CaracteristicaForm(forms.ModelForm):
    class Meta:
        exclude = ['tipo_recurso']
        model = Caracteristica
        fields = [
            'nombre_caracteristica',
            'descripcion',
        ]
        labels = {
            'nombre_caracteristica': 'Nombre de la Caracteristica',
            'descripcion': 'Descripcion',

        }
        widgets = {
            'nombre_caracteristica': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),

        }