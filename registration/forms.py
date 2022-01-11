from django import forms
from nucleo.models import User
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
        }

class UserUpdateForm(forms.ModelForm):
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
        }

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']
#         widgets = { 
#                    'username': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your UserName'}),
#                    'password': forms.PasswordInput (attrs={'class':'formset-field', 'placeholder': 'Write your Password'}),
#         }

# class ClientForm(forms.ModelForm):
#     class Meta:
#         model = Client
#         fields=['dni', 'name', 'surname','address','birthDate']
#         exclude = ("active",)
#         widgets = { 
#                    'dni': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your DNI'}),
#                    'name': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your name'}),
#                    'surname': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your surname'}),
#                    'address': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your address'}),
#                    'birthDate': forms.DateInput (attrs={'class':'formset-field', 'placeholder': 'Write your birthdate'}),
#         }
    
#     def save(self, commit=True):
#         user = User.objects.last()
#         self.instance.idUser = user
#         super(ClientForm,self).save(commit)