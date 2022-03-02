from pyexpat import model
from django.db import models

# Create your models here.
class userdetails(models.Model):
    hospitalName = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    doctorPassword = models.CharField(max_length=10)
    attendantPassword = models.CharField(max_length=10)
    medicalShoppassword = models.CharField(max_length=10)
    contactNumber = models.CharField(max_length=10)

    def __str__(self):
        return self.hospitalName

class Profile(models.Model):
    user = models.OneToOneField(userdetails,on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    role = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.role