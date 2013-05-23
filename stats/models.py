from django.db import models

VISITOR_TYPE = (
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
)


class Category(models.Model):
    name = models.CharField('Name', max_length=20)

    def __unicode__(self):
        return self.name


class Place(models.Model):
    name = models.CharField('Name', max_length=20)
    category = models.ForeignKey(Category, verbose_name='Category', unique=True)

    def __unicode__(self):
        return self.name


class Visitor(models.Model):
    count = models.IntegerField('Count')
    type = models.CharField('Type', choices=VISITOR_TYPE, max_length=1)
    place = models.ForeignKey(Place, verbose_name='Place')

    def __unicode__(self):
        return str(self.count)
