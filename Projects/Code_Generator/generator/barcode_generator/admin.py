from django.contrib import admin
from .models import CustomUser, Barcode

admin.site.register(CustomUser)


@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    list_display = ('barcode_number', 'image')