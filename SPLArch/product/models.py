from django.db import models

       
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    product = models.ManyToManyField(Product)

    def __unicode__(self):
        return self.name
