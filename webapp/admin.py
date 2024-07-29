from django.contrib import admin
from .models import AssetRecord






class AssetRecordAdmin(admin.ModelAdmin):
    list_display = ('description', 'asset_code', 'nomenclature','serial_number_t24', 'serial_number', 'supplier', 'warranty')
   
admin.site.register(AssetRecord, AssetRecordAdmin)

# Register your models here.
