from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Desigination(models.Model):
    desigination=models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return self.desigination

class Registration(models.Model):
    first_name=models.CharField(max_length=100,null=True)
    last_name=models.CharField(max_length=100,null=True)
    email=models.EmailField(max_length=100,null=True)
    username=models.CharField(max_length=100,null=True)
    password=models.CharField(max_length=100,null=True)
    desigination=models.ForeignKey(Desigination,on_delete=models.CASCADE)
    
    def __str__(self) :
        return self.username
    
    
class Vehicle_registeration(models.Model):
    vehicle_number=models.CharField(max_length=100,null=True)
    vehicle_type=models.CharField(max_length=100,null=True)
    vehicle_model=models.CharField(max_length=100,null=True)
    vehicle_description=models.CharField(max_length=100,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self) :
        return self.vehicle_model
    
        
    
    
    
 
    
