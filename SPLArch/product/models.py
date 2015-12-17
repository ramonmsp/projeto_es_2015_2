from django.db import models
from SPLArch.product.mptt.models import MPTTModel, TreeForeignKey

       
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    features = models.ManyToManyField('Feature', blank=True, symmetrical=False)


    def __unicode__(self):
        return self.name
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    product = models.ManyToManyField(Product)

    def __unicode__(self):
        return self.name

<<<<<<< HEAD
class UseCase(models.Model):
   description = models.TextField(blank=True)
   precondition = models.TextField(blank=True)
   title = models.CharField(max_length=200)

   def __unicode__(self):
        return self.name

class MainSteps(models.Model):
    use_case = models.ForeignKey(UseCase)
    system_response = models.TextField(blank=True)
    user_action = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class AlternativeSteps(models.Model):
    use_case = models.ForeignKey(UseCase)
    system_response = models.TextField(blank=True)
    user_action = models.TextField(blank=True)

    def __unicode__(self):
        return self.name
=======
# Features Simulado
class Feature(MPTTModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    configuration = models.CharField(max_length=200)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return "#" + " "  + self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))
>>>>>>> d124d99b1f3daab7990bb3a42f987a8c16636b29
