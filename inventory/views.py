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
from django.db.models import Q, Count, Sum, Max, Min
from django import forms

from django.forms.models import formset_factory, modelformset_factory
import models
import datetime
from datetime import datetime, date, time
from datetime import timedelta
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

    lt = time(h,m,s)
    latest = datetime.combine(d, lt)
    inventory = Inventory.objects.filter(location=location).filter(timestamp__gte=latest).select_related().order_by('beverage')
    return render_to_response('location.html',
            {'location':location, 'inventory':inventory},
        context_instance=RequestContext(request)
    )

def updateInventory(request, location_number):
    InventoryFormSet=modelformset_factory(Beverage, form=InventoryForm, max_num=0)
    location=Location.objects.get(location_number=location_number)
    qs=Beverage.objects.filter(location__location_number=location_number).order_by('name')
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
    qs=Beverage.objects.filter(location__location_number=location_number).order_by('name')
    beverage=Order(units_ordered=0)
    formset=OrderFormSet(queryset=qs)
    latest = Inventory.objects.filter(location=location).latest('timestamp')
    latest = latest.timestamp
    d = latest.date()
    h = latest.hour
    m = latest.minute
    s = latest.second - 1

    lt = time(h,m,s)
    latest = datetime.combine(d, lt)
    inventory = Inventory.objects.filter(location=location).filter(timestamp__gte=latest).select_related().order_by('beverage')

    if request.method=='POST':
        formset=OrderFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                beverage=form.save(commit=False)
                units_ordered=form.cleaned_data['units_ordered']
                if units_ordered > 0:
                    order_delivered = False
                    Order(location=location, beverage=beverage,units_ordered=units_ordered, user=request.user, order_delivered=order_delivered).save()
                else:
                    Order(location=location, beverage=beverage,units_ordered=units_ordered, user=request.user).save()
            return HttpResponseRedirect('/location/' + location_number )
        else:
            return render_to_response('record-order.html',
                {'formset': formset, 'location':location,'inventory':inventory},
                context_instance=RequestContext(request)
            )

    else:
        return render_to_response('record-order.html',
            {'formset': formset, 'location':location,'inventory':inventory},
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

    inventory = LocationStandard.objects.filter(location=location).order_by('beverage__name')

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

def reportList(request):
    orders = Order.objects.all().order_by('timestamp')
    return orders
    """
    return render_to_response('reportList.html',
            {'orders':orders,},
            context_instance=RequestContext(request)
        )
    """

def report(request):
    """
    Build a 2 dimensional array of total units ordered for each beverage in
    each location.

    Returns a two-part tuple of the grid and beverages queryset.
    """
    locations = Location.objects.order_by('location_number')
    beverages = Beverage.objects.order_by('name')

    orders = Order.objects.values('location', 'beverage').annotate(total_units_ordered=Sum('units_ordered'))

    totals = {}

    for order in orders:
        location = totals.setdefault(order['location'], {})
        location[order['beverage']] = order['total_units_ordered']

    grid = []
    for location in locations:
       row = []
       grid.append((location, row))
       for beverage in beverages:
           row.append(totals.get(location.pk, {}).get(beverage.pk, 0))
    
    orders = reportList(request)
    
    return render_to_response('daily-report.html',
            {'grid':grid, 'beverages':beverages,'orders': orders},
        context_instance=RequestContext(request)
    )


def dailyReport(request, year, month, day):
    """
    Build a 2 dimensional array of total units ordered for each beverage in
    each location.

    Returns a two-part tuple of the grid and beverages queryset.
    """
    locations = Location.objects.order_by('location_number')
    beverages = Beverage.objects.order_by('name')
    requestString = '/report/' + year +'/' + month +'/'+ day+ '/'

    year = int(year)
    month = int(month)
    day = int(day)
    
   
    orders = Order.objects.filter(timestamp__year=year,timestamp__month=month,timestamp__day=day).values('location', 'beverage').annotate(total_units_ordered=Sum('units_ordered'))

    totals = {}

    for order in orders:
        location = totals.setdefault(order['location'], {})
        location[order['beverage']] = order['total_units_ordered']
        #print location[order['beverage']]

    grid = []
    for location in locations:
       row = []
       grid.append((location, row))
       for beverage in beverages:
           row.append(totals.get(location.pk, {}).get(beverage.pk, 0))

    orders = reportList(request)


    return render_to_response('daily-report.html',
            {'grid':grid, 'beverages':beverages, 'orders':orders,'requestString': requestString},
        context_instance=RequestContext(request)
    )

def latestOrders(request):
    locations = Location.objects.all().order_by('name').annotate(most_recent=Max('order__timestamp'))
    orders = Order.objects.annotate(most_recent=Max('timestamp')).order_by('-timestamp')
    newest = Order.objects.filter(timestamp__in=[l.most_recent for l in locations])

    grid = []
    for location in locations:
        row = []
        time = []
        reporter = []
        grid.append((location, row, time, reporter))
        for new in newest:
            if new.location == location:
                delt = new.timestamp - timedelta(seconds=2)
                time.append((new.timestamp))
                reporter.append((new.user))
                for order in orders:
                    if order.timestamp > delt and order.location == location:
                        row.append((order.beverage, order.units_ordered, order.order_delivered))

    return render_to_response('latest-orders.html',
            {'grid':grid,},
            context_instance=RequestContext(request)
    )

def latestInventories(request):
    locations = Location.objects.all().order_by('name').annotate(most_recent=Max('inventory__timestamp'))
    inventories = Inventory.objects.annotate(most_recent=Max('timestamp')).order_by('-timestamp')
    newest = Inventory.objects.filter(timestamp__in=[l.most_recent for l in locations])
    standards = LocationStandard.objects.all()

    grid = []
    for location in locations:
        row = []
        time = []
        reporter = []
        grid.append((location, row, time, reporter))
        for new in newest:
            if new.location == location:
                delt = new.timestamp - timedelta(seconds=2)
                time.append((new.timestamp))
                reporter.append((new.user))
                for inv in inventories:
                    if inv.timestamp > delt and inv.location == location:
                        for standard in standards:
                            if standard.beverage == inv.beverage  and standard.location == location:
                                row.append((inv.beverage, inv.units_reported, standard.order_when_below, standard.fill_to_standard))

    return render_to_response('latest-report.html',
            {'grid':grid},
            context_instance=RequestContext(request)
    )


def unfilledOrders(request):
    locations = Location.objects.all().order_by('name')
    orders = Order.objects.all().order_by('location__name')
    
    grid = []
    for location in locations:
        row = []
        grid.append(( location.name, row))
        for order in orders:
            if order.location == location and order.order_delivered == False:
                row.append((order.beverage, order.timestamp, order.order_delivered,))

    return render_to_response('unfilled-orders.html',
            {'grid':grid},
            context_instance=RequestContext(request)
    )


import csv

def csvTotal(request):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment;filename=festival-total.csv'

    writer = csv.writer(response)

    locations = Location.objects.order_by('location_number')
    beverages = Beverage.objects.order_by('name')

    orders = Order.objects.values('location', 'beverage').annotate(total_units_ordered=Sum('units_ordered'))

    totals = {}
    writer.writerow(['Festival Total']);
    bevRow = ['Location #','Location',]
    for beverage in beverages:
        bevRow.append(beverage.name)
    writer.writerow(bevRow)

    for order in orders:
        location = totals.setdefault(order['location'], {})
        location[order['beverage']] = order['total_units_ordered']

    for location in locations:
        row = []
        row.append(location.location_number)
        row.append(location)
        for beverage in beverages:
            row.append(totals.get(location.pk, {}).get(beverage.pk, 0))
        writer.writerow(row)

    return response

def csvDailyReport(request, year, month, day):
    dateString = year+'-'+ month+'-'+ day
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment;filename='+ dateString +'.csv'

    writer = csv.writer(response)

    locations = Location.objects.order_by('location_number')
    beverages = Beverage.objects.order_by('name')

    year = int(year)
    month = int(month)
    day = int(day)

    orders = Order.objects.filter(timestamp__year=year,timestamp__month=month,timestamp__day=day).values('location', 'beverage').annotate(total_units_ordered=Sum('units_ordered'))

    totals = {}

    writer.writerow(['Total for', dateString ]);
    bevRow = ['Location #','Location',]
    for beverage in beverages:
        bevRow.append(beverage.name)

    writer.writerow(bevRow)

    for order in orders:
        location = totals.setdefault(order['location'], {})
        location[order['beverage']] = order['total_units_ordered']

    for location in locations:
        row = []
        row.append(location.location_number)
        row.append(location)
        for beverage in beverages:
            row.append(totals.get(location.pk, {}).get(beverage.pk, 0))
        writer.writerow(row)

    return response

