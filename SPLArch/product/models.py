from django.db import models
from SPLArch.product.mptt.models import MPTTModel, TreeForeignKey

       
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    features = models.ManyToManyField('Feature', blank=True, symmetrical=False)


    def __unicode__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    product = models.ManyToManyField(Product) 

    def __unicode__(self):
        return self.name

# Features Simulado
class Feature(MPTTModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    configuration = models.CharField(max_length=200)

    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')


    def __unicode__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']