from django.contrib import admin

from .models import StoragePlace, Formfactor, OpeningType

# Register your models here.

admin.site.register(StoragePlace)
admin.site.register(Formfactor)
admin.site.register(OpeningType)


