from django.db import models

from authn.models import userdetails



class patientDetails(models.Model):
    userdet = models.ForeignKey(userdetails,on_delete=models.CASCADE)
    patientName = models.CharField(max_length=30)
    age = models.IntegerField()
    gender = models.CharField(max_length=7,blank=True,null=True)
    contactNumber = models.IntegerField()
    bloodGroup = models.CharField(max_length=5, blank=True,null=True)
    date = models.CharField(max_length=11)
    generalReason = models.CharField(max_length=20, blank=True,null=True)
    status = models.CharField(max_length=15,blank=True, null=True)
    problem = models.CharField(max_length=200,blank=True, null=True)
    tabletsDetails = models.CharField(max_length=200,blank=True, null=True)
    tabletsStatus = models.CharField(max_length=15,blank=True, null=True)
    
    def __str__(self):
        return self.patientName

class notAvailableTablets(models.Model):
    patientnum= models.ForeignKey(patientDetails,on_delete=models.CASCADE,blank=True, null=True)
    tabletsname = models.CharField(max_length=70,blank=True, null=True)
    hospitalId = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.tabletsname



""" class bill(models.Model):
    BillNum= models.IntegerField()
    user = models.ForeignKey(userdetails,on_delete=models.CASCADE,default='')

    def __str__(self):
        return str(self.BillNum) """