from django.contrib import admin
from django.forms import Textarea
from SPLArch.requirement.models import Requirement, RequirementType
from django.db import models


class RequirementFeaturesAdminInline(admin.TabularInline):
    model = Requirement.feature.through
    verbose_name_plural = 'Related Features'
    verbose_name = 'Related Feature'
    #fk_name = 'scopeBacklog'
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40,'class':'vLargeTextField',})},
    }

class RequirementAdmin(admin.ModelAdmin):
    fields = ['name','description','status_requirement_choices','requirement_type','priority', 'observations', ]
    inlines = [ RequirementFeaturesAdminInline ]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40,'class':'vLargeTextField',})},
    }
    list_display = ('name', 'requirement_type', 'priority')
    list_filter = ('feature',)

class RequirementTypeAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


admin.site.register(RequirementType, RequirementTypeAdmin)
admin.site.register(Requirement, RequirementAdmin)