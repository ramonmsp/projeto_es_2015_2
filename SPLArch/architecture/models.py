from django.db import models
from django.contrib.auth.models import *
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from SPLArch.architecture.util import render_to_latex
from SPLArch.scoping.models import *
from SPLArch.requirement.models import *



class References(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

    @staticmethod
    def getReport(product=None):
        if(product):
            mycontext = {'references': References.objects.all,
                         'product_name': product.name,
                         'autoescape': False}
        else:
            mycontext = {'references': References.objects.all,
                         'product_name': "All products",
                         'autoescape': False}

        return render_to_latex("admin/fur/references/report_references.tex",mycontext)


class DDSA(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    references = models.ManyToManyField('References')
    technology = models.ManyToManyField('Technology')
    scenarios = models.ManyToManyField('AddScenarios')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name="DSSA"
        verbose_name_plural="DSSAs"

class Scenarios(models.Model):
    name = models.CharField(max_length=100)
    stimulus = models.TextField(blank=True)
    response = models.TextField(blank=True)
    strategy = models.TextField(blank=True)
    feature = models.ManyToManyField(Feature)
    nf_requirement = models.ManyToManyField(Requirement)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name="Scenario Detail"

class AddScenarios(models.Model):
    name = models.CharField(max_length=100)
    nf_requirement = models.ManyToManyField(Requirement)
    scenario = models.ManyToManyField(Scenarios)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name="Quality Scenario"
        verbose_name_plural="Quality Scenarios"

class Technology(models.Model):
    api = models.ManyToManyField('API', verbose_name="API")
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name="Technology"
        verbose_name_plural="Technologies"

class API(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=100)
    specification = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name="API"
        verbose_name_plural="APIs"

    @staticmethod
    def getReport(product=None):
        if(product):
            mycontext = {'api': API.objects.all,
                         'product_name': product.name,
                   'autoescape': False}
        else:
            mycontext = {'api': API.objects.all,
                         'product_name': "All products",
                    'autoescape': False}

        return render_to_latex("admin/fur/api/report_api.tex",mycontext)

class Meta:
       app_label = 'Tasks'


class Architecture(models.Model):
    name = models.CharField(max_length=200)
    description= models.TextField(max_length=500)
    references = models.ManyToManyField('References', blank=True, symmetrical=False, related_name='mainsteps_funcspec')

