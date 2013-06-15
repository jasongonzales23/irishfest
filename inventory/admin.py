from django.contrib import admin
from datetime import datetime
from inventory.models import Beverage,Location, LocationStandard, Inventory, Order, Note, InventoryGroup
from inventory.models import Token, TokenBooth, TokenDelivery, TokenCollection
from inventory.models import BoothTokenNote, LocationTokenNote
from inventory.models import OrderAgeWarningTime, InventoryAgeWarningTime

class InventoryGroupAdmin(admin.ModelAdmin):
    model=InventoryGroup

class InventoryInlineAdmin(admin.TabularInline):
    model=Inventory

class BeverageInlineAdmin(admin.TabularInline):
    model=Beverage

class LocationStandardInlineAdmin(admin.TabularInline):
    model=LocationStandard

class OrderInlineAdmin(admin.TabularInline):
    model=Order

class BeverageAdmin(admin.ModelAdmin):
    list_display = ('name','tokenvalue')
    #extra = 5

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_number', 'organization', 'vendor')

    inlines = [
            LocationStandardInlineAdmin, InventoryInlineAdmin,
            ]

class OrderAdmin(admin.ModelAdmin):
    list_display = ('beverage', 'location', 'timestamp','units_ordered','order_delivered')


class LocationStandardAdmin(admin.ModelAdmin):
    list_display = ('beverage', 'fill_to_standard', 'order_when_below')


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('beverage', 'units_reported', 'timestamp',)

class NoteAdmin(admin.ModelAdmin):
    list_display = ('location', 'timestamp', )

class TokenAdmin(admin.ModelAdmin):
    list_display = ('value',)

class TokenBoothAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_number',)

class TokenDeliveryAdmin(admin.ModelAdmin):
    list_display = ('location','tokens','timestamp','fiscal_day', 'user')

class TokenCollectionAdmin(admin.ModelAdmin):
    list_display = ('location','tokens', 'timestamp', 'fiscal_day', 'user')

class OrderAgeWarningTimeAdmin(admin.ModelAdmin):
    list_display = ('time',)

class InventoryAgeWarningTimeAdmin(admin.ModelAdmin):
    list_display = ('time',)

admin.site.register(Location, LocationAdmin)
admin.site.register(Beverage, BeverageAdmin)
admin.site.register(LocationStandard, LocationStandardAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(InventoryGroup, InventoryGroupAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(TokenBooth, TokenBoothAdmin)
admin.site.register(TokenDelivery, TokenDeliveryAdmin)
admin.site.register(TokenCollection, TokenCollectionAdmin)
admin.site.register(OrderAgeWarningTime, OrderAgeWarningTimeAdmin)
admin.site.register(InventoryAgeWarningTime, InventoryAgeWarningTimeAdmin)
