"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from models import Profile, HttpRequest


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
