from django.contrib import admin
from SPLArch.product.models import *


class productAdmin(admin.ModelAdmin):
    fieldsets = [
                 ('Products', {'fields': ['name','description'], 'classes': ['collapse']})
                 ]

admin.site.register(Product, productAdmin)
admin.site.register(Project)