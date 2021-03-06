from __future__ import division
from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from inventory.models import Beverage, Location, Inventory, Note, Order, InventoryForm, OrderForm, NoteForm
from inventory.models import LocationStandard, InventoryGroup,OrderGroup
from inventory.models import Token, TokenBooth, TokenDelivery, TokenCollection
from inventory.models import TokenDeliveryForm,TokenCollectionForm
from inventory.models import LocationTokenNote, LocationTokenNoteForm, BoothTokenNote,BoothTokenNoteForm
from inventory.models import OrderAgeWarningTime, InventoryAgeWarningTime

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
from django.contrib.auth.decorators import permission_required

def assignFiscalDay(time):
    """
    if hour is less than or equal to 3, assign fiscal day to the day before
    """
    year = time.year
    month = time.month
    day = time.day
    hour = time.hour
    if time.hour <= 3:
        fiscalDay = datetime(year, month, day -1)
    else:
        fiscalDay = datetime(year, month, day)
    return fiscalDay

@login_required
def showDashboardInventory (request):
    locations = Location.objects.annotate(oldest_inventory=Max('inventory__timestamp')).order_by('oldest_inventory')
    q = InventoryAgeWarningTime.objects.all()
    warningtime = q[0].time
    ctx= {}
    ctx['locations'] = []
    for location in locations:
        if not location.vendor:
            oldest = location.oldest_inventory
            end = datetime.now()
            if oldest:
                flag = end - oldest > timedelta(minutes=warningtime)
            else: 
                flag = 'none'
            ctx['locations'].append((location, flag))
    return render(request, 'dashboard-inventory.html', ctx)

@login_required
def showDashboardOrders (request):
    count = Location.objects.filter(order__order_delivered=False).annotate(undelivered=Count('order__order_delivered'))
    locations = count.annotate(latest_order=Min('order__timestamp')).order_by('latest_order')

    q = OrderAgeWarningTime.objects.all()
    warningtime = q[0].time
    
    ctx= {}
    ctx['locations'] = []
    for location in locations:
        if not location.vendor:
            oldest = location.latest_order
            end = datetime.now()
            flag = end - oldest > timedelta(minutes=warningtime)
            ctx['locations'].append((location, flag))
    return render(request, 'dashboard-orders.html', ctx)

@login_required
def showDashboardNotes (request):
    locations = Location.objects.filter(vendor=False).annotate(oldest_note=Max('note__timestamp'), note_count=Count('note')).order_by('-oldest_note')

    return render_to_response('dashboard-notes.html',
            { 'locations': locations },
            context_instance=RequestContext(request)
            )
@login_required
def showVendorDashboard(request):
    locations = Location.objects.filter(vendor=True).order_by('name')

    return render_to_response('vendor-dashboard.html',
            { 'locations': locations },
            context_instance=RequestContext(request)
            )

@login_required
def showLastInventory(request, location_number):
    #change to get obj or 404
    try:
        location = Location.objects.get(location_number=location_number)

    except ObjectDoesNotExist:
        return HttpResponse('no location for that')
    try:
        latest = Inventory.objects.filter(location=location).latest('group')
        inventory = Inventory.objects.filter(group=latest.group.id).order_by('beverage__name')
    except ObjectDoesNotExist:
        inventory = LocationStandard.objects.filter(location=location).order_by('beverage__name')

    standards = LocationStandard.objects.filter(location=location).order_by('beverage__name')

    return render_to_response('location.html',
            {'location':location, 'inventory':inventory,},
        context_instance=RequestContext(request)
    )

@login_required
def updateInventory(request, location_number):
    InventoryFormSet=modelformset_factory(Beverage, form=InventoryForm, max_num=0)
    location=Location.objects.get(location_number=location_number)
    qs=Beverage.objects.filter(location__location_number=location_number).order_by('name')
    formset=InventoryFormSet(queryset=qs)
    if request.method=='POST':
        formset=InventoryFormSet(request.POST)
        group = InventoryGroup.objects.create()
        if formset.is_valid():
            for form in formset:
                beverage=form.save(commit=False)
                units_reported=form.cleaned_data['units_reported']
                Inventory(location=location, beverage=beverage, units_reported=units_reported,user=request.user, group=group).save()

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

@login_required
def recordOrder(request, location_number):
    OrderFormSet=modelformset_factory(Beverage, form=OrderForm, extra=0)
    location=Location.objects.get(location_number=location_number)
    qs=Beverage.objects.filter(location__location_number=location_number).order_by('name')
    beverage=Order(units_ordered=0)
    formset=OrderFormSet(queryset=qs)

    if request.method=='POST':
        formset=OrderFormSet(request.POST)
        group = OrderGroup.objects.create()
        #print group
        if formset.is_valid():
            for form in formset:
                beverage=form.save(commit=False)
                units_ordered=form.cleaned_data['units_ordered']
                if units_ordered > 0:
                    order_delivered = False
                    Order(location=location, beverage=beverage,units_ordered=units_ordered,user=request.user,order_delivered=order_delivered, group=group).save()
                else:
                    Order(location=location, beverage=beverage,units_ordered=units_ordered, user=request.user, group=group).save()
            return HttpResponseRedirect('/location/' + location_number )
        else:
            return render_to_response('record-order.html',
                {'formset': formset, 'location':location,},
                context_instance=RequestContext(request)
            )

    else:
        return render_to_response('record-order.html',
            {'formset': formset, 'location':location,},
            context_instance=RequestContext(request)
        )

@login_required
def orderHistory(request, location_number):
    #latest = OrderGroup.objects.all().order_by('-id')
    location=Location.objects.get(location_number=location_number)
    order=Order.objects.filter(location__location_number=location_number).order_by('-group__id','beverage__name')

    return render_to_response('order-history.html',
            {'location':location, 'order':order},
        context_instance=RequestContext(request)
    )

@login_required
def inventoryHistory(request, location_number):
    location = Location.objects.get(location_number=location_number)
    inventory = Inventory.objects.filter(location=location).order_by('-group__id','beverage__name')

    return render_to_response('inventory-history.html',
            {'location':location, 'inventory':inventory},
        context_instance=RequestContext(request)
    )

@login_required
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

@login_required
def notes(request, location_number):
    location=Location.objects.get(location_number=location_number)
    notes=Note.objects.filter(location=location).order_by('-timestamp')
    basetemplate = "base.html"
    notehref= "/add-note/" + location.location_number
    return render_to_response('notes.html',
            {'location':location, 'notes':notes, 'notehref':notehref, 'basetemplate':basetemplate},
        context_instance = RequestContext(request)
    )

@login_required
def addNote(request, location_number):
    location=Location.objects.get(location_number=location_number)
    basetemplate = "base.html"
    href={'cancel': "/notes/" + location.location_number, 'form': "/add-note/" + location.location_number}
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
            {'form': form, 'location':location, 'href': href, 'basetemplate': basetemplate},
            context_instance=RequestContext(request)
        )

@login_required
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

def report(request):
    """
    Build a 2 dimensional array of total units ordered for each beverage in
    each location.

    Returns a two-part tuple of the grid and beverages queryset.
    """
    locations = Location.objects.filter(vendor=False).order_by('location_number')
    beverages = Beverage.objects.order_by('name')

    orders = Order.objects.values('location', 'beverage').annotate(total_units_ordered=Sum('units_ordered'))

    totals = {}

    for order in orders:
        location = totals.setdefault(order['location'], {})
        location[order['beverage']] = order['total_units_ordered']

    grid = []
    for beverage in beverages:
        row = []
        grid.append((beverage, row))

        rowtotal = 0
        for location in locations:
            itemtotal = totals.get(location.pk, {}).get(beverage.pk, 0)
            rowtotal += itemtotal
            row.append(itemtotal)
        row.append(rowtotal)

    orders = reportList(request)

    return render_to_response('daily-report.html',
            {'grid':grid, 'locations':locations,'orders': orders},
            context_instance=RequestContext(request)
    )

def dailyReport(request, year, month, day):
    locations = Location.objects.filter(vendor=False).order_by('location_number')
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

    grid = []
    for beverage in beverages:
        row = []
        grid.append((beverage, row))

        rowtotal = 0
        for location in locations:
            itemtotal = totals.get(location.pk, {}).get(beverage.pk, 0)
            rowtotal += itemtotal
            row.append(itemtotal)
        row.append(rowtotal)

    orders = reportList(request)

    return render_to_response('daily-report.html',
            {'grid':grid, 'locations':locations, 'orders':orders,'requestString': requestString},
        context_instance=RequestContext(request)
    )

def latestOrders(request):
    locations = Location.objects.filter(vendor=False).order_by('location_number').annotate(most_recent=Max('order__group'))
    orders = Order.objects.annotate(most_recent=Max('timestamp')).order_by('-group__id', 'beverage__name')
    newest = Order.objects.filter(group__in=[l.most_recent for l in locations])

    grid = []
    for location in locations:
        row = []
        time = []
        reporter = []
        grid.append((location, row, time, reporter))
        for new in newest:
            if new.location == location:
                time.append((new.timestamp))
                reporter.append((new.user))
                row.append((new.beverage, new.units_ordered, new.order_delivered))

    return render_to_response('latest-orders.html',
            {'grid':grid,},
            context_instance=RequestContext(request)
    )

def latestInventories(request):
    locations = Location.objects.filter(vendor=False).order_by('location_number').annotate(most_recent=Max('inventory__group'))
    inventories = Inventory.objects.annotate(most_recent=Max('timestamp')).order_by('-group__id', 'beverage__name')
    newest = Inventory.objects.filter(group__in=[l.most_recent for l in locations])
    standards = LocationStandard.objects.all()

    grid = []
    for location in locations:
        row = []
        time = []
        reporter = []
        grid.append((location, row, time, reporter))
        for new in newest:
            if new.location == location:
                time.append((new.timestamp))
                reporter.append((new.user))
                for standard in standards:
                    if standard.beverage == new.beverage and standard.location == location:
                        #print standard.beverage
                        row.append((new.beverage, new.units_reported, standard.order_when_below, standard.fill_to_standard))


    return render_to_response('latest-report.html',
            {'grid':grid},
            context_instance=RequestContext(request)
    )

def unfilledOrders(request):
    locations = Location.objects.filter(vendor=False).order_by('location_number')
    orders = Order.objects.all().order_by('-group__id', 'beverage__name')

    grid = []
    for location in locations:
        row = []
        grid.append(( location, row))
        for order in orders:
            if order.location == location and order.order_delivered == False:
                row.append((order.beverage, order.timestamp, order.order_delivered,))

    return render_to_response('unfilled-orders.html',
            {'grid':grid},
            context_instance=RequestContext(request)
    )
"""
def latestNotes(request):
    locations = Location.objects.annotate(oldest_note=Max('note__timestamp')).order_by('location_number')

    return render(request, 'latest-notes.html', locations)
"""
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
    locationNumRow = ['',]
    for location in locations:
        locationNumRow.append(location.location_number)
    writer.writerow(locationNumRow)

    locationRow = ['',]
    for location in locations:
        locationRow.append(location)
    writer.writerow(locationRow)


    for order in orders:
        location = totals.setdefault(order['location'], {})
        location[order['beverage']] = order['total_units_ordered']

    for beverage in beverages:
        row = []
        row.append(beverage.name)
        rowtotal = 0
        for location in locations:
            itemtotal = totals.get(location.pk, {}).get(beverage.pk, 0)
            rowtotal += itemtotal
            row.append(itemtotal)
        row.append(rowtotal)
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
    locationRow = ['',]
    for location in locations:
        locationRow.append(location)
    writer.writerow(locationRow)


    for order in orders:
        location = totals.setdefault(order['location'], {})
        location[order['beverage']] = order['total_units_ordered']

    for beverage in beverages:
        row = []
        row.append(beverage.name)
        rowtotal = 0
        for location in locations:
            itemtotal = totals.get(location.pk, {}).get(beverage.pk, 0)
            rowtotal += itemtotal
            row.append(itemtotal)
        row.append(rowtotal)
        writer.writerow(row)

    return response

@permission_required('inventory.add_tokendelivery')
def tokensDelivered(request, location_number):
    location=TokenBooth.objects.get(location_number=location_number)
    tokens=TokenDelivery.objects.filter(location=location).order_by('-timestamp')
    locationtype = "booth"
    return render_to_response('token-delivery.html',
            {'location':location ,'tokens':tokens, 'locationtype': locationtype},
            context_instance=RequestContext(request)
    )

@permission_required('inventory.add_tokendelivery')
def recordTokenDelivery(request, location_number):
    location=TokenBooth.objects.get(location_number=location_number)
    locationtype = "booth"

    form=TokenDeliveryForm()
    if request.method=='POST':
        form=TokenDeliveryForm(request.POST)
        if form.is_valid():
            tokendelivery=form.save(commit=False)
            tokens=form.cleaned_data['tokens']
            fiscal_day = assignFiscalDay(datetime.now())
            TokenDelivery(location=location,tokens=tokens,user=request.user, fiscal_day=fiscal_day).save()

            return HttpResponseRedirect('/token/booth/' + location_number )
        else:
            return render_to_response('record-delivery.html',
                    {'form': form, 'location':location, 'locationtype': locationtype},
                context_instance=RequestContext(request)
            )

    else:
        return render_to_response('record-delivery.html',
                {'form': form, 'location':location,'locationtype':locationtype},
            context_instance=RequestContext(request)
        )

@permission_required('inventory.add_tokencollection')
def tokensCollected(request, location_number):
    location=Location.objects.get(location_number=location_number)
    tokens=TokenCollection.objects.filter(location=location).order_by('-timestamp')
    
    return render_to_response('tokens-collected.html',
            {'location':location ,'tokens':tokens},
            context_instance=RequestContext(request)
    )

@permission_required('inventory.add_tokencollection')
def recordTokenCollection(request, location_number):
    location=Location.objects.get(location_number=location_number)
    form=TokenCollectionForm()
    if request.method=='POST':
        form=TokenCollectionForm(request.POST)
        if form.is_valid():
            tokencollection=form.save(commit=False)
            tokens=form.cleaned_data['tokens']
            fiscal_day = assignFiscalDay(datetime.now())
            TokenCollection(location=location,tokens=tokens,user=request.user, fiscal_day=fiscal_day).save()

            return HttpResponseRedirect('/token/location/' + location_number )
        else:
            return render_to_response('record-collection.html',
                {'form': form, 'location':location},
                context_instance=RequestContext(request)
            )

    else:
        return render_to_response('record-collection.html',
            {'form': form, 'location':location,},
            context_instance=RequestContext(request)
        )

@permission_required('inventory.add_boothtokennote')
def addBoothTokenNote(request, location_number):
    location=TokenBooth.objects.get(location_number=location_number)
    basetemplate = "token-base.html"
    href={'cancel': "/token/note/booth/" + location.location_number, 'form': "/token/add-note/booth/" + location.location_number}
    locationtype = "booth"
    if request.method=='POST':
        form=BoothTokenNoteForm(request.POST)
        if form.is_valid():
            note=form.save(commit=False)
            content=form.cleaned_data['content']
            BoothTokenNote(content=content, location=location, user=request.user).save()

        return HttpResponseRedirect('/token/note/booth/' + location_number )
    else:
        form=BoothTokenNoteForm()
        return render_to_response('add-note.html',
            {'form': form, 'location':location, 'basetemplate': basetemplate, 'href': href, 'locationtype': locationtype},
            context_instance = RequestContext(request)
            )

@permission_required('inventory.add_locationtokennote')
def addLocationTokenNote(request, location_number):
    location=Location.objects.get(location_number=location_number)
    basetemplate = "token-base.html"
    href={'cancel': "/token/note/location/" + location.location_number, 'form': "/token/add-note/location/" + location.location_number}
    if request.method=='POST':
        form=LocationTokenNoteForm(request.POST)
        if form.is_valid():
            note=form.save(commit=False)
            content=form.cleaned_data['content']
            LocationTokenNote(content=content, location=location, user=request.user).save()

        return HttpResponseRedirect('/token/note/location/' + location_number )
    else:
        form=NoteForm()
        return render_to_response('add-note.html',
                {'form': form, 'location':location, 'basetemplate': basetemplate, 'href': href},
            context_instance = RequestContext(request)
            )

@permission_required('inventory.add_locationtokennote')
def locationTokenNote(request, location_number):
    location=Location.objects.get(location_number=location_number)
    notes=LocationTokenNote.objects.filter(location=location).order_by('-timestamp')
    basetemplate = "token-base.html"
    notehref = "/token/add-note/location/" + location.location_number
    return render_to_response('notes.html',
            {'location':location, 'notes':notes, 'basetemplate':basetemplate, 'notehref':notehref},
        context_instance = RequestContext(request)
    )

@permission_required('inventory.add_boothtokennote')
def boothTokenNote(request, location_number):
    location=TokenBooth.objects.get(location_number=location_number)
    notes=BoothTokenNote.objects.filter(location=location).order_by('-timestamp')
    basetemplate = "token-base.html"
    notehref = "/token/add-note/booth/" + location.location_number
    locationtype = "booth"
    return render_to_response('notes.html',
            {'location':location, 'notes':notes, 'basetemplate':basetemplate, 'notehref':notehref, 'locationtype': locationtype},
        context_instance = RequestContext(request)
    )

@permission_required('inventory.add_token')
def collectionReport(request):
    locations = Location.objects.filter(vendor=False).order_by('location_number')
    tokens = TokenCollection.objects.order_by('location', 'fiscal_day')
    dates = TokenCollection.objects.dates('fiscal_day','day');

    grid = []
    for location in locations:
        row = []
        grid.append((location, row))
        rowtotal = 0
        for date in dates:
            daytotal = 0
            for token in tokens:
                if token.location == location and token.fiscal_day == date.date():
                    daytotal += token.tokens
                    rowtotal += token.tokens
            row.append(daytotal)
        row.append(rowtotal)

    grandtotal = []
    tokentotal = 0
    for date in dates:
        daytotal = 0
        for token in tokens:
            if token.timestamp.date() == date.date():
                daytotal += token.tokens
                tokentotal += token.tokens
        grandtotal.append(daytotal)
    grandtotal.append(tokentotal)

    return render_to_response('collection-report.html',
            {'tokens':tokens, 'grid':grid, 'dates': dates,'grandtotal':grandtotal,},
        context_instance = RequestContext(request)
    )

@permission_required('inventory.add_token')
def csvCollectionReport(request):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment;filename=token-collection-report.csv'
    writer = csv.writer(response)
    
    locations = Location.objects.order_by('location_number')
    tokens = TokenCollection.objects.order_by('location', 'fiscal_day')
    dates = TokenCollection.objects.dates('fiscal_day','day');
    
    heading= ['Token Collection Report']
    writer.writerow(heading)
    daterow = ['Beverage Station']
    for date in dates:
        daterow.append(date.date())

    daterow.append('Total')
    writer.writerow(daterow)

    for location in locations:
        row = []
        rowtotal = 0
        row.append(location)
        for date in dates:
            daytotal = 0
            for token in tokens:
                if token.location == location and token.fiscal_day == date.date():
                    daytotal += token.tokens
                    rowtotal += token.tokens
            row.append(daytotal)
        row.append(rowtotal)
        writer.writerow(row)
    grandtotal = ['Grand Total']

    tokentotal = 0
    for date in dates:
        daytotal = 0
        for token in tokens:
            if token.timestamp.date() == date.date():
                daytotal += token.tokens
                tokentotal += token.tokens
        grandtotal.append(daytotal)
    grandtotal.append(tokentotal)
    
    writer.writerow(grandtotal)
    return response

@permission_required('inventory.add_token')
def deliveryReport(request):
    locations = TokenBooth.objects.order_by('location_number')
    tokens = TokenDelivery.objects.order_by('location', 'fiscal_day')
    dates = TokenDelivery.objects.dates('fiscal_day','day');

    grid = []
    for location in locations:
        row = []
        grid.append((location, row))
        rowtotal = 0
        for date in dates:
            daytotal = 0
            for token in tokens:
                if token.location == location and token.fiscal_day == date.date():
                    daytotal += token.tokens
                    rowtotal += token.tokens
            row.append(daytotal)
        row.append(rowtotal)

    grandtotal = []
    tokentotal = 0
    for date in dates:
        daytotal = 0
        for token in tokens:
            if token.timestamp.date() == date.date():
                daytotal += token.tokens
                tokentotal += token.tokens
        grandtotal.append(daytotal)
    grandtotal.append(tokentotal)

    return render_to_response('delivery-report.html',
            {'tokens':tokens, 'grid':grid, 'dates': dates,'grandtotal': grandtotal,},
        context_instance = RequestContext(request)
    )

@permission_required('inventory.add_token')
def csvDeliveryReport(request):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment;filename=token-delivery-report.csv'
    writer = csv.writer(response)

    locations = TokenBooth.objects.order_by('location_number')
    tokens = TokenDelivery.objects.order_by('location', 'fiscal_day')
    dates = TokenDelivery.objects.dates('fiscal_day','day');
    
    heading= ['Token Collection Report']
    writer.writerow(heading)
    daterow = ['Beverage Station']
    for date in dates:
        daterow.append(date.date())
    daterow.append('Total')
    writer.writerow(daterow)

    for location in locations:
        row = []
        row.append(location)
        rowtotal = 0
        for date in dates:
            daytotal = 0
            for token in tokens:
                if token.location == location and token.fiscal_day == date.date():
                    daytotal += token.tokens
                    rowtotal += token.tokens
            row.append(daytotal)
        row.append(rowtotal)
        writer.writerow(row)

    grandtotal = ['Grand Total']
    tokentotal = 0
    for date in dates:
        daytotal = 0
        for token in tokens:
            if token.timestamp.date() == date.date():
                daytotal += token.tokens
                tokentotal += token.tokens
        grandtotal.append(daytotal)
    grandtotal.append(tokentotal)
    writer.writerow(grandtotal)

    return response

@permission_required('inventory.add_token')
def reconciliationReport(request):
    locations = Location.objects.filter(vendor=False).order_by('location_number')
    tokens = TokenCollection.objects.order_by('location', 'fiscal_day')
    dates = TokenCollection.objects.dates('fiscal_day','day');
    orders = Order.objects.order_by('location__location_number')
    tokenval = 2
    grid = []
    for location in locations:
        row = []
        daytotals = []
        grid.append((location, daytotals, row))
        rowtotal = 0
        for date in dates:
            daytotal = 0
            for token in tokens:
                if token.location == location and token.fiscal_day == date.date():
                    daytotal += token.tokens
                    rowtotal += token.tokens
            daytotals.append(daytotal)
        row.append(rowtotal)
        
        totalinv = 0
        for order in orders:
            if order.location == location:
                totalinv += order.units_ordered * order.beverage.tokenvalue
        totalinv = totalinv * tokenval
        row.append(totalinv)
        if rowtotal == 0 or totalinv == 0:
            tokendelta = 'NA'
        else:
            tokendelta = round((-100 * ((totalinv - (rowtotal * tokenval)) / totalinv )),2)
        row.append(tokendelta)
    
    grandtotal = []
    daytotals = []
    row = []
    grandtotal.append((daytotals, row))
    tokentotal = 0
    for date in dates:
        daytotal = 0
        for token in tokens:
            if token.timestamp.date() == date.date():
                daytotal += token.tokens
                tokentotal += token.tokens
        daytotals.append(daytotal)

    invdelivered = 0
    for order in orders:
        invdelivered += order.units_ordered * order.beverage.tokenvalue
    invdelivered = invdelivered * tokenval
    row.append(tokentotal)
    row.append(invdelivered)

    if invdelivered == 0:
        granddelta = 'NA'
    else:
        granddelta = round((-100 * ((invdelivered - (tokentotal * tokenval)) / invdelivered)), 2)

    row.append(granddelta)

    return render_to_response('reconciliation-report.html',
            {'tokens':tokens, 'grid':grid, 'dates': dates, 'grandtotal':grandtotal},
        context_instance = RequestContext(request)
    )

@permission_required('inventory.add_token')
def csvReconciliationReport(request):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment;filename=token-reconciliation-report.csv'

    writer = csv.writer(response)

    locations = Location.objects.order_by('location_number')
    tokens = TokenCollection.objects.order_by('location', 'fiscal_day')
    dates = TokenCollection.objects.dates('fiscal_day','day');
    orders = Order.objects.order_by('location__location_number')

    heading= ['Token Reconciliation Report']
    writer.writerow(heading)
    daterow = ['Beverage Station']
    for date in dates:
        daterow.append(date.date())
    daterow.append('Token Total')
    daterow.append('Inventory Delivered in $')
    daterow.append('Token Delta as %')

    writer.writerow(daterow)

    tokenval = 2
    for location in locations:
        row = []
        row.append(location) 
        rowtotal = 0
        for date in dates:
            daytotal = 0
            for token in tokens:
                if token.location == location and token.fiscal_day == date.date():
                    daytotal += token.tokens
                    rowtotal += token.tokens
            row.append(daytotal)
        row.append(rowtotal)
        
        totalinv = 0
        for order in orders:
            if order.location == location:
                totalinv += order.units_ordered * order.beverage.tokenvalue
        totalinv = totalinv * tokenval
        row.append(totalinv)
        if rowtotal == 0 or totalinv == 0:
            tokendelta = 'NA'
        else:
            tokendelta = round((-100 * ((totalinv - (rowtotal * tokenval)) / totalinv )),2)
        row.append(tokendelta)
        writer.writerow(row)

    grandtotal = ['Grand Totals']
    tokentotal = 0
    for date in dates:
        daytotal = 0
        for token in tokens:
            if token.timestamp.date() == date.date():
                daytotal += token.tokens
                tokentotal += token.tokens
        grandtotal.append(daytotal)

    invdelivered = 0
    for order in orders:
        invdelivered += order.units_ordered * order.beverage.tokenvalue
    invdelivered = invdelivered * tokenval
    grandtotal.append(tokentotal)
    grandtotal.append(invdelivered)
    
    if invdelivered == 0:
        granddelta = 'NA'
    else:
        granddelta = round((-100 * ((invdelivered - (tokentotal * tokenval)) / invdelivered)), 2)

    grandtotal.append(granddelta)
    writer.writerow(grandtotal)

    return response

