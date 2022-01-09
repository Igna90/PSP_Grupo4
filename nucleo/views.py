from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from registration.forms import UserForm, UserUpdateForm

from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpRequest


def index(request):
    return render(request, "nucleo/index.html")

class FormularioClientView(HttpRequest):
    def index(request):
        userForm = UserForm()
        return render(request, "registration/register.html", {"form":userForm})
    def procesar_formulario(request):
        userForm = UserForm(request.POST)
        if request.method =='POST' and  userForm.is_valid():
            userForm.save()
            return redirect(('index'))
        return render(request, "registration/register.html", {"form":userForm})
            
def login_view(request):
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Bienvenid@ {}'.format(user.username))
                return redirect('index')
            else:
                messages.error(request, "Usuario o contraseña no validos")
        return render(request, "registration/login.html", {})
 
@login_required    
def profile(request):
    if request.method=="POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # messages.success(request, f'El perfil ha sido actualizado')
            return redirect('index')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form':form 
    }
    return render(request, 'nucleo/profile.html', context)