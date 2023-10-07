
from django.contrib import admin

from .models import Inventory
# Register your models here.

class InventoryAdmin(admin.ModelAdmin):

    model = Inventory
    list_search = ['client']

admin.site.register(Inventory, InventoryAdmin)