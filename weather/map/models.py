from django.db import models
from django.utils.translation import gettext as _
# Create your models here.
class Search(models.Model):
    address = models.CharField(max_length=200,  null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Countries(models.Model):
    name = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class City(models.Model):
    city = models.CharField(max_length=200, null=True)
    country = models.ForeignKey(Countries,on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city

