from django import forms

from django.contrib.auth.models import User,Group

from app.usuario.models import Profile, CategoriaUsuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model= Profile

        fields = [

            'direccion',
            'telefono',
            'categoria',
            'cedula',
        ]

        labels = {

            'direccion' : 'Direccion',
            'telefono' : 'Telefono',
            'categoria': 'Categoria',
            'cedula': 'Cedula',
        }

        widgets = {

            'direccion' :  forms.TextInput(attrs={'class': 'form-control'}),
            'telefono':  forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),



        }

class UserForm(forms.ModelForm):
    password2 = forms.CharField(label='Confirmar Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model= User

        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        ]

        labels = {
            'username':'Username',
            'email':'Email',
            'first_name':'Nombre',
            'last_name':'Apellido',
            'password': 'Password',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
class UserEditable(forms.ModelForm):
    class Meta:
        model= User

        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]

        labels = {
            'username':'Username',
            'email':'Email',
            'first_name':'Nombre',
            'last_name':'Apellido',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
class CategoriaForm(forms.ModelForm):
    class Meta:
        model= CategoriaUsuario

        fields = [
            'nombre',
        ]
        labels = {
            'nombre': 'Nombre'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AsignarForm(forms.ModelForm):
    group = forms.ModelChoiceField(label='Rol',queryset=Group.objects.all(),
                                   required=True,widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = [ 'group']
