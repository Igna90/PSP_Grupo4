from django.db import models
from django.db.models.deletion import DO_NOTHING

# Create your models here.


class User(models.Model):
    # id, username, password
    userName=models.CharField(max_length=50,verbose_name="Name")
    password=models.CharField(max_length=18,verbose_name="Password")
    
    def __str__(self):
        return self.userName
    
class Client(models.Model):
    dni=models.IntegerField(max_length=8,verbose_name="DNI")
    name=models.CharField(max_length=50,verbose_name="Name")
    surname=models.CharField(max_length=50,verbose_name="Surname")
    address=models.CharField(max_length=50,verbose_name="Address")
    birthDate=models.DateField(verbose_name="Birthday")
    registerDate=models.DateField(verbose_name="Date of register")
    active=models.BooleanField(verbose_name="Active")
    idUser=models.ForeignKey(User,verbose_name="IdUser",on_delete=models.CASCADE)
    
class Employees(models.Model):
    dni=models.IntegerField(max_length=8,verbose_name="DNI")
    name=models.CharField(max_length=50,verbose_name="Name")
    surname=models.CharField(max_length=50,verbose_name="Surname")
    address=models.CharField(max_length=50,verbose_name="Address")
    biography=models.TextField(max_length=260,verbose_name="Biography", )
    idUser=models.ForeignKey(User,verbose_name="IdUser",on_delete=models.CASCADE)
    
class Category(models.Model):
     name=models.CharField(max_length=50,verbose_name="Name")
     image=models.ImageField(verbose_name="Image")
class Project(models.Model):
    title=models.CharField(max_length=50,verbose_name="Title")
    description=models.TextField(max_length=260,verbose_name="Description")
    level:models.IntegerField(max_length=8,verbose_name="Level")
    startDate:models.DateField(verbose_name="Start Day")
    endDate:models.DateField(verbose_name="End Day")
    endReport:models.TextField(max_length=260,verbose_name="End Report")
    idEmployee=models.ForeignKey(Employees,verbose_name="IdEmployee",on_delete=models.CASCADE)
    idCategory=models.ForeignKey(Category,verbose_name="IdCategory",on_delete=models.CASCADE)
    
    
class Participate(models.Model):
    idCliente=models.ForeignKey(Client,verbose_name="IdClient",on_delete=models.CASCADE)
    idProject=models.ForeignKey(Project,verbose_name="IdProject",on_delete=models.CASCADE)
    registrationDate=models.DateField(verbose_name="Registration Date")
    rol=models.TextField(max_length=260,verbose_name="Rol")