from django.contrib import admin
from SPLArch.product.models import *
from django.forms import CheckboxSelectMultiple
from SPLArch.product.mptttreewidget.widget import MpttTreeWidget
from django.forms.models import *
from django.forms import TextInput, Textarea


class ProductMapForm(ModelForm):
    features = ModelMultipleChoiceField(required=False, queryset=Feature.objects.all(), widget=MpttTreeWidget)

    class Meta:
        model = Feature


class ProductAdmin(admin.ModelAdmin):
    form = ProductMapForm
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40,'class':'vLargeTextField',})},
    }


admin.site.register(Product, ProductAdmin)
admin.site.register(Project)
admin.site.register(Feature)
