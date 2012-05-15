from django.contrib import admin
from datetime import datetime
from inventory.models import Beverage, Inventory, Location, Order, Note

class BeverageInlineAdmin(admin.StackedInline):
    model=Beverage

class InventoryInlineAdmin(admin.TabularInline):
    model=Inventory

class OrderInlineAdmin(admin.TabularInline):
    model=Order

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_number', 'organization',)
    
    inlines = [
        BeverageInlineAdmin, InventoryInlineAdmin#, OrderInlineAdmin,
    ]

class BeverageAdmin(admin.ModelAdmin):
    list_display = ('name', 'fill_to_standard', 'order_when_below',)
    
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('beverage', 'units_reported', 'timestamp',)


admin.site.register(Location, LocationAdmin)
admin.site.register(Beverage, BeverageAdmin)
admin.site.register(Inventory, InventoryAdmin)