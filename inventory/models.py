from django.db import models
from datetime import datetime
from django.forms import ModelForm
from django import forms
from django.forms.widgets import TextInput, Input
from django.contrib.auth.models import User


class Html5NumInput(Input):
    input_type = 'number'

class Beverage(models.Model):
    name=models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Location(models.Model):
    name=models.CharField(max_length=255)
    beverages = models.ManyToManyField(Beverage, through='LocationStandard')
    location_number=models.CharField(max_length=255)
    organization=models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class LocationStandard(models.Model):
    beverage=models.ForeignKey(Beverage)
    location=models.ForeignKey(Location) #elim this or m2m
    start_units=models.IntegerField()
    fill_to_standard=models.IntegerField(max_length=10)
    order_when_below=models.IntegerField(max_length=10)

class Order(models.Model):
    location=models.ForeignKey(Location) #elim this or m2m
    beverage=models.ForeignKey(Beverage)
    units_ordered=models.IntegerField(max_length=10, default=0)
    order_delivered=models.NullBooleanField(null=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User)


class OrderForm(ModelForm):
    units_ordered=forms.IntegerField(initial=0, widget=Html5NumInput)
    class Meta:
        model=Beverage
        fields=('name', 'id')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['units_ordered'].label = ''
        self.fields['units_ordered'].widget.attrs = {'class':'number'}
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['name'].label = ''

class Inventory(models.Model):
    location=models.ForeignKey(Location) #elim this or m2m
    beverage=models.ForeignKey(Beverage)
    units_reported=models.IntegerField(max_length=10, default=0)
    timestamp=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User)

class InventoryForm(ModelForm):
    units_reported=forms.IntegerField(required=True, initial=0, widget=Html5NumInput)
    class Meta:
        model=Beverage
        fields=('name', 'id')

    def __init__(self, *args, **kwargs):
        super(InventoryForm, self).__init__(*args, **kwargs)
        self.fields['units_reported'].label = ''
        self.fields['units_reported'].widget.attrs = {'class':'number'}
        self.fields['name'].widget.attrs = {'class':'labelish'}
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['name'].label = ''

class Note(models.Model):
    location=models.ForeignKey(Location)
    timestamp=models.DateTimeField(auto_now=True)
    content=models.TextField(max_length=50000)
    user=models.ForeignKey(User)

class NoteForm(ModelForm):
    class Meta:
        model=Note
        fields=('content',)
"""
class DailyTotals(models.Model):
    date=models.DateTimeField()
    beverage=models.CharField(max_length=255)
    daily_total=models.IntegerField()
    grand_total=models.IntegerField()
"""
