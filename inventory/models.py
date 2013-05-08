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
    tokenvalue=models.IntegerField(default=0)

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

class OrderGroup(models.Model):
    id = models.AutoField(primary_key=True)

    def __unicode__(self):
        return str(self.id)


class Order(models.Model):
    group=models.ForeignKey(OrderGroup)
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
        self.fields['name'].widget.attrs = {'class':'labelish'}
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['name'].label = ''

class InventoryGroup(models.Model):
    id = models.AutoField(primary_key=True)

    def __unicode__(self):
        return str(self.id)

class Inventory(models.Model):
    group=models.ForeignKey(InventoryGroup)
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

class Token(models.Model):
    value=models.IntegerField(default=0)

class TokenBooth(models.Model):
    name=models.CharField(max_length=255)
    location_number=models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class TokenDelivery(models.Model):
    location=models.ForeignKey(TokenBooth)
    tokens=models.IntegerField(default=0)
    timestamp=models.DateTimeField(auto_now=True)
    fiscal_day=models.DateField(default=datetime.now)
    user=models.ForeignKey(User)


class TokenDeliveryForm(ModelForm):
    tokens=forms.IntegerField(initial=0, widget=Html5NumInput)
    class Meta:
        model=TokenDelivery
        fields=('tokens',)

class TokenCollection(models.Model):
    location=models.ForeignKey(Location)
    tokens=models.IntegerField(default=0)
    timestamp=models.DateTimeField(auto_now=True)
    fiscal_day=models.DateField(default=datetime.now)
    user=models.ForeignKey(User)

class TokenCollectionForm(ModelForm):
    tokens=forms.IntegerField(initial=0, widget=Html5NumInput)
    class Meta:
        model=TokenCollection
        fields=('tokens',)

class LocationTokenNote(models.Model):
    location=models.ForeignKey(Location)
    timestamp=models.DateTimeField(auto_now=True)
    content=models.TextField(max_length=50000)
    user=models.ForeignKey(User)

class LocationTokenNoteForm(ModelForm):
    class Meta:
        model=LocationTokenNote
        fields=('content',)

class BoothTokenNote(models.Model):
    location=models.ForeignKey(TokenBooth)
    timestamp=models.DateTimeField(auto_now=True)
    content=models.TextField(max_length=50000)
    user=models.ForeignKey(User)

class BoothTokenNoteForm(ModelForm):
    class Meta:
        model=BoothTokenNote
        fields=('content',)


