from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from inventory.models import Beverage, Location, Inventory, Note, Order, InventoryForm, OrderForm, NoteForm
from inventory.models import LocationStandard
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count, Sum
from django import forms

from django.forms.models import formset_factory, modelformset_factory
import models
import datetime
from django.contrib.auth.decorators import login_required

import itertools

@login_required
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
    inventory = Inventory.objects.filter(location=location).filter(timestamp__gte=latest).select_related()

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
                Inventory(location=location, beverage=beverage, units_reported=units_reported, user=request.user).save()

            return HttpResponseRedirect('/location/' + location_number )
        else:
            return render_to_response('updateInventory.html',
                {'formset': formset, 'location':location},
                context_instance=RequestContext(request)
            )
    else:

        return render_to_response('updateInventory.html',
            {'formset': formset, 'location':location},
            context_instance=RequestContext(request)
        )

def recordOrder(request, location_number):

    OrderFormSet=modelformset_factory(Beverage, form=OrderForm, extra=0)
    location=Location.objects.get(location_number=location_number)
    qs=Beverage.objects.filter(location__location_number=location_number)
    beverage=Order(units_ordered=0)
    formset=OrderFormSet(queryset=qs)

    if request.method=='POST':
        formset=OrderFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                beverage=form.save(commit=False)
                units_ordered=form.cleaned_data['units_ordered']
                Order(location=location, beverage=beverage, units_ordered=units_ordered, user=request.user).save()
            return HttpResponseRedirect('/location/' + location_number )
        else:
            return render_to_response('record-order.html',
                {'formset': formset, 'location':location},
                context_instance=RequestContext(request)
            )

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

    inventory = LocationStandard.objects.filter(location=location).order_by('beverage')

    return render_to_response('starting-inventory.html',
        {'location':location, 'inventory':inventory},
        context_instance=RequestContext(request)
    )

def notes(request, location_number):
    location=Location.objects.get(location_number=location_number)
    notes=Note.objects.filter(location=location).order_by('-timestamp')

    return render_to_response('notes.html',
        {'location':location, 'notes':notes},
        context_instance = RequestContext(request)
    )

def addNote(request, location_number):
    location=Location.objects.get(location_number=location_number)
    if request.method=='POST':
        form=NoteForm(request.POST)
        if form.is_valid():
            note=form.save(commit=False)
            content=form.cleaned_data['content']
            Note(content=content, location=location, user=request.user).save()

        return HttpResponseRedirect('/notes/' + location_number )
    else:
        form=NoteForm()
        return render_to_response('add-note.html',
            {'form': form, 'location':location},
            context_instance=RequestContext(request)
        )

def recordDelivery(request, location_number, order_id, order_delivered):
    #put a try catch of some kind in here
    location=Location.objects.get(location_number=location_number)
    order = Order.objects.get(pk=order_id)
    if request.method=='GET':
        if order_delivered == 'True':
            tog = False
        else:
            tog = True

        order.order_delivered=tog
        order.save()
        return HttpResponse(tog)

def dailyReport(request):
    """
    Build a 2 dimensional array of total units ordered for each beverage in
    each location.

    Returns a two-part tuple of the grid and beverages queryset.
    """
    locations = Location.objects.order_by('name')
    beverages = Beverage.objects.order_by('name')

    orders = Order.objects.values('location', 'beverage').annotate(total_units_ordered=Sum('units_ordered'))

    totals = {}

    for order in orders:
        location = totals.setdefault(order['location'], {})
        location[order['beverage']] = order['total_units_ordered']
        print location[order['beverage']]

    grid = []
    for location in locations:
       row = []
       grid.append((location, row))
       for beverage in beverages:
           row.append(totals.get(location.pk, {}).get(beverage.pk, 0))

    #return grid, beverages
    return render_to_response('daily-report.html',
            {'grid':grid, 'beverages':beverages},
        context_instance=RequestContext(request)
    )


def test(request, location_number):
    location=Location.objects.get(location_number=location_number)
    bev=Beverage.objects.filter(location__location_number=location_number)

    return render_to_response('test.html',
        {'bev':bev, 'location':location, 'orders':orders},
        context_instance=RequestContext(request)
    )
