"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from models import Category


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class BaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        p = User.objects.create_user('admin',
                                        'admin@example.com',
                                        'admin')
        p.is_staff = True
        p.is_active = True
        p.is_superuser = True
        p.save()
        p = Category(name='Jobs')
        p.save()


class StatsViewTest(BaseTest):
    def test_stats(self):
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 302)

        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)

        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jobs', status_code=200)
