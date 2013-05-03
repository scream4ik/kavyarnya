from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from optparse import make_option


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--tee-stderr',
            action='store_true',
            dest='tee',
            default=False,
            help='duplicate output to stderr'),

        make_option('--stderr-prefix',
            action="store",
            type="string",
            dest='prefix',
            default='error:',
            help='prefix for stderr output'),
    )

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

            if options.get('tee'):
                prefix = options.get('prefix')
                if prefix:
                    self.stderr.write('%s %s\n' % (prefix, row))
                else:
                    self.stderr.write('%s\n' % row)
