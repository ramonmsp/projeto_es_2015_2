"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.test import TestCase
from SPLArch.scoping.models import  *


class LoginTestCase(TestCase):

    def test_status(self):
        c = Client()
        response = c.post('/admin/login/', {'username': 'admin', 'password': 'adin'})
        self.assertEqual(response.status_code,  200)
        print response.status_code


class ProductTestCase(TestCase):

    def test_response(self):
        c = Client()
        response = c.post('/admin/scoping/product/')
        self.assertEqual(response.status_code,  200)

        response = c.post('/admin/scoping/product/add/')
        self.assertEqual(response.status_code,  200)

        response = c.post('/admin/scoping/product/', {'pk' : 1})
        self.assertEqual(response.status_code,  200)

class ProjectTestCase(TestCase):

    def test_response(self):
        c = Client()
        response = c.post('/admin/scoping/project/')
        self.assertEqual(response.status_code,  200)

        response = c.post('/admin/scoping/project/',  {'pk' : 1})
        self.assertEqual(response.status_code,  200)

        response = c.post('/admin/scoping/project/add/')
        self.assertEqual(response.status_code,  200)

class GlossaryTestCase(TestCase):

    def test_response(self):
        c = Client()
        response = c.post('/admin/scoping/glossary/')
        self.assertEqual(response.status_code,  200)

        response = c.post('/admin/scoping/glossary/',  {'pk' : 1})
        self.assertEqual(response.status_code,  200)

        response = c.post('/admin/scoping/glossary/add/')
        self.assertEqual(response.status_code,  200)

class FeatureTestCase(TestCase):

    def test_response(self):
        c = Client()
        response = c.post('/admin/scoping/feature/')
        self.assertEqual(response.status_code,  200)

        response = c.post('/admin/scoping/feature/',  {'pk' : 1})
        self.assertEqual(response.status_code,  200)

        response = c.post('/admin/scoping/feature/add/')
        self.assertEqual(response.status_code,  200)

class BindingTimeTestCase(TestCase):

    def test_response(self):
        c = Client()
        response = c.post('/admin/scoping/bindingtime/')
        self.assertEqual(response.status_code,  200)

        response = c.post('/admin/scoping/bindingtime/',  {'pk' : 1})
        self.assertEqual(response.status_code,  200)

        response = c.post('/admin/scoping/bindingtime/add/')
        self.assertEqual(response.status_code,  200)


