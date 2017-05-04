from django import forms

from app.recurso.models import Recurso1, TipoRecurso1, Caracteristica

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
        fields = [
            'tipo_id',
            'estado',
        ]
        labels = {
            'tipo_id': 'Tipo de Recurso',
            'estado': 'Estado del Recurso',
        }
        widgets = {
            'tipo_id': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(choices=ESTADO_CHOICE),
        }


class RecursoForm2(forms.ModelForm):
    class Meta:
        model = Recurso1
        fields = [
            'tipo_id',
        ]
        labels = {
            'tipo_id': 'Tipo de Recurso',
        }
        widgets = {
            'tipo_id': forms.Select(attrs={'class': 'form-control'}),
        }


class TipoRecursoForm(forms.ModelForm):
    class Meta:
        model = TipoRecurso1
        fields = [
            'nombre_recurso',
            'reservable',
            'fecha_mantenimiento',
        ]
        labels = {
            'nombre_recurso': 'Nombre del Recurso',
            'reservable': 'Indique si es reservable',
            'fecha_mantenimiento': 'Fecha de mantenimiento Preventivo',
        }
        widgets = {
            'nombre_recurso': forms.TextInput(attrs={'class': 'form-control'}),
            'reservable': forms.CheckboxInput(),
            'fecha_mantenimiento': forms.DateTimeInput(format="%Y-%m-%d %H:%M"),
        }


class TipoRecursoForm2(forms.ModelForm):
    class Meta:
        model = TipoRecurso1
        fields = [
            'nombre_recurso',
            'reservable',
            'fecha_mantenimiento',
            'ctra_id',
        ]
        labels = {
            'nombre_recurso': 'Nombre del Recurso',
            'reservable': 'Indique si es reservable',
            'fecha_mantenimiento': 'Fecha de mantenimiento Preventivo',
            'ctra_id': 'Caracteristicas Configurables',
        }
        widgets = {
            'nombre_recurso': forms.TextInput(attrs={'class': 'form-control'}),
            'reservable': forms.CheckboxInput(),
            'fecha_mantenimiento': forms.DateTimeInput(format="%Y-%m-%d %H:%M"),
            'ctra_id': forms.Select(attrs={'class': 'form-control'}),
        }


class CaractiristicaForm(forms.ModelForm):
    class Meta:
        model = Caracteristica
        fields = [
            'nombre_caracteristica',
            'activo',
        ]
        labels = {
            'nombre_caracteristica': 'Caracteristica Configurable',
            'activo': 'Indique si sera activada',
        }
        widgets = {
            'nombre_caracteristica': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput()
        }










