from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from inventory.models import Beverage, Location, Inventory, Note, Order, InventoryForm
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django import forms
from django.forms.models import formset_factory, modelformset_factory
import models
import datetime
#from django.db.models import Max

def showLastInventory(request, location_number):
    #change to get obj or 404
    try:
        location = Location.objects.get(location_number=location_number)
        
    except ObjectDoesNotExist:
        return HttpResponse('no location for that')
    
    #beverage = Beverage.objects.filter(location__location_number=location_number)
    #inventory = beverage.inventory_set.all()
    #beverage = Beverage.objects.filter(location__location_number=location_number)
    latest = Inventory.objects.filter(location=location).latest('timestamp')
    latest = latest.timestamp
    d = latest.date()
    h = latest.hour
    m = latest.minute
    s = latest.second - 1
    
    lt = datetime.time(h,m,s)
    latest = datetime.datetime.combine(d, lt)
    
    inventory = Inventory.objects.filter(location=location).filter(timestamp__gte=latest)

    
    return render_to_response('location.html',
        {'location':location, 'inventory':inventory},
        context_instance=RequestContext(request)
    )
    
def updateInventory(request, location_number):
    """
    TODO: set a max of three on the fields
    lay out as a table
    whatever else
    """
    
    InventoryFormSet=modelformset_factory(Beverage, form=InventoryForm)
    #location = Location.objects.get(location_number=location_number)
    qs=Beverage.objects.filter(location__location_number=location_number)
    formset=InventoryFormSet(queryset=qs)
    if request.method=='POST':
        formset=InventoryFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                beverage=form.save(commit=False)
                units_reported=form.cleaned_data['units_reported']
                Inventory(beverage=beverage, units_reported=units_reported).save()
    
    else:
        
        return render_to_response('updateInventory.html',
            {'formset': formset},
            context_instance=RequestContext(request)
        )
    
    #if request.method == 'POST':
    #    form = InventoryForm(request.POST)
    #    
    #else:
    #    location = Location.objects.get(location_number=location_number)
    #    inventory = Inventory.objects.filter(location=location)
    #    
    #    InventoryFormSet = inlineformset_factory(Beverage, Inventory)
    #    beverage = Beverage.objects.get(location=location)
    #    
    #    formset = InventoryFormSet(instance=beverage)
    #    
    #    return render_to_response('updateInventory.html',
    #        {'formset': formset},
    #        context_instance=RequestContext(request)
    #    )

def test(request, location_number):
    #location = Location.objects.get(location_number=location_number)
    bev=Beverage.objects.filter(location__location_number=location_number)
    
    return render_to_response('test.html',
        {'bev':bev},
        context_instance=RequestContext(request)
    )
    