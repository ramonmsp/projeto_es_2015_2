from django.contrib import admin
from SPLArch.architecture.models import *
from SPLArch.scoping.models import Feature, Product, Glossary, Project, BindingTime
from SPLArch.requirement.models import *
from django.forms import *
from mptttreewidget.widget import MpttTreeWidget
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.template import RequestContext
from django.http import HttpResponse
from django.core.files.temp import NamedTemporaryFile
from django.db import models
import os
import zipfile
import StringIO
import codecs


class ProductMapForm(ModelForm):
    features = ModelMultipleChoiceField(required=False, queryset=Feature.objects.all(), widget=MpttTreeWidget)

    class Meta:
        model = Feature

class ProductAdmin(admin.ModelAdmin):
    #fields = ['name', 'description','configuration']
    form = ProductMapForm
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40,'class':'vLargeTextField',})},
    }

    def change_view(self, request, object_id, form_url='', extra_context=None):
        opts = self.model._meta
        if not request.REQUEST.has_key("_change"):
            if request.REQUEST.has_key("_zipreport"):
                product = Product.objects.get(id=object_id)
                #use case
                usecase = UseCase.getReport(product)
                usecaseTemp = NamedTemporaryFile()
                usecaseTemp.close()
                usecaseTemp = codecs.open(usecaseTemp.name,'wb')
                usecaseTemp.write(usecase)
                usecaseTemp.close()

                #Feature
                features = Feature.getReport(Product.objects.get(id=object_id))
                featuresTemp = NamedTemporaryFile()
                featuresTemp.close()
                featuresTemp = codecs.open(featuresTemp.name,'wb')
                featuresTemp.write(features)
                featuresTemp.close()

                #Glossary
                glossary = Glossary.getReport(Product.objects.get(id=object_id))
                glossaryTemp = NamedTemporaryFile()
                glossaryTemp.close()
                glossaryTemp = codecs.open(glossaryTemp.name,'wb')
                glossaryTemp.write(glossary)
                glossaryTemp.close()

                #Test Case
                #testCase = TestCase.getReport(Product.objects.get(id=object_id))
               # testCaseTemp = NamedTemporaryFile()
               # testCaseTemp.close()
               # testCaseTemp = codecs.open(testCaseTemp.name,'wb')
               #testCaseTemp.write(testCase)
                #testCaseTemp.close()


                #User story
                #userStory = UserStory.getReport(Product.objects.get(id=object_id))
                #userStoryTemp = NamedTemporaryFile()
                #userStoryTemp.close()
                #userStoryTemp = codecs.open(userStoryTemp.name,'wb')
                #userStoryTemp.write(userStory)
                #userStoryTemp.close()


                # Folder name in ZIP archive which contains the above files
                # E.g [thearchive.zip]/somefiles/file2.txt
                # FIXME: Set this to something better
                zip_subdir = product.name.replace(" ", "_")+"_artifacs"
                zip_filename = "%s.zip" % zip_subdir

                # Open StringIO to grab in-memory ZIP contents
                s = StringIO.StringIO()

                # The zip compressor
                zf = zipfile.ZipFile(s, "w")

                # Calculate path for file in zip
                usecase_zip_path = os.path.join(zip_subdir, product.name+ "_usecase_report.pdf")
                feature_zip_path = os.path.join(zip_subdir, product.name+ "_features_report.pdf")
                glossary_zip_path = os.path.join(zip_subdir, product.name+ "_glossary_report.pdf")
                testCase_zip_path = os.path.join(zip_subdir, product.name+ "_testCase_report.pdf")
                userStory_zip_path = os.path.join(zip_subdir, product.name+ "_userStory_report.pdf")

                # Add file, at correct path
                zf.write(usecaseTemp.name, usecase_zip_path)
                zf.write(featuresTemp.name, feature_zip_path)
                zf.write(glossaryTemp.name, glossary_zip_path)
                #zf.write(testCaseTemp.name, testCase_zip_path)
                #zf.write(userStoryTemp.name, userStory_zip_path)

                # Must close zip for all contents to be written
                zf.close()

                # Grab ZIP file from in-memory, make response with correct MIME-type
                resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
                # ..and correct content-disposition
                resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
                return resp
            else:
                product = Product.objects.get(id=object_id)
                context = {
                    'product': product,
                    'title': _('Product: %s') % force_unicode(product.name),
                    'opts': opts,
                    'object_id': object_id,
                    'is_popup': request.REQUEST.has_key('_popup'),
                    'app_label': opts.app_label,
                    }
                return render_to_response('admin/fur/product/view.html',
                                          context,
                                          context_instance=RequestContext(request))
        return super(ProductAdmin, self).change_view(request, object_id,
            form_url, extra_context=None)


class FeatureExcludeAdminInline(admin.TabularInline):
    model = Feature.excludes.through
    verbose_name_plural = 'Excluded features'
    verbose_name = 'Excluded feature'
    #I got the fk_name using the django shell, by inspecting the objet Feature
    fk_name = 'from_feature'
    extra = 0
    #form = ExcludedFeaturesForm

class FeatureRequireAdminInline(admin.TabularInline):
    model = Feature.requires.through
    verbose_name_plural = 'Required features'
    verbose_name = 'Required feature'
    #I gor the fk_name using the django shell, by inspecting the objet Feature
    fk_name = 'from_feature'
    extra = 0
    #form = RequiredFeaturesForm


class FeatureAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'type', 'variability'  , 'binding_time' , 'parent' , 'glossary', ]
    inlines = [ FeatureRequireAdminInline, FeatureExcludeAdminInline, ]
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    filter_horizontal = ("glossary",)
    list_filter = ('type', 'variability')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_report'] = True
        return super(FeatureAdmin, self).changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        opts = self.model._meta
        if not request.REQUEST.has_key("_change"):
            if request.REQUEST.has_key("_report"):
                body = Feature.getReport()
                resp = HttpResponse(body, mimetype='application/pdf')
                resp['Content-Disposition'] = 'attachment; filename=features_report.pdf'
                return resp
            else:
                feature = Feature.objects.get(id=object_id)
                context = {
                    'feature': feature,
                    'title': _('Feature: %s') % force_unicode(feature.name),
                    'opts': opts,
                    'object_id': object_id,
                    'is_popup': request.REQUEST.has_key('_popup'),
                    'app_label': opts.app_label,
                    }
                return render_to_response('admin/fur/feature/view.html',
                                          context,
                                          context_instance=RequestContext(request))
        return super(FeatureAdmin, self).change_view(request, object_id,
            form_url, extra_context=None)


class GlossaryAdmin(admin.ModelAdmin):
    fields = ['term','definition']

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_report'] = True
        return super(GlossaryAdmin, self).changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        opts = self.model._meta
        if not request.REQUEST.has_key("_change"):
            if request.REQUEST.has_key("_report"):
                body = Glossary.getReport()
                resp = HttpResponse(body, mimetype='application/pdf')
                resp['Content-Disposition'] = 'attachment; filename=glossary_report.pdf'
                return resp
            else:
                glossary = Glossary.objects.get(id=object_id)
                context = {
                    'glossary': glossary,
                    'title': _('Glossary: %s') % force_unicode(glossary.term),
                    'opts': opts,
                    'object_id': object_id,
                    'is_popup': request.REQUEST.has_key('_popup'),
                    'app_label': opts.app_label,
                    }
                return render_to_response('admin/fur/glossary/view.html',
                                          context,
                                          context_instance=RequestContext(request))
        return super(GlossaryAdmin, self).change_view(request, object_id,
            form_url, extra_context=None)


class ProjectAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'product',]
    filter_horizontal = ("product",)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        opts = self.model._meta
        if not request.REQUEST.has_key("_change"):
            if request.REQUEST.has_key("_zipreport"):
                project = Project.objects.get(id=object_id)
                #use case
                usecase = UseCase.getReport(Product)
                usecaseTemp = NamedTemporaryFile()
                usecaseTemp.close()
                usecaseTemp = codecs.open(usecaseTemp.name,'wb')
                usecaseTemp.write(usecase)
                usecaseTemp.close()

                #Feature
                features = Feature.getReport(Project.objects.get(id=object_id))
                featuresTemp = NamedTemporaryFile()
                featuresTemp.close()
                featuresTemp = codecs.open(featuresTemp.name,'wb')
                featuresTemp.write(features)
                featuresTemp.close()

                #Glossary
                glossary = Glossary.getReport(Project.objects.get(id=object_id))
                glossaryTemp = NamedTemporaryFile()
                glossaryTemp.close()
                glossaryTemp = codecs.open(glossaryTemp.name,'wb')
                glossaryTemp.write(glossary)
                glossaryTemp.close()

                #Test Case
                #testCase = TestCase.getReport(Product.objects.get(id=object_id))
               # testCaseTemp = NamedTemporaryFile()
               # testCaseTemp.close()
               # testCaseTemp = codecs.open(testCaseTemp.name,'wb')
               #testCaseTemp.write(testCase)
                #testCaseTemp.close()


                #User story
                #userStory = UserStory.getReport(Product.objects.get(id=object_id))
                #userStoryTemp = NamedTemporaryFile()
                #userStoryTemp.close()
                #userStoryTemp = codecs.open(userStoryTemp.name,'wb')
                #userStoryTemp.write(userStory)
                #userStoryTemp.close()


                # Folder name in ZIP archive which contains the above files
                # E.g [thearchive.zip]/somefiles/file2.txt
                # FIXME: Set this to something better
                zip_subdir = product.name.replace(" ", "_")+"_artifacs"
                zip_filename = "%s.zip" % zip_subdir

                # Open StringIO to grab in-memory ZIP contents
                s = StringIO.StringIO()

                # The zip compressor
                zf = zipfile.ZipFile(s, "w")

                # Calculate path for file in zip
                usecase_zip_path = os.path.join(zip_subdir, project.name+ "_usecase_report.pdf")
                feature_zip_path = os.path.join(zip_subdir, project.name+ "_features_report.pdf")
                glossary_zip_path = os.path.join(zip_subdir, project.name+ "_glossary_report.pdf")
                testCase_zip_path = os.path.join(zip_subdir, project.name+ "_testCase_report.pdf")
                userStory_zip_path = os.path.join(zip_subdir, project.name+ "_userStory_report.pdf")

                # Add file, at correct path
                zf.write(usecaseTemp.name, usecase_zip_path)
                zf.write(featuresTemp.name, feature_zip_path)
                zf.write(glossaryTemp.name, glossary_zip_path)
                #zf.write(testCaseTemp.name, testCase_zip_path)
                #zf.write(userStoryTemp.name, userStory_zip_path)

                # Must close zip for all contents to be written
                zf.close()

                # Grab ZIP file from in-memory, make response with correct MIME-type
                resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
                # ..and correct content-disposition
                resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
                return resp
            else:
                project = Project.objects.get(id=object_id)
                context = {
                    'project': project,
                    'title': _('Project: %s') % force_unicode(project.name),
                    'opts': opts,
                    'object_id': object_id,
                    'is_popup': request.REQUEST.has_key('_popup'),
                    'app_label': opts.app_label,
                    }
                return render_to_response('admin/fur/project/view.html',
                                          context,
                                          context_instance=RequestContext(request))
        return super(Project, self).change_view(request, object_id,
            form_url, extra_context=None)

admin.site.register(Product, ProductAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Glossary, GlossaryAdmin)
admin.site.register(BindingTime)
admin.site.register(Project, ProjectAdmin)