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