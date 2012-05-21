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
    location=models.ForeignKey(Location) #elim this or m2m
    fill_to_standard=models.IntegerField(max_length=10)
    order_when_below=models.IntegerField(max_length=10)
    
    def __unicode__(self):
        return self.name
    
class Order(models.Model):
    beverage=models.ForeignKey(Beverage)
    location=models.ForeignKey(Location)
    units_ordered=models.IntegerField(max_length=10, default=0)
    order_delivered=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now=True)
    
class OrderForm(ModelForm):
    units_ordered=forms.IntegerField(initial=0)
    class Meta:
        model=Beverage
        fields=('name', 'id')
    
class StartingInventory(models.Model):
    location=models.ForeignKey(Location)
    beverage=models.ForeignKey(Beverage)
    units=models.IntegerField()

class Inventory(models.Model):
    location=models.ForeignKey(Location)
    beverage=models.ForeignKey(Beverage)
    units_reported=models.IntegerField(max_length=10, default=0)
    timestamp=models.DateTimeField(auto_now=True)
    
class InventoryForm(ModelForm):
    units_reported=forms.IntegerField(required=True, initial=0)
    class Meta:
        model=Beverage
        fields=('name', 'id')

class Note(models.Model):
    location=models.ForeignKey(Location)
    timestamp=models.DateTimeField(auto_now=True)
    content=models.TextField(max_length=50000)
    
class NoteForm(ModelForm):
    class Meta:
        model=Note
        fields=('content',)
    
class DailyTotals(models.Model):
    date=models.DateTimeField()
    beverage=models.CharField(max_length=255)
    daily_total=models.IntegerField()
    grand_total=models.IntegerField()
    