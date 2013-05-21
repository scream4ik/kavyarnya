"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.management import call_command
from django.contrib.contenttypes.models import ContentType

from models import Profile, HttpRequest, Log

import sys
import StringIO


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
        p = Profile(name='Slava',
                    surname='Kyrachevsky',
                    birthday='1990-06-02',
                    bio='My bio',
                    email='slava.deb@gmail.com')
        p.save()


class IndexViewTest(BaseTest):
    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class ProfileEditViewTest(BaseTest):
    def test_profile_edit(self):
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 302)
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        response = self.client.post(
                        reverse('profile_edit'),
                        {
                            'name': 'Slava',
                            'surname': 'Kyrachevsky',
                            'birthday': '1990-06-02',
                            'bio': 'My new bio',
                            'email': 'slava.deb@gmail.com'
                        })
        self.assertEqual(response.status_code, 302)

        data = Profile.objects.all()[0]

        self.assertEquals(data.name, 'Slava')
        self.assertEquals(data.surname, 'Kyrachevsky')
        self.assertEquals(data.birthday.strftime('%Y-%m-%d'), '1990-06-02')
        self.assertEquals(data.bio, 'My new bio')
        self.assertEquals(data.email, 'slava.deb@gmail.com')


class CheckTextTest(BaseTest):
    def test_text(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'My bio', status_code=200)


class MiddlewareTest(BaseTest):
    def test_middleware(self):
        self.client.get(reverse('index'))

        req = HttpRequest.objects.get(url='/')
        self.assertNotEquals(req, None)
        self.assertEquals(req.priority, 0)


class AdminEditLinkTest(BaseTest):
    def test_admin_edit_link(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response,
                                '<a href="/admin/core/profile/1/">admin</a>')

        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                                '<a href="/admin/core/profile/1/">admin</a>')


class CommandsTestCase(BaseTest):
    def test_show_models(self):
        old_stderr = sys.stderr
        sys.stderr = StringIO.StringIO()
        call_command('show_models')
        self.assertTrue('core.models.HttpRequest' in sys.stderr.getvalue())
        sys.stderr = old_stderr


class LogTestCase(BaseTest):
    def test_obj_create(self):
        profile = Profile.objects.all()[0]
        log = Log.objects.all().order_by('-pk')[0]

        self.assertEquals(log.action, 'add')
        self.assertEquals(log.object_id, profile.pk)
        self.assertEquals(log.content_type,
                            ContentType.objects.get(model='profile'))

    def test_obj_update(self):
        profile = Profile.objects.all()[0]
        profile.name = 'qwerty'
        profile.save()
        log = Log.objects.all().order_by('-pk')[0]

        self.assertEquals(log.action, 'edit')
        self.assertEquals(log.object_id, profile.pk)
        self.assertEquals(log.content_type,
                            ContentType.objects.get(model='profile'))

    def test_obj_delete(self):
        profile = Profile.objects.all()[0]
        pk = profile.pk
        profile.delete()
        log = Log.objects.all().order_by('-pk')[0]

        self.assertEquals(log.action, 'delete')
        self.assertEquals(log.object_id, pk)
        self.assertEquals(log.content_type,
                            ContentType.objects.get(model='profile'))


class HttpRequestViewTest(BaseTest):
    def test_http_request(self):
        self.client.get(reverse('index'))

        req = HttpRequest.objects.get(url='/')
        self.assertNotEquals(req, None)
        self.assertEquals(req.priority, 0)

        response = self.client.post(
                        reverse('http_request'),
                        {
                            'pr': 'increase',
                            'obj_pk': req.pk,
                        })
        self.assertEqual(response.status_code, 302)

        req = HttpRequest.objects.get(pk=req.pk)
        self.assertEquals(req.priority, 1)
