from django.db import models
from datetime import datetime
from django.forms import ModelForm
from django import forms


class Location(models.Model):
    name=models.CharField(max_length=255)
    location_number=models.CharField(max_length=255)
    organization=models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name
    
class Beverage(models.Model):
    name=models.CharField(max_length=255)
    location=models.ForeignKey(Location)
    fill_to_standard=models.IntegerField(max_length=10)
    order_when_below=models.IntegerField(max_length=10)
    
    def __unicode__(self):
        return self.name
    
class Order(models.Model):
    beverage=models.ForeignKey(Beverage)
    units_ordered=models.IntegerField(max_length=10)
    timestamp=models.DateTimeField(auto_now=True)
    
class Inventory(models.Model):
    location=models.ForeignKey(Location)
    beverage=models.ForeignKey(Beverage)
    units_reported=models.IntegerField(max_length=10)
    timestamp=models.DateTimeField(auto_now=True)
    
class InventoryForm(ModelForm):
    units_reported=forms.IntegerField()
    class Meta:
        model=Beverage
        fields=('name', 'id')

class Note(models.Model):
    location=models.ForeignKey(Location)
    timestamp=models.DateTimeField(auto_now=True)
    content=models.TextField()
    
