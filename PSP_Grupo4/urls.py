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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('',views.index, name="index"),
    path('login/', views.login_view.loginUser, name='login'),
    path('createClient/', views.FormularioClientView.index, name='createClient'),
    path('guardarClient/', views.FormularioClientView.procesar_formulario, name='guardarClient'),
    path('editProfile/', login_required(views.profile), name='profile'),
    path('logout/', views.logout_request, name='logout'),
    path('employeeList/', views.EmployeeList, name='employeeList'),
]


urlpatterns += staticfiles_urlpatterns()