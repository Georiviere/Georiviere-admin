from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from paperclip.models import FileType as BaseFileType, Attachment as BaseAttachment
from geotrek.authent.models import StructureOrNoneRelated
from geotrek.common.mixins.models import AddPropertyMixin


class FileType(StructureOrNoneRelated, BaseFileType):
    class Meta(BaseFileType.Meta):
        pass


class Attachment(BaseAttachment):
    pass


class DataSource(StructureOrNoneRelated):

    name = models.CharField(verbose_name=_("Name"), max_length=50)

    class Meta:
        verbose_name = _("Data source")
        verbose_name_plural = _("Data sources")
        ordering = ['name']

    def __str__(self):
        if self.structure:
            return "{} ({})".format(self.name, self.structure.name)
        return self.name


class AddPropertyBufferMixin(AddPropertyMixin):
    """Add function to test if it is in a buffer"""

    @classmethod
    def within_buffer(cls, topology):
        area = topology.geom.buffer(settings.BASE_INTERSECTION_MARGIN)
        qs = cls.objects.filter(geom__intersects=area)
        return qs
