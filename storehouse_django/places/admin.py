from django.contrib import admin

from .models import StoragePlace, Formfactor, OpeningType
from items.models import Item

# Register your models here.

#admin.site.register(StoragePlace)
admin.site.register(OpeningType)

class StoragePlaceInline(admin.TabularInline):
    model = StoragePlace

class ItemInline(admin.TabularInline):
    model = Item

@admin.register(StoragePlace)
class StoragePlaceAdmin(admin.ModelAdmin):
    readonly_fields = ('full_humanid', 'volume', 'free_volume', 'used_volume')

    inlines = [
        StoragePlaceInline,
        ItemInline,
    ]


@admin.register(Formfactor)
class FormfactorAdmin(admin.ModelAdmin):
    readonly_fields = ('outside_volume',)

