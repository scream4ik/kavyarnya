# -*- coding:utf-8 -*-
from django.db import models


class Profile(models.Model):
    name = models.CharField('Name', max_length=20)
    surname = models.CharField('Surname', max_length=20)
    birthday = models.DateField('Date of birth')
    bio = models.TextField('Bio')
    email = models.EmailField('E-mail')
    jabber = models.EmailField('Jabber', blank=True)
    skype = models.CharField('Skype', max_length=20, blank=True)
    other_contacts = models.TextField('Other contacts', blank=True)

    def __unicode__(self):
        return self.name
