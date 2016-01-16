from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.test import TestCase
from SPLArch.scoping.models import  *
from SPLArch.architecture.models import *

from django.test import TestCase

class ReferencesTestCase(TestCase):

    def setUp(self):
        self.references1 = ReferencesTestCase.objects.create(name='')
        self.references1.save()
        self.model = self.references1

    def test_response(self):
        url = reverse("admin:%s_%s_add" % (self.model._meta.app_label, self.model._meta.module_name))
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_change" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_delete" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_history" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_changelist" % (self.model._meta.app_label, self.model._meta.module_name))
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

class ReferencesTestCase(TestCase):

    def setUp(self):
        self.references_test1 = References.objects.create(title='', author='', description='')
        self.references_test1.save()
        self.model = self.references_test1

    def test_response(self):
        url = reverse("admin:%s_%s_add" % (self.model._meta.app_label, self.model._meta.module_name))
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_change" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_delete" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_history" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_changelist" % (self.model._meta.app_label, self.model._meta.module_name))
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

class DDSATestCase(TestCase):

    def setUp(self):
        self.ddsa1 = DDSA.objects.create(name='')
        self.ddsa1.save()
        self.model = self.ddsa1

    def test_response(self):
        url = reverse("admin:%s_%s_add" % (self.model._meta.app_label, self.model._meta.module_name))
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_change" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_delete" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_history" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_changelist" % (self.model._meta.app_label, self.model._meta.module_name))
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

class ScenariosTestCase(TestCase):
    def setUp(self):
        self.scenarios1 = Scenarios.objects.create(name='')
        self.scenarios1.save()
        self.model = self.scenarios1

    def test_response(self):
        url = reverse("admin:%s_%s_add" % (self.model._meta.app_label, self.model._meta.module_name))
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_change" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_delete" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_history" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_changelist" % (self.model._meta.app_label, self.model._meta.module_name))
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

class AddScenariosTestCase(TestCase):
    def setUp(self):
            self.add_scenarios1 = AddScenarios.objects.create(name='')
            self.add_scenarios1.save()
            self.model = self.add_scenarios1

    def test_response(self):
        url = reverse("admin:%s_%s_add" % (self.model._meta.app_label, self.model._meta.module_name))
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_change" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_delete" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_history" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_changelist" % (self.model._meta.app_label, self.model._meta.module_name))
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

class APITestCase(TestCase):
    def setUp(self):
            self.api1 = API.objects.create(name='')
            self.api1.save()
            self.model = self.api1

    def test_response(self):
        url = reverse("admin:%s_%s_add" % (self.model._meta.app_label, self.model._meta.module_name))
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_change" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_delete" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_history" % (self.model._meta.app_label, self.model._meta.module_name), args=[self.model.id])
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

        url = reverse("admin:%s_%s_changelist" % (self.model._meta.app_label, self.model._meta.module_name))
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code,  200)

