from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.contrib.auth import authenticate,login
from nucleo.models import User

from registration.forms import ClientForm, UserForm

from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpRequest


def index(request):
    return render(request, "nucleo/index.html")

class FormularioClientView(HttpRequest):
    def index(request):
        clientForm = ClientForm()
        userForm = UserForm()
        return render(request, "registration/register.html", {"form2":userForm,"form":clientForm})
    def procesar_formulario(request):
        clientForm = ClientForm(request.POST)
        userForm = UserForm(request.POST)
        
        if request.method =='POST' and  userForm.is_valid() and clientForm.is_valid():
            userForm.save()
            clientForm.save()
            return redirect(('index'))
        return render(request, "registration/register.html", {"form2":userForm,"form":clientForm})
        

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
