import factory

from geotrek.common.utils.testdata import get_dummy_uploaded_image

from georiviere.flatpages import models
from georiviere.portal.tests.factories import PortalFactory


class FlatPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FlatPage

    title = factory.Sequence(lambda n: "Title %s" % n)
    order = factory.Sequence(lambda n: n)

    @factory.post_generation
    def portals(obj, create, extracted=None, **kwargs):
        if create:
            if extracted:
                obj.portals.set(extracted)
            else:
                obj.portals.add(PortalFactory.create())


class FlatPagePictureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FlatPagePicture

    picture = get_dummy_uploaded_image('level.png')
    flatpage = factory.SubFactory(FlatPageFactory)
