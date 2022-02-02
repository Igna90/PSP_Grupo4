from audioop import reverse
from contextlib import nullcontext
import datetime
from http.client import HTTPResponse
from msilib.schema import ListView
from multiprocessing import context
from multiprocessing.connection import Client
import os
from re import template
<<<<<<< HEAD

=======
>>>>>>> 36b6291334e108c523fcee737863c63fc2238683
from tkinter.tix import MAX, Select
from unicodedata import name
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.views import View
from nucleo.models import Category, Participate, Project, User
from registration.forms import EditCategoryForm, EmployeeForm, UserForm, UserUpdateForm,CategoryForm
from registration.forms import EmployeeForm, ProjectForm, UserForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, request
from django.views.generic import DeleteView,UpdateView, DetailView, ListView,TemplateView
from django.db.models import Q


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
            return redirect(('userList'))
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
            return redirect(('employeeList'))
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
    
class FormularioProjectView(HttpRequest):
    def index(request):
        projectForm = ProjectForm()
        return render(request, "nucleo/users/create_proj.html", {"form":projectForm})
    def procesar_formulario(request):
        projectForm = ProjectForm(request.POST)
        project = projectForm.save(commit=False)
        project.idEmployee = request.user
        if project.endDate < project.startDate:
            messages.error(request, "La fecha final de proyecto debe ser mayor a la de inicio")
            return redirect(('createProject'))
            
        
        if request.method =='POST' and  projectForm.is_valid():
            project.save()
            messages.success(request, "El proyecto se ha creado correctamente")
            return redirect(('listProjects'))
        return render(request, "nucleo/users/create_proj.html", {"form":projectForm})
            
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

class EmployeeList(ListView):
    model=User
    template_name="nucleo/admin/employee_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(role_user='Empleado')
        return context
    
class UserList(ListView):
    model=User
    template_name="nucleo/admin/user_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(role_user='Cliente')
        return context

class UserDeleteView(DeleteView):
    model= User
    template_name='nucleo/admin/delete.html'
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
        if(self.object.role_user =="Cliente"):
            return HttpResponseRedirect('/userList/')
        else:
            return HttpResponseRedirect('/employeeList/')
    
class UserUpdateView(UpdateView):
        model= User
        form_class = UserForm
        template_name='nucleo/admin/update.html'
        
        def dispatch(self, request, *args, **kwargs):
            self.object = self.get_object()
            return super().dispatch(request, *args, **kwargs)
        
        def get_success_url(self):
            return '/userList/'
            
class EmployeeUpdateView(UpdateView):
        model= User
        form_class = EmployeeForm
        template_name='nucleo/admin/update.html'
        
        def dispatch(self, request, *args, **kwargs):
            self.object = self.get_object()
            return super().dispatch(request, *args, **kwargs)
        
        def get_success_url(self):
            return '/employeeList/'
    
class ProjectDeleteView(DeleteView):
    model= Project
    template_name='nucleo/users/deleteproject.html'
    succes_url = reverse_lazy('nucleo:projects_list')
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
        return HttpResponseRedirect('/listProjects/')
    
class ProjectUpdateView(UpdateView):
        model= Project
        form_class = ProjectForm
        template_name='nucleo/users/updateproject.html'
        
        def dispatch(self, request, *args, **kwargs):
            self.object = self.get_object()
            return super().dispatch(request, *args, **kwargs)
    
        def get_success_url(self):
            return '/listProjects/'

class ParticipateView(ListView):
    model = Participate
    template_name="nucleo/users/participate_list.html"
    
    def get_context_data(self,**kwargs):
        now = datetime.datetime.now()
        context = super().get_context_data(**kwargs)
        if(self.request.user.role_user == "Empleado"):
            context['participates'] = Project.objects.filter(idEmployee_id=self.request.user.id,endDate__lt=now).order_by("startDate")
        else:
            project = Project.objects.filter(endDate__lt=now).order_by("startDate")
            context['participates'] = Participate.objects.filter(idCliente_id = self.request.user.id,idProject_id__in=project)
        return context
    
def project_participate(request,pk):
    projects = Project.objects.filter(pk=pk)
    isParticipates = Participate.objects.filter(idProject_id=pk).filter(idCliente_id=request.user.id).exists()
    if (isParticipates == False):
        context = {
            'projects' : projects,
            }
        return render(request,"nucleo/users/project_participate.html",context)
    else:
        return render(request,'nucleo/users/is_participate.html')

def agregarParticipa(request,pk):
    if request.method=="POST":
        idProjecto=Project.objects.get(pk=pk)
        cliente=request.user.id
        now = datetime.datetime.now()
        participate = Participate.objects.create(idCliente_id=cliente, idProject = idProjecto, registrationDate = now,rol="null")
        participate.save()
        messages.success(request,"Has sido inscrito satisfactoriamente")
        return redirect(("listProjects"))
    
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
<<<<<<< HEAD
    template_name="nucleo/project_list.html"
=======
    template_name="nucleo/users/project_list.html"
>>>>>>> 36b6291334e108c523fcee737863c63fc2238683
    
    def get_queryset(self):
        query = self.request.GET.get('buscar')
        if query:
            object_list = self.model.objects.filter(idCategory=query)
        else:
             object_list = self.model.objects.all()    
        return object_list

    def get_context_data(self, **kwargs):
        now = datetime.datetime.now()
        context = super().get_context_data(**kwargs)
        context['projectsDates'] = Project.objects.filter(startDate__gt=now)
        context['categorys'] = Category.objects.all()
        return context

class EmployeeProjectView(ListView):
    model = Project
    template_name="nucleo/users/employee_project.html"
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(idEmployee_id=self.request.user.pk)
        return context

class ClientProjectView(ListView):
    model = Participate
    template_name="nucleo/users/client_project.html"
    
    def post(self,*args,**kwargs):
        if self.request.method == "POST":
            role = self.request.POST.get('rol')
            id = self.request.POST.get('id')
            idProject = self.request.POST.get('idProject')
            Participate.objects.filter(pk=id).update(rol = role)
            participates = Participate.objects.filter(idProject_id = idProject)
            return render(self.request,'nucleo/users/client_project.html',{'participates':participates})
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        idProject = self.request.GET.get('idProject')
        context['participates'] = Participate.objects.filter(idProject_id = idProject)
        return context 

class CategoryListView(ListView):
    model=Category
    template_name="nucleo/admin/category_list.html"
    
class editCategory(UpdateView):
    model= Category
    form_edit = EditCategoryForm
    template_name='nucleo/admin/category_form.html'
    fields = ['name','image']
    def get_success_url(self):
        return '/categoryList/'
    
class CategoryDeleteView(DeleteView):
    model= Category
    template_name='nucleo/admin/delete_category.html'
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


class ProjectNextWeekListView(ListView):
    model=Project
    template_name="nucleo/ListNextWeek_list.html"
<<<<<<< HEAD

    @staticmethod
    def get_next_week():
        now = datetime.datetime.now()
        weekDayNow = now.weekday()
        diasRestantes = 6 - weekDayNow
        monday = now + datetime.timedelta(diasRestantes)
        sunday = monday + datetime.timedelta(6)
        return Project.objects.filter(startDate__gt=monday, startDate__lt=sunday)
      
=======
    projects = Project.objects.all()    
    # print(item[0].startDate.weekday())
    @staticmethod
    def get_next_week():
        now = datetime.datetime.now()
        # print(project.startDate.weekday())
        weekDayNow = now.weekday()
        diasRestantes = 7 - weekDayNow
        
        monday = weekDayNow + diasRestantes
        sunday = monday + 6
        return Project.objects.filter(startDate__gt=monday, startDate__lt=sunday)
    
>>>>>>> 36b6291334e108c523fcee737863c63fc2238683
    def get_context_data(self, **kwargs):
        now = datetime.datetime.now()
        context = super().get_context_data(**kwargs)
        context['projectsDates'] = self.get_next_week()
        return context