from django.contrib import admin
from datetime import datetime
from inventory.models import Beverage,Location, LocationStandard, Inventory, Order, Note, StartingInventory


class InventoryInlineAdmin(admin.TabularInline):
    model=Inventory

class BeverageInlineAdmin(admin.TabularInline):
    model=Beverage

class LocationStandardInlineAdmin(admin.TabularInline):
    model=LocationStandard

class StartingInventory(admin.TabularInline):
    model = StartingInventory

class BeverageAdmin(admin.ModelAdmin):
    list_display = ('name',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_number', 'organization',)

    inlines = [
            LocationStandardInlineAdmin, StartingInventory, InventoryInlineAdmin,
            ]


class LocationStandardAdmin(admin.ModelAdmin):
    list_display = ('location', 'beverage', 'fill_to_standard', 'order_when_below')

class OrderInlineAdmin(admin.TabularInline):
    model=Order

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('location','beverage', 'units_reported', 'timestamp',)

class NoteAdmin(admin.ModelAdmin):
    list_display = ('location', 'timestamp', )

admin.site.register(Location, LocationAdmin)
admin.site.register(Beverage, BeverageAdmin)
admin.site.register(LocationStandard, LocationStandardAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Note, NoteAdmin)

