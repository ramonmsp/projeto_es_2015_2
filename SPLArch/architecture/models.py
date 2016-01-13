from django.db import models
from django.contrib.auth.models import *
from mptt.models import MPTTModel, TreeForeignKey
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from SPLArch.architecture.util import render_to_latex

STATUS_REQUIREMENT_CHOICES = (
    ('proposed', 'Proposed'),
    ('approved', 'Approved'),
    ('implemented', 'Implemented'),
    ('verified', 'Verified'),
    ('deferred', 'Deferred'),
    ('deleted', 'Deleted'),
    ('rejected', 'Rejected'),
)

VARIABILITY_CHOICES = (
    ('mandatory', 'Mandatory'),
    ('optional', 'Optional'),
    ('alternative', 'Alternative')
)
TYPE_CHOICES = (
    ('abstract', 'Abstract'),
    ('concrete', 'Concrete')
)


PRIORITY = (
    ('no-priority', 'No Priority'),
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('very-high', 'Very High'),
    ('Urgent', 'Urgent'),
)


class Feature(MPTTModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    configuration = models.CharField(max_length=200)

    variability = models.CharField(max_length=20, choices=VARIABILITY_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    binding_time = models.ForeignKey('BindingTime')

    parent  = TreeForeignKey('self', blank=True, null=True, related_name='children')
    requires = models.ManyToManyField("self", blank=True, symmetrical=False,
                                      related_name='requires_features')
    excludes = models.ManyToManyField("self", blank=True, symmetrical=False,
                                      related_name='excludes_features')
    glossary = models.ManyToManyField('Glossary', blank=True)

    def __unicode__(self):
        return "#" + str(self.id) + " "  + self.name
    class MPTTMeta:
        order_insertion_by = ['name']
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    @staticmethod
    def getReport(product=None):
        if(product):
            mycontext = {'features': product.features.all,
                         'product_name': product.name,
                   'autoescape': False}
        else:
            mycontext = {'features': Feature.objects.all,
                         'product_name': "All products",
                    'autoescape': False}
        return render_to_latex("admin/fur/feature/report_features.tex",mycontext)

class RequirementType(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name


class Requirement(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    observations = models.TextField(blank=True)
    status_requirement_choices = models.CharField( max_length=200, choices=STATUS_REQUIREMENT_CHOICES, verbose_name='Status')
    requirement_type =models.ForeignKey('RequirementType')
    feature = models.ManyToManyField(Feature)
    priority = models.CharField(max_length=20, choices=PRIORITY)

    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    features = models.ManyToManyField('Feature', blank=True, symmetrical=False)

    def __unicode__(self):
        return self.name
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

class References(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

class DDSA(models.Model):
    description = models.CharField(max_length=100)
    references = models.ManyToManyField('References')
    technology = models.ManyToManyField('Technology')

    def __unicode__(self):
        return self.description

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

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    product = models.ManyToManyField(Product)

    def __unicode__(self):
        return self.name
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

class Meta:
       app_label = 'Tasks'

class BindingTime(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Feature binding time Item'
        verbose_name_plural = 'Feature binding times'

    def __unicode__(self):
        return self.name

class Glossary(models.Model):
    term = models.CharField(max_length=200)
    definition = models.TextField(max_length=200)

    class Meta:
        verbose_name = 'Glossary Item'
        verbose_name_plural = 'Glossary'
    def __unicode__(self):
        return self.term
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))
    @staticmethod
    def getReport(product=None):
        if(product):
            mycontext = {'glossary': Glossary.objects.filter(feature__in=product.features.all).distinct(),
                         'product_name': product.name,
                   'autoescape': False}
        else:
            mycontext = {'glossary': Glossary.objects.all,
                         'product_name': "All products",
                    'autoescape': False}

        return render_to_latex("admin/fur/glossary/report_glossary.tex",mycontext)

class UseCase(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    precondition = models.TextField(max_length=200, blank=True,verbose_name="Pre-condition")
    feature = models.ManyToManyField(Feature)
    mainSteps = models.ManyToManyField('MainSteps', blank=True, symmetrical=False, related_name='mainsteps_funcspec')
    owner = models.ManyToManyField(User, blank=False, symmetrical=False, related_name='owner_funcspec')
    alternativeSteps = models.ManyToManyField('AlternativeSteps', blank=True, symmetrical=False, related_name='alternativesteps_funcspec')

    def __unicode__(self):
        return self.title
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    @staticmethod
    def getReport(product=None):
        if(product):
            mycontext = {'usecases': UseCase.objects.filter(feature__in=product.features.all),
                         'product_name': product.name,
                   'autoescape': False}
        else:
            mycontext = {'usecases': UseCase.objects.all,
                         'product_name': "All products",
                    'autoescape': False}

        return render_to_latex("admin/fur/usecase/report_usecase.tex",mycontext)

class MainSteps(models.Model):    
    use_case = models.ForeignKey(UseCase)
    user_action = models.TextField()
    system_response = models.TextField()
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))
    def __unicode__(self):
        return "Main Step"

class AlternativeSteps(models.Model):    
    use_case = models.ForeignKey(UseCase)
    user_action = models.TextField()
    system_response = models.TextField()
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))
    def __unicode__(self):
        return "Alternative Step"

class Architecture(models.Model):
    name = models.CharField(max_length=200)
    description= models.TextField(max_length=500)
    references = models.ManyToManyField('References', blank=True, symmetrical=False, related_name='mainsteps_funcspec')
















'''
class TestCase(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=False)
    use_case = models.ForeignKey(UseCase)
    expected_result = models.TextField(blank=False)
    steps = models.ManyToManyField('TestSteps', blank=True, symmetrical=False)


    def __unicode__(self):
        return self.title
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))
    @staticmethod
    def getReport(product=None):
        if(product):
            mycontext = {'testCases': TestCase.objects.filter(use_case__in=UseCase.objects.filter(feature__in=product.features.all)).distinct(),
                         'product_name': product.name,
                   'autoescape': False}
        else:
            mycontext = {'testCases': TestCase.objects.all,
                         'product_name': "All products",
                    'autoescape': False}

        return render_to_latex("admin/fur/testcase/report_testcase.tex",mycontext)

class TestSteps(models.Model):
    test_case = models.ForeignKey(TestCase)
    description = models.TextField(blank=False)
    def __unicode__(self):
        return self.description
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


    STATUS_CHOICES = (('pass', 'Passed'),
                    ('failed', 'Failed'))
class TestExecution(models.Model):
    test_case = models.ForeignKey(TestCase)
    result = models.CharField(max_length=20, choices=STATUS_CHOICES)
    def __unicode__(self):
        return "Test execution " + str(self.id)
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

class UserStory(models.Model):
    name = models.CharField(max_length=200)
    features = models.ManyToManyField(Feature)
    as_a = models.CharField(max_length=200)
    i_want = models.TextField()
    so_that = models.TextField()
    constraints = models.ManyToManyField('Constraint', blank=True, symmetrical=False,
                                      related_name='constraints_userstory')
    def __unicode__(self):
        return self.name

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))
    class Meta:
        verbose_name = 'User story'
        verbose_name_plural = 'User stories'
    @staticmethod
    def getReport(product=None):
        if(product):
            mycontext = {'userStories': UserStory.objects.filter(features__in=product.features.all).distinct(),
                         'product_name': product.name,
                   'autoescape': False}
        else:
            mycontext = {'userStories': UserStory.objects.all,
                         'product_name': "All products",
                    'autoescape': False}

        return render_to_latex("admin/fur/userstory/report_userstory.tex",mycontext)

class Constraint(models.Model):
    user_story = models.ForeignKey(UserStory)
    restriction_n = models.TextField()
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

class AcceptanceTest(models.Model):
    name = models.CharField(max_length=200)
    user_story = models.ForeignKey(UserStory)
    given = models.TextField()
    when = models.TextField()
    then = models.TextField()
    def __unicode__(self):
        return self.name

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

class AcceptanceTestExecution(models.Model):
    acceptance_test = models.ForeignKey(AcceptanceTest)
    date = date =  models.DateField()
    result = models.CharField(max_length=20, choices=STATUS_CHOICES)
    observation = models.TextField()

    def __unicode__(self):
        return str(self.date)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

class Note(models.Model):
    title = models.CharField(max_length=200)
    date = date =  models.DateField()
    note = models.TextField()
    result = models.CharField(max_length=20, choices=STATUS_CHOICES)
    def __unicode__(self):
        return self.title
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))
'''