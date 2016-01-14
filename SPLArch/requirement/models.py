from django.db import models

from django.contrib.auth.models import *
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from SPLArch.architecture.util import render_to_latex
from SPLArch.architecture.models import Feature


STATUS_REQUIREMENT_CHOICES = (
    ('proposed', 'Proposed'),
    ('approved', 'Approved'),
    ('implemented', 'Implemented'),
    ('verified', 'Verified'),
    ('deferred', 'Deferred'),
    ('deleted', 'Deleted'),
    ('rejected', 'Rejected'),
)

PRIORITY = (
    ('no-priority', 'No Priority'),
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('very-high', 'Very High'),
    ('Urgent', 'Urgent'),
)

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




