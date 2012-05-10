from django.db import models

class Locations(models.Model):
    name=models.CharField(max_length=255)
    location_id=models.CharField(max_length=255)
    organization=models.CharField(max_length=255)
    
class Beverages(models.Model):
    name=models.CharField(max_length=255)
    units_reported=models.IntegerField(max_length=10)
    fill_to_standard=models.IntegerField(max_length=10)
    order_when_below=models.IntegerField(max_length=10)
    
class Orders(models.Model):
    amount=models.IntegerField(max_length=20)
    timestamp=models.DateTimeField(auto_now=True)
    
class Inventory(models.Model):
    location=models.ForeignKey(Locations)
    beverage=models.ForeignKey(Beverages)
    notes=models.TextField(max_length=2550)
    timestamp=models.DateTimeField(auto_now=True)