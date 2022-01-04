from django.db import models
from django.db.models.deletion import DO_NOTHING
import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    id=models.AutoField(primary_key=True)
    dni=models.CharField(max_length=9,verbose_name="DNI")
    name=models.CharField(max_length=50,verbose_name="Name")
    surname=models.CharField(max_length=50,verbose_name="Surname")
    address=models.CharField(max_length=50,verbose_name="Address")
    birthDate=models.DateField(verbose_name="Birthday")
    registerDate=models.DateTimeField(verbose_name="Date of register", auto_now=True)
    active=models.BooleanField(verbose_name="Active",null=True)
    role_user = models.CharField(max_length=50,verbose_name="role",default='client')
    
    
    def _str_(self):
        return self.dni+" "+self.name+" "+self.surname+" "+self.address+" "+self.birthDate+" "+self.active+" "+self.role_user

# class User(models.Model):
#     id=models.AutoField(primary_key=True)
#     username=models.CharField(max_length=50,verbose_name="UserName")
#     password=models.CharField(max_length=18,verbose_name="Password")
    
#     def __str__(self):
#         return self.username
    
# class Client(models.Model):
#     id=models.AutoField(primary_key=True)
#     dni=models.CharField(max_length=9,verbose_name="DNI")
#     name=models.CharField(max_length=50,verbose_name="Name")
#     surname=models.CharField(max_length=50,verbose_name="Surname")
#     address=models.CharField(max_length=50,verbose_name="Address")
#     birthDate=models.DateField(verbose_name="Birthday")
#     registerDate=models.DateTimeField(verbose_name="Date of register", auto_now=True )
#     active=models.BooleanField(verbose_name="Active",null=True)
#     idUser=models.ForeignKey(User,verbose_name="IdUser",on_delete=models.CASCADE)
    
#     # def __str__(self):
#     #         return self.dni+" "+self.name+" "+self.surname+" "+self.address+" "+self.birthDate.strftime('%m/%d/%Y')+" "+self.active+" "+self.idUser
    
# class Employees(models.Model):
#     id=models.AutoField(primary_key=True)
#     dni=models.CharField(max_length=9,verbose_name="DNI")
#     name=models.CharField(max_length=50,verbose_name="Name")
#     surname=models.CharField(max_length=50,verbose_name="Surname")
#     address=models.CharField(max_length=50,verbose_name="Address")
#     biography=models.TextField(max_length=260,verbose_name="Biography", )
#     idUser=models.ForeignKey(User,verbose_name="IdUser",on_delete=models.CASCADE)
    
class Category(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,verbose_name="Name")
    image=models.ImageField(verbose_name="Image")
     
class Project(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=50,verbose_name="Title")
    description=models.TextField(max_length=260,verbose_name="Description")
    level:models.IntegerField(max_length=8,verbose_name="Level")
    startDate:models.DateField(verbose_name="Start Day")
    endDate:models.DateField(verbose_name="End Day")
    endReport:models.TextField(max_length=260,verbose_name="End Report")
    idEmployee=models.ForeignKey(User,verbose_name="id",on_delete=models.CASCADE)
    idCategory=models.ForeignKey(Category,verbose_name="id",on_delete=models.CASCADE)
    
    
class Participate(models.Model):
    id=models.AutoField(primary_key=True)
    idCliente=models.ForeignKey(User,verbose_name="id",on_delete=models.CASCADE)
    idProject=models.ForeignKey(Project,verbose_name="id",on_delete=models.CASCADE)
    registrationDate=models.DateField(verbose_name="Registration Date")
    rol=models.TextField(max_length=260,verbose_name="Rol")