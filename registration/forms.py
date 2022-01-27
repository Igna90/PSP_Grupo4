from django import forms
from nucleo.models import Project, User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','dni', 'name', 'surname','address','birthDate']
        labels = {
            'name': 'Nombre',
            'surname': 'Apellidos',
            'address': 'Dirección',
            'birthDate': 'Fecha de Nacimiento'
        }
        exclude = ("active",)
        widgets = { 
                   'username': forms.TextInput (attrs={'class':'formset-field','placeholder': 'Write your UserName'}),
                   'dni': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your DNI'}),
                   'name': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your name'}),
                   'surname': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your surname'}),
                   'address': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your address'}),
                   'birthDate': forms.DateInput (attrs={'class':'formset-field', 'placeholder': 'Write your birthdate'}),
                   'password': forms.PasswordInput (render_value=True,attrs={'placeholder': 'Write your password'}),
        }

class UserUpdateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','dni', 'name', 'surname','address','birthDate']
        exclude = ("active",)
        widgets = { 
                   'username': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your UserName'}),
                   'dni': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your DNI'}),
                   'name': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your name'}),
                   'surname': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your surname'}),
                   'address': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your address'}),
                   'birthDate': forms.DateInput (attrs={'class':'formset-field', 'placeholder': 'Write your birthdate'}),
                   'password': forms.PasswordInput (render_value=True,attrs={'placeholder': 'Write your password'}),
                   
        }
        
class EmployeeForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','dni', 'name', 'surname','address','biography']
        labels = {
            'name': 'Nombre',
            'surname': 'Apellidos',
            'address': 'Dirección',
            'biography': 'Biografía',
        }
        exclude = ("active","birthDate","registerDate")
        widgets = { 
                   'username': forms.TextInput (attrs={'class':'formset-field','placeholder': 'Write your UserName'}),
                   'dni': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your DNI'}),
                   'name': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your name'}),
                   'surname': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your surname'}),
                   'address': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your address'}),
                   'bioraphy': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your biography'}),
                   'password': forms.PasswordInput (render_value=True,attrs={'placeholder': 'Write your password'}),
        }
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','description', 'level', 'startDate','endDate','endReport','idCategory','idEmployee']
        labels = {
            'title': 'Titulo',
            'description': 'Descripción',
            'level': 'Nivel',
            'startDate': 'Fecha de inicio',
            'endDate': 'Fecha de fin',
            'endReport': 'Informe final',
            'idCategory' : 'Categoria',
            'idEmployee' : 'Empleado',
        }
        widgets = { 
                   'title': forms.TextInput (attrs={'class':'formset-field','placeholder': ' '}),
                   'description': forms.TextInput (attrs={'class':'formset-field', 'placeholder': ' '}),
                   'level': forms.TextInput (attrs={'class':'formset-field', 'placeholder': ' '}),
                   'startDate': forms.DateInput (attrs={'type':'date'}),
                   'endDate': forms.DateInput (attrs={'type':'date'}),
                   'endReport': forms.TextInput (attrs={'class':'formset-field', 'placeholder': ' '}),
                   'idCategory' : forms.TextInput (attrs={'class':'formset-field', 'placeholder': ' '}),
                   'idEmployee': forms.TextInput (attrs={'class':'formset-field', 'placeholder': ' '}),
        }