from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):

    def handle(self, *args, **options):
        result = {}

        for ct in ContentType.objects.all():
            try:
                m = ct.model_class()
                model_name = '%s.%s' % (m.__module__, m.__name__)
                result[model_name] = m.objects.count()
            except AttributeError:
                pass

        for k, v in result.items():
            row = '%s\t%d' % (k, v)
            self.stdout.write('%s\n' % row)

            prefix = 'error:'
            self.stderr.write('%s %s\n' % (prefix, row))
