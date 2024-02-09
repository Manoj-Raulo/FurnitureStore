from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    pname=models.CharField(max_length=500,null=True)
    category=models.CharField(max_length=200,null=True)
    preference=models.CharField(max_length=200,null=True)
    size=models.CharField(max_length=200,null=True)
    material=models.CharField(max_length=300,null=True)
    finishtype=models.CharField(max_length=300,null=True)
    dimension=models.CharField(max_length=300,null=True)
    colour=models.CharField(max_length=200,null=True)
    brand=models.CharField(max_length=200,null=True)
    features=models.CharField(max_length=500,null=True)
    desc=models.CharField(max_length=1000,null=True)
    price=models.FloatField(null=True)
    time=models.TimeField(auto_now=True,null=True)
    date=models.DateField(auto_now=True,null=True)
    weight=models.CharField(max_length=100,null=True)
    stock=models.IntegerField(null=True)
    img1=models.ImageField(upload_to='media',null=True)
    img2=models.ImageField(upload_to='media',null=True)
    img3=models.ImageField(upload_to='media',null=True)
    img4=models.ImageField(upload_to='media',null=True)
    img5=models.ImageField(upload_to='media',null=True)

    

    def __str__(self):
        return self.pname

class Offers(models.Model):
    offer1=models.ImageField(upload_to='offer',null=True)
    offer2=models.ImageField(upload_to='offer',null=True)
    offer3=models.ImageField(upload_to='offer',null=True)
    offer4=models.ImageField(upload_to='offer',null=True)
    offer5=models.ImageField(upload_to='offer',null=True)

class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

class Save(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

class RegisterationRequest(models.Model):
    bname=models.CharField(max_length=100,null=True)
    email = models.EmailField()
    contact=models.BigIntegerField(null=True)
    shopaddress=models.CharField(max_length=300,null=True)
    branddesc=models.CharField(max_length=500,null=True)


    


    
    
