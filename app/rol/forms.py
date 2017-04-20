from django import forms
from app.rol.models import Rolusuario


class RolForm(forms.ModelForm):
    class Meta:
        model = Rolusuario
        # Lista los campos que se desea tener en el formulario
        exclude = ['id_rol']
        fields = [
            'nombre_rol',
            'descripcion',
            'crear_usuario',
            'modificar_usuario',
            'eliminar_usuario',
            'crear_rol',
            'modificar_rol',
            'eliminar_rol',
            'crear_recurso',
            'modificar_recurso',
            'eliminar_recurso',
            'consultar_recurso',
            'crear_reserva',
            'modificar_reserva',
            'eliminar_reserva',
            'consultar_reserva',
            'crear_mantenimiento',
            'modificar_mantenimiento',
            'eliminar_mantenimiento',
        ]
        # Escribir un diccionario para tener los nombres asociados a los atributos del modelo Rol

        labels = {
            'nombre_rol': 'Nombre de Rol',
            'descripcion': 'Descripcion',
            'crear_usuario': 'Crear Usuario',
            'modificar_usuario': 'Modificar Usuario',
            'eliminar_usuario': 'Eliminar Usuario',
            'crear_rol': 'Crear Rol',
            'modificar_rol': 'Modificar Rol',
            'eliminar_rol': 'Eliminar Rol',
            'crear_recurso': 'Crear Recurso',
            'modificar_recurso': 'Modificar Recurso',
            'eliminar_recurso': 'Eliminar Recurso',
            'consultar_recurso': 'Consultar Recurso',
            'crear_reserva': 'Crear Reserva',
            'modificar_reserva': 'Modificar Reserva',
            'eliminar_reserva': 'Eliminar Reserva',
            'consultar_reserva': 'Consultar Reserva',
            'crear_mantenimiento': 'Crear Mantenimiento',
            'modificar_mantenimiento': 'Modificar Mantenimiento',
            'eliminar_mantenimiento': 'Eliminar Mantenimiento',
        }
        # Se define la forma en que se van a presentar los datos del formulario en etiquetas html

        widgets = {
            'nombre_rol': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'crear_usuario': forms.CheckboxInput(),
            'modificar_usuario': forms.CheckboxInput(),
            'eliminar_usuario': forms.CheckboxInput(),
            'crear_rol': forms.CheckboxInput(),
            'modificar_rol': forms.CheckboxInput(),
            'eliminar_rol': forms.CheckboxInput(),
            'crear_recurso': forms.CheckboxInput(),
            'modificar_recurso': forms.CheckboxInput(),
            'eliminar_recurso': forms.CheckboxInput(),
            'consultar_recurso': forms.CheckboxInput(),
            'crear_reserva': forms.CheckboxInput(),
            'modificar_reserva': forms.CheckboxInput(),
            'eliminar_reserva': forms.CheckboxInput(),
            'consultar_reserva': forms.CheckboxInput(),
            'crear_mantenimiento': forms.CheckboxInput(),
            'modificar_mantenimiento': forms.CheckboxInput(),
            'eliminar_mantenimiento': forms.CheckboxInput(),
        }
