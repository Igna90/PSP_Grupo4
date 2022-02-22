import datetime

from msilib.schema import ListView


from django.utils.decorators import method_decorator

from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.views import View
from nucleo.decorators import is_active, is_admin, is_client, is_current_employee, is_employee, is_not_admin
from nucleo.models import Category, Participate, Project, User
from registration.forms import EditCategoryForm, EmployeeForm, UserForm, UserUpdateForm,CategoryForm
from registration.forms import EmployeeForm, ProjectForm, UserForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import DeleteView,UpdateView, ListView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from nucleo.serializers import ParticipateSerializers, ProjectsSerializers, UserSerializers

from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View
from reportlab.platypus import Table,TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors


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
    
@method_decorator(is_employee,name="dispatch")
class EmployeeCurrentProjectView(ListView):
    model = Project
    template_name="nucleo/users/employee_current_projects.html"
            
    def get_context_data(self, **kwargs):
        now = datetime.datetime.now()
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(idEmployee_id=self.request.user.pk,endDate__gt=now)
        return context
    
@method_decorator(is_employee,name="dispatch")
@method_decorator(is_current_employee,name="dispatch")           
class EmployeeUpdateEndDate(UpdateView):
        model= Project
        template_name='nucleo/users/updateEndReport.html'
        fields = ['endReport']
   
        def post(self, request, **kwargs):
            if self.request.method == "POST":
                projectId = self.request.POST.get('idProject')
                now = datetime.datetime.now()
                Project.objects.filter(id = projectId).update(endDate = now)
                
            return super(EmployeeUpdateEndDate, self).post(request, **kwargs)
        
        def dispatch(self, request, *args, **kwargs):
            self.object = self.get_object()
            return super().dispatch(request, *args, **kwargs)
        
        
        def get_success_url(self):
            return '/listEmployeeCurrentProjects/'


# Vistas para la api

class User_APIView(APIView):
    # permission_classes=[IsAuthenticated]
    
    def get(self,request,format=None,*args,**kwargs):
        user = User.objects.filter(role_user='Cliente')
        serializer = UserSerializers(user,many=True)
        return Response(serializer.data)
    
    # def post(self, request, format=None):
    #     serializer = UserSerializers(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Participate_APIView(APIView):
    # permission_classes=[IsAuthenticated]
    
    def get(self,request,format=None,*args,**kwargs):
        participate = Participate.objects.all()
        serializer = ParticipateSerializers(participate,many=True)
        return Response(serializer.data)

class Project_APIView(APIView):
    # permission_classes=[IsAuthenticated]
    
    def get(self,request,format=None,*args,**kwargs):
        proj = Project.objects.all()
        serializer = ProjectsSerializers(proj,many=True)
        return Response(serializer.data)
    
    
class TestView(APIView):
    
    def get(self,request, format=None):
        return Response({'detail':"GET Response"})
    
    def post(self,request,format=None):
        try:
            data=request.data
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status= status.HTTP_400_BAD_REQUEST
            )
        if "user" not in data or "password" not in data:
            return Response(
                'Wrong credentials',
                status = status.HTTP_401_UNAUTHORIZED
            )
            
        user = User.objects.get(username=data["user"])
        if not user:
            return Response(
                'No default user,please create one',
                status=status.HTTP_404_NOT_FOUND
            )
            
        token = Token.objects.get_or_create(user=user)
        return Response({'details':'POST answer','token':token[0].key})
    
#pruebas pdf

class ReportePersonasPDF(View):  
    
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT+'assets/img/section-title-bg.png'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)
        pdf.setFont("Helvetica",16)
        pdf.drawString(230,790, u"Cliente")
        pdf.setFont("Helvetica",14)
        pdf.drawString(200, 770, u"Listado de proyectos")  
        
    def tabla(self,pdf,y):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = [('DNI', 'Nombre', 'Apellidos', 'fechaNacimiento')]
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [(cliente.dni, cliente.name, cliente.surname, cliente.birthDate, cliente.address) for cliente in User.objects.filter(role_user='Cliente')]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table(encabezados + detalles, colWidths=[2 * cm, 5 * cm, 5 * cm, 5 * cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black), 
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 2),
            ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla 
        detalle_orden.wrapOn(pdf, 800, 600)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 60,y)
            
        
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)
        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        y = 600
        self.tabla(pdf, y)
        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    