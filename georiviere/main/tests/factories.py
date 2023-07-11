import factory

from georiviere.main.models import Attachment, DataSource, FileType

from geotrek.authent.tests.factories import UserFactory
from geotrek.common.utils.testdata import get_dummy_uploaded_image


class DataSourceFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'stream-%d' % n)

    class Meta:
        model = DataSource


class FileTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FileType

    type = factory.Sequence(lambda n: f'Type {n}')


class AttachmentFactory(factory.django.DjangoModelFactory):
    """
    Create an attachment. You must provide an 'obj' keywords,
    the object (saved in db) to which the attachment will be bound.
    """

    class Meta:
        model = Attachment

    attachment_file = get_dummy_uploaded_image()
    filetype = factory.SubFactory(FileTypeFactory)

    creator = factory.SubFactory(UserFactory)
    title = factory.Sequence("Title {0}".format)
    legend = factory.Sequence("Legend {0}".format)
