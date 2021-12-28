
from django import forms
from django.http import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate,login
from nucleo.models import Client, User

from registration.forms import ClientForm, UserForm

from django.contrib import messages
from django.contrib.auth import logout
from django.views.generic.edit import CreateView
from django.http import HttpRequest


# def index(request):
#     return render(request, "nucleo/index.html")

class FormularioClientView(HttpRequest):
    def index(request):
        client = ClientForm()
        user = UserForm()
        return render(request, "registration/register.html", {"form2":user,"form":client})
    def procesar_formulario(request):
        # client = ClientForm(request.POST)
        user = UserForm(request.POST)
        if request.method =='POST' and  user.is_valid():

            user.save()
        userId =  User.objects.last()
        # if request.method =='POST' and  client.is_valid():
        #     Client.objects.create()
        return render(request, "registration/register.html", {"form2":user,"mensaje": 'OK'})
        


# class registerClient(CreateView):
#     register_form = UserCreationForm()
#     template_name='registration/register.html'
    
#     def get_success_url(self):
#         return reverse_lazy('login')+'?register'
    
#     def get_form(self, form_class=None):
#         form=super(registerClient,self).get_form()
#         form.fields['username'].widget=forms.TextInput(attrs={'class':'form-control mb2','placeholder':'Nombre de usuario'})
#         form.fields['password'].widget=forms.TextInput(attrs={'class':'form-control mb2','placeholder':'Nombre de usuario'})
#         return form        
        
        
    # if request.method=="POST" and register_form.is_valid():
    #         username = register_form.cleaned_data.get('username')
    #         password = register_form.cleaned_data.get('password')
            # name=request.POST.get('name','')
            # dni=request.POST.get('dni','')
            # surname=request.POST.get('surname','')
            # address=request.POST.get('address','')
            # birhtDate=request.POST.get('birhtDate','')
            
    #         if user:
    #             login(request,user)
    #             messages.success(request, 'Bienvenido {}'.format(user.username))
    #         return redirect(('index'))
        
        
    # return render(request, "registration/register.html", {"form":register_form})

def login_view(request):
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Bienvenido {}'.format(user.username))
                return redirect('index')
            else:
                messages.error(request, "Usuario o contraseña no validos")
        return render(request, "registration/login.html", {})

# class HomePageView(TemplateView):
#     template_name="nucleo/client.html"

# class ClientCreateView(CreateView):
#     model=Client
#     fields=['dni', 'name', 'surname', 'address','birthDate','active','idUser']
#     success_url="/"