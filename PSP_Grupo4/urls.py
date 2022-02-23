"""PSP_Grupo4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf.urls import include
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from nucleo import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('',views.index, name="index"),
    path('login/', views.login_view.loginUser, name='login'),
    path('editProfile/', login_required(views.profile), name='profile'),
    path('logout/', login_required(views.logout_request), name='logout'),
    
    #ROL_ADMIN
    path('userList/',login_required(views.UserList.as_view()), name='userList'),
    path('activeUser/', login_required(views.ActiveUserView.as_view()) , name='activeUser'),
    path('deleteClient/<int:pk>',login_required(views.UserDeleteView.as_view()), name='deleteUser'),
    path('updateUser/<int:pk>', login_required(views.UserUpdateView.as_view()) , name='updateUser'),
    path('updateEmployee/<int:pk>', login_required(views.EmployeeUpdateView.as_view()) , name='updateEmployee'),
    path('employeeList/', login_required(views.EmployeeList.as_view()), name='employeeList'),
    path('createEmployee/', login_required(views.FormularioEmployeeView.index), name='createEmployee'),
    path('guardarEmployee/', login_required(views.FormularioEmployeeView.procesar_formulario), name='guardarEmployee'),
    path('createClient/', views.FormularioClientView.index, name='createClient'),
    path('guardarClient/', views.FormularioClientView.procesar_formulario, name='guardarClient'),
    path('categoryList/', login_required(views.CategoryListView.as_view()), name='categoryList'),
    path('createCategoria/',login_required(views.FormCreateCategoryView.index), name='createCategoria'),
    path('guardarCategoria/', login_required(views.FormCreateCategoryView.procesar_formulario), name='guardarCategoria'),
    path('updateCategory/<int:pk>', login_required(views.editCategory.as_view()) , name='updateCategory'),
    path('deleteCategory/<int:pk>',login_required(views.CategoryDeleteView.as_view()), name='deleteCategory'),
    path('createEmployee/', login_required(views.FormularioEmployeeView.index), name='createEmployee'),
    path('guardarEmployee/', login_required(views.FormularioEmployeeView.procesar_formulario), name='guardarEmployee'),

    #ROL_EMPLEADOS + ROL_CLIENTE
    path('listProjects/', login_required(views.ProjectListView.as_view()), name='listProjects'),
    path('listParticipate/', login_required(views.ParticipateView.as_view()), name='listParticipate'),
    
    #ROL_EMPLEADOS
    path('deleteProjects/<int:pk>', login_required(views.ProjectDeleteView.as_view()), name='deleteProjects'),
    path('updateProject/<int:pk>', login_required(views.ProjectUpdateView.as_view()) , name='updateProject'),
    path('createProject/', login_required(views.FormularioProjectView.index), name='createProject'),
    path('guardarProject/', login_required(views.FormularioProjectView.procesar_formulario), name='guardarProject'),
    path('listEmployeeProjects/', login_required(views.EmployeeProjectView.as_view()), name='listEmployeeProjects'),
    path('clientProjectView/', login_required(views.ClientProjectView.as_view()), name='clientProjectView'),
    path('listEmployeeCurrentProjects/', login_required(views.EmployeeCurrentProjectView.as_view()), name='listEmployeeCurrentProjects'),
    path('endProjects/<int:pk>', login_required(views.EmployeeUpdateEndDate.as_view()), name='endProjects'),
    path('searchClient/', login_required(views.SearchClientView.as_view()), name='searchClient'),
    path('listThisProject/', login_required(views.ListProjctView.as_view()), name='listThisProject'),

    #ROL_CLIENTE
    path('projectParticipate/<int:pk>',login_required(views.project_participate), name='projectParticipate'),
    path('createdParticipate/<int:pk>',login_required(views.agregarParticipa), name='createdParticipate'),
    path('listProjectsNextWeek/', login_required(views.ProjectNextWeekListView.as_view()), name='listProjectsNextWeek'),
    #API
    path('api/users/',User_APIView.as_view()),
    path('api/participates/',Participate_APIView.as_view()),
    path('api/projects/',Project_APIView.as_view()),
    # path('api/employees/<int:pk>',Employees_APIView_Detail.as_view()),  
    path('api/token/',TestView.as_view()), 
    #PDF
    path('reporte_personas_pdf/',(ReportePersonasPDF.as_view()), name="reporte_personas_pdf"),
    path('infoPDF/', login_required(views.infoPDFView.as_view()), name='infoPDF'),
    path('infoPDFFilter/', login_required(views.infoPDFFilterView.as_view()), name='infoPDFFilter'),
    path('generatePDF/', login_required(views.generatePDFView.as_view()), name='generatePDF'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()