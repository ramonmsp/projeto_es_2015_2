from django.contrib import admin
from SPLArch.product.models import Product


class productAdmin(admin.ModelAdmin):
    fieldsets = [
                 ('Products', {'fields': ['name','description'], 'classes': ['collapse']})
                 ]

admin.site.register(Product, productAdmin)