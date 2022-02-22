from audioop import reverse
import datetime
from io import BytesIO
from msilib import Table
from msilib.schema import ListView
from multiprocessing import context
from multiprocessing.connection import Client
from unicodedata import name

from django.conf import settings
from django.utils.decorators import method_decorator

from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.views import View
from nucleo.decorators import is_active, is_admin, is_client, is_employee, is_not_admin
from nucleo.models import Category, Participate, Project, User
from registration.forms import EditCategoryForm, EmployeeForm, UserForm, UserUpdateForm,CategoryForm
from registration.forms import EmployeeForm, ProjectForm, UserForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import DeleteView,UpdateView, ListView

from reportlab.pdfgen import canvas
from reportlab.platypus import Table,TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER

def index(request):
    return render(request, "nucleo/index.html")


class FormularioClientView(HttpRequest):
    def index(request):
        userForm = UserForm()
        return render(request, "registration/register.html", {"form":userForm})
    def procesar_formulario(request):
        now = datetime.date.today()
        userForm = UserForm(request.POST)
        user = userForm.save(commit=False)
        user.idEmployee = request.user
        if user.birthDate >= now:
            messages.error(request, "La fecha de nacimiento no puede ser posterior a hoy")
            return redirect(('createClient'))
        if request.method =='POST' and  userForm.is_valid():
            now = datetime.datetime.now()    
            formulario = userForm.save()
            formulario.registerDate = now
            formulario.save()
            messages.success(request, "El usuario ha sido registrado correctamente.")
            return redirect(('userList'))
        return render(request, "registration/register.html", {"form":userForm})

class FormularioEmployeeView(HttpRequest):
    @is_admin
    def index(request):
        userForm = EmployeeForm()
        return render(request, "registration/create_emp.html", {"form":userForm})
    @is_admin
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
    @is_admin
    def index(request):
        catForm = CategoryForm()
        return render(request, "registration/create_cat.html", {"form":catForm})
    @is_admin
    def procesar_formulario(request):
        catForm = CategoryForm(request.POST, request.FILES)
        if request.method =='POST' and  catForm.is_valid():
            catForm.save()
            messages.success(request, "La categoria ha sido registrada correctamente")
            return redirect(('categoryList'))
        return render(request, "registration/create_cat.html", {"form":catForm})
    

class FormularioProjectView(HttpRequest):
    @is_employee
    def index(request):
        projectForm = ProjectForm()
        return render(request, "nucleo/users/create_proj.html", {"form":projectForm})
    @is_employee
    def procesar_formulario(request):
        now = datetime.date.today()
        projectForm = ProjectForm(request.POST)
        project = projectForm.save(commit=False)
        project.idEmployee = request.user
        if project.endDate < project.startDate:
            messages.error(request, "La fecha de finalización del proyecto debe ser mayor a la de inicio")
            return redirect(('createProject'))
        if project.startDate <= now:
            messages.error(request, "La fecha de comienzo del proyecto debe ser posterior a hoy")
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

@method_decorator(is_admin,name="dispatch")
class EmployeeList(ListView):
    model=User
    template_name="nucleo/admin/employee_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(role_user='Empleado')
        return context
    
@method_decorator(is_admin,name="dispatch")   
class UserList(ListView):
    model=User
    template_name="nucleo/admin/user_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(role_user='Cliente')
        return context
    
@method_decorator(is_admin,name="dispatch")
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
        
@method_decorator(is_admin,name="dispatch")
class UserUpdateView(UpdateView):
        model= User
        form_class = UserForm
        template_name='nucleo/admin/update.html'
        
        def dispatch(self, request, *args, **kwargs):
            self.object = self.get_object()
            return super().dispatch(request, *args, **kwargs)
        
        def get_success_url(self):
            return '/userList/'
        
@method_decorator(is_admin,name="dispatch")         
class EmployeeUpdateView(UpdateView):
        model= User
        form_class = EmployeeForm
        template_name='nucleo/admin/update.html'
        
        def dispatch(self, request, *args, **kwargs):
            self.object = self.get_object()
            return super().dispatch(request, *args, **kwargs)
        
        def get_success_url(self):
            return '/employeeList/'
        
@method_decorator(is_employee,name="dispatch")
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
    
@method_decorator(is_employee,name="dispatch")  
class ProjectUpdateView(UpdateView):
        model= Project
        form_class = ProjectForm
        template_name='nucleo/users/updateproject.html'
        
        def dispatch(self, request, *args, **kwargs):
            self.object = self.get_object()
            return super().dispatch(request, *args, **kwargs)
    
        def get_success_url(self):
            return '/listProjects/'

@method_decorator(is_not_admin,name="dispatch") 
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

@is_client
@is_active
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
        
@is_client
@is_active
def agregarParticipa(request,pk):
    if request.method=="POST":
        idProjecto=Project.objects.get(pk=pk)
        cliente=request.user.id
        now = datetime.datetime.now()
        participate = Participate.objects.create(idCliente_id=cliente, idProject = idProjecto, registrationDate = now,rol="null")
        participate.save()
        messages.success(request,"Has sido inscrito satisfactoriamente")
        return redirect(("listProjects"))

@method_decorator(is_admin,name="dispatch")   
class ActiveUserView(UpdateView):
    def post(self, *args,**kwargs):
        if self.request.method =="POST":
            id = self.request.POST.get('idClient')
            user = User.objects.get(pk=id)
            if(user.active == False):
                user.active = True
                user.save()
                users = User.objects.filter(role_user="Cliente")
                return render(self.request,"nucleo/admin/user_list.html",{'users':users})
            else:
                user.active = False
                user.save()
                users = User.objects.filter(role_user="Cliente")
                return render(self.request,"nucleo/admin/user_list.html",{'users':users})
        
@method_decorator(is_not_admin,name="dispatch")
@method_decorator(is_active,name="dispatch")
class ProjectListView(ListView):
    model=Project
    template_name="nucleo/users/project_list.html"
    
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
    
@method_decorator(is_employee,name="dispatch")
class EmployeeProjectView(ListView):
    model = Project
    template_name="nucleo/users/employee_project.html"
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(idEmployee_id=self.request.user.pk)
        return context
    
@method_decorator(is_employee,name="dispatch")
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
    
@method_decorator(is_employee,name="dispatch")
class SearchClientView(ListView):
    model = Participate
    template_name="nucleo/users/search_client.html"
    
    def get_context_data(self, **kwargs):
        if self.request.method == "GET":
            context = super().get_context_data(**kwargs)
            role = self.request.GET.get('rol')
            context['participates'] = Participate.objects.filter(rol = role)
            return context

@method_decorator(is_employee,name="dispatch")
class ListProjctView(ListView):
    model = Project
    template_name="nucleo/users/this_project.html"
    
    def get_context_data(self, **kwargs):
        if self.request.method == "GET":
            context = super().get_context_data(**kwargs)
            idProject = self.request.GET.get('idProject')
            context['projects'] = Project.objects.filter(id = idProject)
            return context

@method_decorator(is_client,name="dispatch")
class infoPDFView(ListView):
    model = Participate
    template_name="nucleo/users/my_info.html"
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        idClient = self.request.user.id
        isParticipate = Participate.objects.filter(idCliente_id = idClient).exists()
        if( isParticipate == True ):
            context['user'] = User.objects.get(id=idClient)
            context['participates'] = Participate.objects.filter(idCliente_id = idClient)
            return context
        else:
            context['participates'] = User.objects.filter(id = idClient)
            return context
        
@method_decorator(is_client,name="dispatch")
class infoPDFFilterView(ListView):
    model = Participate
    template_name="nucleo/users/my_info.html"
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        idClient = self.request.user.id
        stDate = self.request.GET.get('stDate')
        ndDate = self.request.GET.get('ndDate')
        projects = Project.objects.filter(endDate__gt = stDate, endDate__lt = ndDate).exists()
        if( projects == True ):
            context['user'] = User.objects.get(id=idClient)
            projectsList = Project.objects.filter(endDate__gt = stDate, endDate__lt = ndDate)
            context['participates'] = Participate.objects.filter(idCliente_id = idClient).filter(idProject_id__in = projectsList)
            context['stDate'] = stDate
            context['ndDate'] = ndDate
            return context
        else:
            context['user'] = User.objects.get(id=idClient)
            message = "No existe ningun proyecto en las fechas indicadas"
            context['messages'] = message
            return context
         
@method_decorator(is_admin,name="dispatch")
class CategoryListView(ListView):
    model=Category
    template_name="nucleo/admin/category_list.html"

@method_decorator(is_admin,name="dispatch")
class editCategory(UpdateView):
    model= Category
    form_edit = EditCategoryForm
    template_name='nucleo/admin/category_form.html'
    fields = ['name','image']
    def get_success_url(self):
        return '/categoryList/'

@method_decorator(is_admin,name="dispatch")    
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

@method_decorator(is_client,name="dispatch")
@method_decorator(is_active,name="dispatch")
class ProjectNextWeekListView(ListView):
    model=Project
    template_name="nucleo/ListNextWeek_list.html"
      
    @staticmethod
    def get_next_week():
        now = datetime.datetime.now()
        weekDayNow = now.weekday()
        diasRestantes = 6 - weekDayNow
        monday = now + datetime.timedelta(diasRestantes)
        sunday = monday + datetime.timedelta(6)
        return Project.objects.filter(startDate__gt=monday, startDate__lt=sunday)
    
    def get_context_data(self, **kwargs):
        now = datetime.datetime.now()
        context = super().get_context_data(**kwargs)
        context['projectsDates'] = self.get_next_week()
        return context
    
class generatePDFView(View):
    
    width, height = A4
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_LEFT
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
  
    def cabecera(self,pdf):
        logo = settings.BASE_DIR.as_posix()+'/static/assets/img/logo.png'
        pdf.drawImage(logo,40,750,120,90,preserveAspectRatio=True)
        
    
    def tarjeta(self,pdf,y):
        for cliente in User.objects.filter(id = self.request.user.id):
            pdf.setFont("Courier-Bold",16)
            pdf.drawString(70, 700, u"DATOS DEL CLIENTE")
            pdf.setFont("Courier-Bold",12)
            pdf.drawString(70, 670, u"Nombre: ")
            pdf.setFont("Courier",12)
            pdf.drawString(130, 670, u""+str(cliente.name))
            pdf.setFont("Courier-Bold",12)
            pdf.drawString(70, 650, u"Apellidos: ")
            pdf.setFont("Courier",12)
            pdf.drawString(150, 650, u""+str(cliente.surname))
            pdf.setFont("Courier-Bold",12)
            pdf.drawString(70, 630, u"Dni: ")
            pdf.setFont("Courier",12)
            pdf.drawString(100, 630, u""+str(cliente.dni))
            pdf.setFont("Courier-Bold",12)
            pdf.drawString(70, 610, u"Dirección: ")
            pdf.setFont("Courier",12)
            pdf.drawString(150, 610, u""+str(cliente.address))
            pdf.setFont("Courier-Bold",12)
            pdf.drawString(70, 590, u"Fecha Nacimiento: ")
            pdf.setFont("Courier",12)
            pdf.drawString(200, 590, u""+str(cliente.birthDate))
            
    def coord(x, y, unit=1):
        x, y = x * unit, height -  y * unit
        return x, y   
        
    def tabla(self,pdf,y):
        


        stDate = self.request.GET.get('stDate')
        ndDate = self.request.GET.get('ndDate')
        if str(stDate) == "":
            



              #Creamos una tupla de encabezados para neustra tabla
            encabezados = ('Titulo', 'Descripcion', 'Nivel', 'Inicio','Fin','Informe final')
            #Creamos una lista de tuplas que van a contener a las personas
            detalles = [(cliente.idProject.title, cliente.idProject.description, cliente.idProject.level, cliente.idProject.startDate , cliente.idProject.endDate, cliente.idProject.endReport) for cliente in Participate.objects.filter(idCliente = self.request.user.id)]
            #Establecemos el tamaño de cada una de las columnas de la tabla
            detalle_orden = Table([encabezados] + detalles, rowHeights=50,colWidths=[3 * cm, 5 * cm, 5 * cm, 5 * cm, 5 * cm, 5 * cm])
            #Aplicamos estilos a las celdas de la tabla
            detalle_orden.setStyle(TableStyle([
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(0,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black), 
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
            ))
            #Establecemos el tamaño de la hoja que ocupará la tabla 
            detalle_orden.wrapOn(pdf, 800, 600)
            #Definimos la coordenada donde se dibujará la tabla
            detalle_orden.drawOn(pdf, 60,y)
            for cliente in Participate.objects.filter(idCliente = self.request.user.id):
                pdf.drawString(70, y-20, u"Descripción: ")
                pdf.setFont("Courier",8)
                pdf.drawString(200, y-20, u""+str(cliente.idProject.description))
            

    def get(self,request,*args,**kwargs):
        response = HttpResponse(content_type='application/pdf')
        buffer=BytesIO()
        pdf = canvas.Canvas(buffer,pagesize=A4,)
        self.cabecera(pdf)
        y = 600
        self.tarjeta(pdf,y)
        y = 400
        self.tabla(pdf,y)
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
        
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     stDate = self.request.GET.get('stDate')
    #     ndDate = self.request.GET.get('ndDate')

    #     return context