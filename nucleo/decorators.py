from django.contrib import messages
from django.http import HttpResponseRedirect

def is_employee(fun):
    def client_call(request,*args,**kwargs):
        if request.user.role_user == 'Cliente' or request.user.role_user =='Administrador':
            messages.success(request, "Acceso no permitido")
            return HttpResponseRedirect('/')
        return fun(request,*args,**kwargs)
    return client_call

def is_client(fun):
    def employee_call(request,*args,**kwargs):
        if request.user.role_user == 'Empleado' or request.user.role_user =='Administrador':
            messages.success(request, "Acceso no permitido")
            return HttpResponseRedirect('/')
        return fun(request,*args,**kwargs)
    return employee_call

def is_admin(fun):
    def admin_call(request,*args,**kwargs):
        if request.user.role_user == 'Empleado' or request.user.role_user =='Cliente':
            messages.success(request, "Acceso no permitido")
            return HttpResponseRedirect('/')
        return fun(request,*args,**kwargs)
    return admin_call

def is_not_admin(fun):
    def admin_call(request,*args,**kwargs):
        if request.user.role_user == 'Administrador':
            messages.success(request, "Acceso no permitido")
            return HttpResponseRedirect('/')
        return fun(request,*args,**kwargs)
    return admin_call

def is_active(fun):
    def active_or_no(request,*args,**kwargs):
        if request.user.active == False:
            messages.success(request, "Lo sentimos, pero su usuario aún no está activado")
            return HttpResponseRedirect('/')
        return fun(request,*args,**kwargs)
    return active_or_no
            