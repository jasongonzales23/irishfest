from django.contrib import admin
from datetime import datetime
from inventory.models import Beverage, Inventory, Location, Order, Note, StartingInventory

class InventoryInlineAdmin(admin.TabularInline):
    model=Inventory

class BeverageInlineAdmin(admin.TabularInline):
    model=Beverage
    
    inlines = [
        InventoryInlineAdmin
    ]

class OrderInlineAdmin(admin.TabularInline):
    model=Order

class StartingInventory(admin.TabularInline):
    model = StartingInventory

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_number', 'organization',)
    
    inlines = [
        BeverageInlineAdmin, StartingInventory, InventoryInlineAdmin, OrderInlineAdmin,
    ]

class BeverageAdmin(admin.ModelAdmin):
    list_display = ('name', 'fill_to_standard', 'order_when_below',)
    
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('beverage', 'location', 'units_reported', 'timestamp',)

class NoteAdmin(admin.ModelAdmin):
    list_display = ('location', 'timestamp', )

admin.site.register(Location, LocationAdmin)
admin.site.register(Beverage, BeverageAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Note, NoteAdmin)