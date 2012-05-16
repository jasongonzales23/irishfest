from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from inventory.models import Beverage, Location, Inventory, Note, Order, InventoryForm, OrderForm
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
    InventoryFormSet=modelformset_factory(Beverage, form=InventoryForm, max_num=0)
    location=Location.objects.get(location_number=location_number)
    qs=Beverage.objects.filter(location__location_number=location_number)
    formset=InventoryFormSet(queryset=qs)
    if request.method=='POST':
        formset=InventoryFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                beverage=form.save(commit=False)
                units_reported=form.cleaned_data['units_reported']
                Inventory(location=location, beverage=beverage, units_reported=units_reported).save()
                
        return HttpResponseRedirect('/location/' + location_number )
    else:
        
        return render_to_response('updateInventory.html',
            {'formset': formset, 'location':location},
            context_instance=RequestContext(request)
        )
    
def recordOrder(request, location_number):
    
    OrderFormSet=modelformset_factory(Beverage, form=OrderForm, max_num=0)
    location=Location.objects.get(location_number=location_number)
    qs=Beverage.objects.filter(location__location_number=location_number)
    formset=OrderFormSet(queryset=qs)
    if request.method=='POST':
        formset=OrderFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                beverage=form.save(commit=False)
                units_ordered=form.cleaned_data['units_ordered']
                Order(location=location, beverage=beverage, units_ordered=units_ordered).save()
        return HttpResponseRedirect('/location/' + location_number )
    
    else:
        return render_to_response('record-order.html',
            {'formset': formset, 'location':location},
            context_instance=RequestContext(request)
        )
    
def orderHistory(request, location_number):
    location=Location.objects.get(location_number=location_number)
    order=Order.objects.filter(location__location_number=location_number).order_by('-timestamp')
    
    return render_to_response('order-history.html',
        {'location':location, 'order':order},
        context_instance=RequestContext(request)
    )

def inventoryHistory(request, location_number):
    location=Location.objects.get(location_number=location_number)
    inventory=Inventory.objects.filter(location__location_number=location_number).order_by('-timestamp')
    
    return render_to_response('inventory-history.html',
        {'location':location, 'inventory':inventory},
        context_instance=RequestContext(request)
    )    
    
def startingInventory(request, location_number):
        #change to get obj or 404
    try:
        location = Location.objects.get(location_number=location_number)
        
    except ObjectDoesNotExist:
        return HttpResponse('no location for that')
    
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
def notes(request, location_number):
    return HttpResponse('hello')

def test(request, location_number):
    location=Location.objects.get(location_number=location_number)
    bev=Beverage.objects.filter(location__location_number=location_number)
    
    return render_to_response('test.html',
        {'bev':bev, 'location':location},
        context_instance=RequestContext(request)
    )    