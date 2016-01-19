from django.contrib import admin
from SPLArch.architecture.models import *
from SPLArch.scoping.models import *
from django.forms import TextInput, Textarea
from django.db import models
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.utils.encoding import force_unicode
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django import forms


class ApiAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_report'] = True
        return super(ApiAdmin, self).changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        opts = self.model._meta
        if not request.REQUEST.has_key("_change"):
            if request.REQUEST.has_key("_report"):
                body = API.getReport()
                resp = HttpResponse(body, mimetype='application/pdf')
                resp['Content-Disposition'] = 'attachment; filename=api_report.pdf'
                return resp
            else:
                api = API.objects.get(id=object_id)
                context = {
                    'api': api,
                    'title': _('API: %s') % force_unicode(api.name),
                    'opts': opts,
                    'object_id': object_id,
                    'is_popup': request.REQUEST.has_key('_popup'),
                    'app_label': opts.app_label,
                }
                return render_to_response('admin/fur/api/view.html',
                                          context,
                                          context_instance=RequestContext(request))
        return super(ApiAdmin, self).change_view(request, object_id,
                                                 form_url, extra_context=None)


class ReferencesAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_report'] = True
        return super(ReferencesAdmin, self).changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        opts = self.model._meta
        if not request.REQUEST.has_key("_change"):
            if request.REQUEST.has_key("_report"):
                body = References.getReport()
                resp = HttpResponse(body, mimetype='application/pdf')
                resp['Content-Disposition'] = 'attachment; filename=references_report.pdf'
                return resp
            else:
                references = References.objects.get(id=object_id)
                context = {
                    'references': references,
                    'title': _('References: %s') % force_unicode(references.title),
                    'opts': opts,
                    'object_id': object_id,
                    'is_popup': request.REQUEST.has_key('_popup'),
                    'app_label': opts.app_label,
                }
                return render_to_response('admin/fur/references/view.html',
                                          context,
                                          context_instance=RequestContext(request))
        return super(ReferencesAdmin, self).change_view(request, object_id,
                                                        form_url, extra_context=None)


class TechnologyAdmin(admin.ModelAdmin):
    fields = ['api', 'description', ]
    filter_horizontal = ("api",)


class UseCaseMainStepsAdminInline(admin.TabularInline):
    model = MainSteps
    verbose_name_plural = 'Main Steps'
    verbose_name = 'Main Steps'
    # fk_name = 'scopeBacklog'
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'vLargeTextField', })},
    }


class FeatureAdminInline(admin.TabularInline):
    model = Feature
    verbose_name_plural = 'Features'
    verbose_name = 'Feature'
    # fk_name = 'scopeBacklog'
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'vLargeTextField', })},
    }


class UseCaseAlternativeStepsAdminInline(admin.TabularInline):
    model = AlternativeSteps
    verbose_name_plural = 'Secondary Steps'
    verbose_name = 'Secondary Steps'
    # fk_name = 'scopeBacklog'
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'vLargeTextField', })},
    }


class UseCaseAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'owner', 'feature'
        , 'precondition']
    inlines = [UseCaseMainStepsAdminInline, UseCaseAlternativeStepsAdminInline]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'vLargeTextField', })},
    }
    list_filter = ('feature',)
    filter_horizontal = ("feature", "owner")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_report'] = True
        return super(UseCaseAdmin, self).changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        opts = self.model._meta
        if not request.REQUEST.has_key("_change"):
            if request.REQUEST.has_key("_report"):
                body = UseCase.getReport()
                resp = HttpResponse(body, mimetype='application/pdf')
                resp['Content-Disposition'] = 'attachment; filename=usecase_report.pdf'
                return resp
            else:
                use_case = UseCase.objects.get(id=object_id)
                context = {
                    'use_case': use_case,
                    'title': _('Use Case: %s') % force_unicode(use_case.title),
                    'opts': opts,
                    'object_id': object_id,
                    'is_popup': request.REQUEST.has_key('_popup'),
                    'app_label': opts.app_label,
                }
                return render_to_response('admin/fur/usecase/view.html',
                                          context,
                                          context_instance=RequestContext(request))
        return super(UseCaseAdmin, self).change_view(request, object_id,
                                                     form_url, extra_context=None)


class ArchitectureAdmin(admin.ModelAdmin):
    model = Architecture

    def __unicode__(self):
        return '%s' % self.nome


class ScenariosAdmin(admin.ModelAdmin):
    filter_horizontal = ("nf_requirement", "feature")


class DSSAAdmin(admin.ModelAdmin):
    fields = ["name", "description", "references", "technology", "scenarios", ]
    filter_horizontal = ("references", "technology", "scenarios",)


class AddScenariosForm(forms.ModelForm):
    class Meta:
        model = AddScenarios

    def __init__(self, *args, **kwargs):
        super(AddScenariosForm, self).__init__(*args, **kwargs)
        wtf = Requirement.objects.filter(
            requirement_type=RequirementType.objects.filter(name='Non-functional requirement'));
        print  wtf
        w = self.fields['nf_requirement'].widget
        choices = []
        for choice in wtf:
            choices.append((choice.id, choice.name))
        w.choices = choices


class AddScenariosAdmin(admin.ModelAdmin):
    filter_horizontal = ("nf_requirement", "scenario")
    form = AddScenariosForm


admin.site.unregister(Site)
admin.site.register(UseCase, UseCaseAdmin)
admin.site.register(References, ReferencesAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(API, ApiAdmin)
admin.site.register(Architecture)
admin.site.register(DDSA, DSSAAdmin)
admin.site.register(AddScenarios, AddScenariosAdmin)
admin.site.register(Scenarios, ScenariosAdmin)
admin.site.unregister(Architecture)