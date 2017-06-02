from django import forms
from app.usuario.models import Profile
from app.rol.models import UserRol, PermisoRol

from django.contrib.auth.models import Permission,Group


'''Clase para crear el formulario que refleja los atributos del modelo para crear las vistas y los
    templates'''

''' Formulario para el modelo Rol'''


class RolForm(forms.ModelForm):
    class Meta:
        """ Se importa el modelo del Rol
            fields: para referenciar al modelo Rolusuario
            labels: nombres que apareceran en los templates para cada campo
            widgets: tipo de comportamiento a mostrar en los templates, los inputs elements"""
        model = UserRol
        # Lista los campos que se desea tener en el formulario
        fields = [
            #'nombre_rol',
            'descripcion',
        ]
        # Escribir un diccionario para tener los nombres asociados a los atributos del modelo Rol

        labels = {
            #'nombre_rol': 'Nombre de Rol',
            'descripcion': 'Descripcion',
        }
        # Se define la forma en que se van a presentar los datos del formulario en etiquetas html

        widgets = {
            #'nombre_rol': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

''' Formulario para el Modelo Permiso, incluyendo el rol_id pk'''


class PermisoForm(forms.ModelForm):
    class Meta:
        model = PermisoRol
        fields = [
            'permiso',
            'activo',
            'rol_id',
        ]
        labels = {
            'permiso': 'Nombre del Permiso',
            'activo': 'Activar Permiso',
            'rol_id': 'Elija el Rol a asignar el nuevo Permiso',
        }
        widgets = {
            'permiso': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(),
            'rol_id': forms.Select(attrs={'class': 'form-control'}),
        }


''' Formulario para el Modelo Permiso obviando el rol_id pk para usar formulario doble'''


class PermisoForm2(forms.ModelForm):
    class Meta:
        model = PermisoRol
        fields = [
            'permiso',
            'activo',
        ]
        labels = {
            'permiso': 'Nombre del Permiso',
            'activo': 'Activar Permiso',
        }
        widgets = {
            'permiso': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(),
        }


class AsignarRolForm(forms.Form):
    class Meta:
        model = Profile

        fields = [
            'cedula',
            'rol',
        ]

        labels = {
            'cedula': 'cedula',
            'rol': 'rol',
        }
        widgets = {
            'cedula': forms.TextInput(),
            'rol': forms.Select()
        }

class RolGrupo(forms.ModelForm):
    class Meta:
        model= Group
        fields=[
            'name',
            'permissions',
        ]
        labels={
            'name':'Rol',
            'permissions':'Permisos',
        }
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'permissions':forms.CheckboxSelectMultiple(),
        }

class PermisoGrupo(forms.ModelForm):
    class Meta:
        model=Permission

        fields=[
            'codename',
            'name',
        ]
        labels={
            'codename':'Permiso',
            'name':'Descripcion',
        }
        widgets={
            'codename':forms.TextInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
        }