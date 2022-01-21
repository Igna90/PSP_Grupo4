from django.db import models
from django.db.models.deletion import DO_NOTHING
import datetime
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.

class User(AbstractUser):
    class UserType(models.TextChoices):
        Client = 'Cliente', _('Cliente')
        Employee = 'Empleado', _('Empleado')
        Admin = 'Administrador', _('Administrador')
        
    id=models.AutoField(primary_key=True)
    dni=models.CharField(max_length=9,verbose_name="DNI")
    name=models.CharField(max_length=50,verbose_name="Nombre")
    surname=models.CharField(max_length=50,verbose_name="Apellido")
    address=models.CharField(max_length=50,verbose_name="Dirección")
    birthDate=models.DateField(verbose_name="Fecha de cumpleaños")
    registerDate=models.DateTimeField(verbose_name="Fecha de registro", auto_now=True)
    active=models.BooleanField(verbose_name="Activo",null=True)
    role_user = models.CharField(max_length=50,verbose_name="role",choices=UserType.choices,default=UserType.Client)
    
    class Meta:
        verbose_name="Usuario"
        verbose_name_plural="Usuarios"
    
    def _str_(self):
        return self.dni+" "+self.name+" "+self.surname+""+self.birthDate+" "+self.address+"  "+self.active+" "+self.role_user
    
    # def save(self,*args,**kwargs):
    #     if self.pk is None:
    #         self.set_password(self.password)
    #     else:
    #         user = User.objects.get(pk=self.pk)
    #         if user.password == self.password:
    #             self.set_password(self.password)
    #     super().save(*args,**kwargs)

    
class Category(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,verbose_name="Categoria")
    image=models.ImageField(verbose_name="Imagen")
    
    class Meta:
        verbose_name="Categoria"
        verbose_name_plural="Categorias"
     
class Project(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=50,verbose_name="Titulo")
    description=models.TextField(max_length=260,verbose_name="Descripcion")
    level=models.IntegerField(verbose_name="Nivel")
    startDate=models.DateField(verbose_name="Fecha de comienzo")
    endDate=models.DateField(verbose_name="Fecha final")
    endReport=models.TextField(max_length=260,verbose_name="Informe final")
    idEmployee=models.ForeignKey(User,verbose_name="id",on_delete=models.CASCADE)
    idCategory=models.ForeignKey(Category,verbose_name="id",on_delete=models.CASCADE)
    
    class Meta:
        verbose_name="Proyecto"
        verbose_name_plural="Proyectos"
    
    def _str_(self):
        return self.title+" "+self.description+" "+self.startDate+" "+self.endDate+" "+self.endReport
    
class Participate(models.Model):
    id=models.AutoField(primary_key=True)
    # idCliente=models.ForeignKey(User,verbose_name="id",on_delete=models.CASCADE)
    idProject=models.ForeignKey(Project,verbose_name="id",on_delete=models.CASCADE)
    registrationDate=models.DateField(verbose_name="Fecha de registro")
    rol=models.TextField(max_length=260,verbose_name="Rol")
    class Meta:
        verbose_name="Participa"
        verbose_name_plural="Participan"

