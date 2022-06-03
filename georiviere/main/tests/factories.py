import factory

from georiviere.main.models import DataSource


class DataSourceFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'stream-%d' % n)

    class Meta:
        model = DataSource
