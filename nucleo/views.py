from msilib.schema import ListView
from multiprocessing.connection import Client
import os
from re import template
from tkinter.tix import Select
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.views import View
from nucleo.models import Category, Participate, Project, User
from registration.forms import EditCategoryForm, EmployeeForm, UserForm, UserUpdateForm,CategoryForm
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, request
from django.views.generic import DeleteView,UpdateView, DetailView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

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
            messages.success(request, "El usuario ha sido registrado correctamente, vaya a acceder para comenzar")
            return redirect(('index'))
        return render(request, "registration/register.html", {"form":userForm})

class FormularioEmployeeView(HttpRequest):
    def index(request):
        userForm = EmployeeForm()
        return render(request, "registration/create_emp.html", {"form":userForm})
    def procesar_formulario(request):
        userForm = EmployeeForm(request.POST)
        if request.method =='POST' and  userForm.is_valid():
            formulario = userForm.save()
            formulario.role_user = 'Empleado'
            formulario.save()
            messages.success(request, "El usuario ha sido registrado correctamente")
            return redirect(('index'))
        return render(request, "registration/create_emp.html", {"form":userForm})

    
class FormCreateCategoryView(HttpRequest):
    def index(request):
        catForm = CategoryForm()
        return render(request, "registration/create_cat.html", {"form":catForm})
    def procesar_formulario(request):
        catForm = CategoryForm(request.POST, request.FILES)
        if request.method =='POST' and  catForm.is_valid():
            
            
            catForm.save()
            messages.success(request, "La categoria ha sido registrada correctamente")
            return redirect(('categoryList'))
        return render(request, "registration/create_cat.html", {"form":catForm})
            
class login_view(HttpRequest):
    def loginUser(request):
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                item = User.objects
                login(request, user)
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
            messages.success(request, "Tu usuario ha sido editado con exito, por seguridad necesitas volver a loguearte.")
            return redirect('index')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form':form 
    }
    return render(request, 'nucleo/profile.html', context)

def logout_request(request):
     logout(request)
     messages.success(request,"Has salido satisfactoriamente")
     return redirect("index")
     
def EmployeeList(request):
    items = User.objects.filter(role_user='Empleado')
    
    context={
        'items': items,
    }

    return render(request, 'nucleo/employee_list.html', context )

def UserList(request):
    
    items = User.objects.filter(role_user='Cliente')
    
    context = {
        'items' : items,
    }
    
    return render(request,'nucleo/user_list.html',context)

class UserDeleteView(DeleteView):
    model= User
    template_name='nucleo/delete.html'
    succes_url = reverse_lazy('nucleo:user_list')
    url_redirect = succes_url
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data={}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponseRedirect('/userList/')
    
class UserUpdateView(UpdateView):
        model= User
        form_class = UserForm
        template_name='nucleo/update.html'
        
        def dispatch(self, request, *args, **kwargs):
            self.object = self.get_object()
            self.object
            return super().dispatch(request, *args, **kwargs)
        
        def get_success_url(self):
            if(self.object.role_user=="Cliente"):
                return HttpResponseRedirect('/userList/')
            else:
                return HttpResponseRedirect('/employeeList/')
            

def ActiveUser(request,pk):
    u = User.objects.get(id=pk)
    u.active = True
    u.save()
    return HttpResponseRedirect('/userList/')

def DeactiveUser(request,pk):
    u = User.objects.get(id=pk)
    u.active = False
    u.save()
    return HttpResponseRedirect('/userList/')

class SignProject(HttpRequest):
     def register(request,pk):
           a = User.objects.get(id=pk)
           b = Participate.objects.create()


class ProjectListView(ListView):
    model=Project     
class ProjectDetailView(DetailView):
    model=Project

class CategoryListView(ListView):
    model=Category
    
class editCategory(UpdateView):
    model= Category
    form_edit = EditCategoryForm
    template_name='nucleo/category_form.html'
    fields = ['name','image']
    def get_success_url(self):
        return '/categoryList/'
    
    
    
class CategoryDeleteView(DeleteView):
    model= Category
    template_name='nucleo/delete_category.html'
    succes_url = reverse_lazy('nucleo:categoryList')
    url_redirect = succes_url
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data={}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponseRedirect('/categoryList/')
    
