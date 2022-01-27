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
    path('userList/',login_required(views.UserList), name='userList'),
    path('login/', views.login_view.loginUser, name='login'),
    path('createClient/', views.FormularioClientView.index, name='createClient'),
    path('guardarClient/', views.FormularioClientView.procesar_formulario, name='guardarClient'),
    path('editProfile/', login_required(views.profile), name='profile'),
    path('logout/', login_required(views.logout_request), name='logout'),
    path('employeeList/', login_required(views.EmployeeList), name='employeeList'),
    path('deleteClient/<int:pk>',login_required(views.UserDeleteView.as_view()), name='deleteUser'),
    path('updateUser/<int:pk>', login_required(views.UserUpdateView.as_view()) , name='updateUser'),
    path('activeUser/<int:pk>', login_required(views.ActiveUser) , name='activeUser'),
    path('deactiveUser/<int:pk>', login_required(views.DeactiveUser) , name='deactiveUser'),
    path('createEmployee/', login_required(views.FormularioEmployeeView.index), name='createEmployee'),
    path('guardarEmployee/', login_required(views.FormularioEmployeeView.procesar_formulario), name='guardarEmployee'),
    path('listProjects/', login_required(views.ProjectListView.as_view()), name='listProjects'),
    path('deleteProjects/<int:pk>', login_required(views.ProjectDeleteView.as_view()), name='deleteProjects'),
    path('updateProject/<int:pk>', login_required(views.ProjectUpdateView.as_view()) , name='updateProject'),
    path('createProject/', login_required(views.FormularioProjectView.index), name='createProject'),
    path('guardarProject/', login_required(views.FormularioProjectView.procesar_formulario), name='guardarProject'),
    path('createEmployee/', views.FormularioEmployeeView.index, name='createEmployee'),
    path('guardarEmployee/', views.FormularioEmployeeView.procesar_formulario, name='guardarEmployee'),
    path('listtProjects/', login_required(views.ProjectListtView.as_view()), name='listtProjects'),
    path('<int:pk>', login_required(views.ProjectDetailView.as_view()), name='detailProjects'),
    path('categoryList/', views.CategoryListView.as_view(), name='categoryList'),
    path('createCategoria/', views.FormCreateCategoryView.index, name='createCategoria'),
    path('guardarCategoria/', views.FormCreateCategoryView.procesar_formulario, name='guardarCategoria'),
    path('updateCategory/<int:pk>', login_required(views.editCategory.as_view()) , name='updateCategory'),
    path('deleteCategory/<int:pk>',login_required(views.CategoryDeleteView.as_view()), name='deleteCategory'),
    # path('guardarEmployee/', views.FormularioEmployeeView.procesar_formulario, name='guardarEmployee'),
    path('listParticipate/', views.ParticipateView.as_view(), name='listParticipate'),
    # path('<int:pk>', views.ProjectDetailView.as_view(), name='detailProjects'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()