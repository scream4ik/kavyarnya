# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from kavyarnya.utils import image_path
from sorl.thumbnail import ImageField

from datetime import datetime


ACTION = (
    ('add', 'Add'),
    ('edit', 'Edit'),
    ('delete', 'Delete'),
)


class Profile(models.Model):
    name = models.CharField('Name', max_length=20)
    surname = models.CharField('Surname', max_length=20)
    birthday = models.DateField('Date of birth')
    bio = models.TextField('Bio')
    email = models.EmailField('E-mail')
    jabber = models.EmailField('Jabber', blank=True)
    skype = models.CharField('Skype', max_length=20, blank=True)
    other_contacts = models.TextField('Other contacts', blank=True)
    photo = ImageField('Photo', upload_to=image_path, max_length=250, blank=True, null=True)

    def __unicode__(self):
        return self.name


class HttpRequest(models.Model):
    time = models.DateTimeField(default=datetime.now)
    url = models.CharField(max_length=250)

    class Meta:
        ordering = ('pk',)

    def __unicode__(self):
        return self.url


class Log(models.Model):
    action = models.CharField(max_length=10, choices=ACTION)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return str(self.pk)


@receiver(post_save, sender=Profile)
@receiver(post_save, sender=HttpRequest)
def add_or_edit(sender, instance, created, **kwargs):
    if created:
        p = Log(content_object=instance, action='add')
    else:
        p = Log(content_object=instance, action='edit')
    p.save()


@receiver(post_delete, sender=Profile)
@receiver(post_delete, sender=HttpRequest)
def delete(sender, instance, **kwargs):
    Log(content_object=instance, action='delete').save()
