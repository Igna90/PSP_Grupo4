from django import forms
from nucleo.models import Client,User



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = { 
                   'username': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your UserName'}),
                   'password': forms.PasswordInput (attrs={'class':'formset-field', 'placeholder': 'Write your Password'}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields=['dni', 'name', 'surname','address','birthDate']
        exclude = ("active",)
        widgets = { 
                   'dni': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your DNI'}),
                   'name': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your name'}),
                   'surname': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your surname'}),
                   'address': forms.TextInput (attrs={'class':'formset-field', 'placeholder': 'Write your address'}),
                   'birthDate': forms.DateInput (attrs={'class':'formset-field', 'placeholder': 'Write your birthdate'}),
        }
    
        
    # def save(self, commit=True):
    #     user = super(RegisterForm, self).save()
    #     user.save()
    #     return user
        
        
    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
        
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError('El username no se encuentra disponible')
        
    #     return username
    
# class CreateClient(CreateView):
       
    # name=forms.CharField(label="Name", required=True, widget=forms.TextInput(
    #     attrs={'class':'form-control', 'placeholder': 'Write your name'}
    # ))
    # dni=forms.CharField(label="DNI", required=True, widget=forms.TextInput(
    #     attrs={'class':'form-control', 'placeholder': 'Write your DNI'}
    # ))
    # surname=forms.CharField(label="Surname", required=True, widget=forms.TextInput(
    #     attrs={'class':'form-control', 'placeholder': 'Write your surname'}
    # ))
    # address=forms.CharField(label="Address", required=True, widget=forms.TextInput(
    #     attrs={'class':'form-control', 'placeholder': 'Write your address'}
    # ))
    # birhtDate=forms.DateField(label="Birthday",required=True, widget = forms.SelectDateWidget( 
    #     attrs={'class':'form-control'}
    # ))

#     class meta:
#         model = Client
#         fields = ['Name', 'DNI','Surname', 'Address','Birthday']
#         success_url="/"