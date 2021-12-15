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
    biography=models.TextField(verbose_name="Biography", )
    idUser=models.ForeignKey(User,verbose_name="IdUser",on_delete=models.CASCADE)