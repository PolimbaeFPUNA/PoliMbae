from django import forms

from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm
from app.usuario.models import Profile

INS = 1
TIT = 2
ADJ = 3
ASI = 4
ENC = 5
AUX = 6
ALU = 7
FUN = 8
CATEGORIA_CHOICE = ((INS, 'Institucional'),
                    (TIT, 'Titular'),
                    (ADJ, 'Adjunto'),
                    (ASI, 'Asistente'),
                    (ENC, 'Encargado de Catedra'),
                    (AUX, 'Auxiliar de Ensenanza'),
                    (ALU, 'Alumno'),
                    (FUN, 'Funcionario'),
                    )


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'email',
                  'username',
                  'password1',
                  'password2',
                  ]

        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Email',
            'username': 'Nombre de Usuario',
            'password1': 'Password',
            'password2': 'Vuelva a repetir su Password',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

        # clean email field
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Ya hay un usuario registrado con este mismo email')

    # modificamos el metodo save() asi podemos definir  user.is_active a False la primera vez que se registra
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False  # No esta activo hasta que active el vinculo de verificacion
            user.save()

        return user


class UsuarioForm(forms.ModelForm):
    class Meta:
        exclude = ['categoria']
        model = Profile
        fields = [
            'direccion',
            'telefono',
            'cedula',
        ]

        labels = {
            'direccion' : 'Direccion',
            'telefono' : 'Telefono',
            'cedula': 'Cedula',
        }

        widgets = {
            'direccion' :  forms.TextInput(attrs={'class': 'form-control'}),
            'telefono':  forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),

        }

class UsuarioForm2(forms.ModelForm):
    class Meta:
        exclude = ['categoria']
        model = Profile
        fields = [
            'user',
            'direccion',
            'telefono',
            'cedula',
        ]

        labels = {
            'user': 'Username',
            'direccion' : 'Direccion',
            'telefono' : 'Telefono',
            'cedula': 'Cedula',
        }

        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'direccion' :  forms.TextInput(attrs={'class': 'form-control'}),
            'telefono':  forms.TextInput(attrs={'class': 'form-control'}),
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

class UsuariocategoriaForm(forms.ModelForm):
    class Meta:
        exclude = [ 'direccion', 'telefono', 'cedula',]
        model = Profile
        fields = [
            'categoria',
        ]
        labels = {
            'categoria' : 'Categoria',
        }
        widgets = {
            'categoria': forms.Select(choices=CATEGORIA_CHOICE, attrs={'class':'form-control'}),
        }


class AsignarForm(forms.ModelForm):
    group = forms.ModelChoiceField(label='Rol',queryset=Group.objects.all(),
                                   required=True,widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:

        model = User
        fields = ['group']

