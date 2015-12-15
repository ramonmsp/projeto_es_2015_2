from django.contrib import admin
from SPLArch.product.models import *
from django.forms import CheckboxSelectMultiple


class ProductAdmin(admin.ModelAdmin):
    formfield_overrides = {
                           models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

admin.site.register(Product, ProductAdmin)
admin.site.register(Project)
admin.site.register(Feature)