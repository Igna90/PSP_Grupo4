from django import forms
from django.db import models
from nucleo.models import Category, User
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
    
    password1=forms.CharField(required=False,widget=forms.PasswordInput(attrs={'class': 'form-control mb2', 'placeholder': 'Contraseña'}), label="Contraseña")
    password2=forms.CharField(required=False,widget=forms.PasswordInput(attrs={'class': 'form-control mb2', 'placeholder': 'Repite contraseña'}), label="Repite Contraseña")
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
                   'birthDate': forms.DateInput (attrs={'type':'date', 'placeholder': 'Write your birthdate'}),
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
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','image']
        labels = {
            'name': 'Nombre',
            'image': 'Imagen',
        }
class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','image']
        labels = {
            'name': 'Nombre',
            'image': 'Imagen',
        }
       