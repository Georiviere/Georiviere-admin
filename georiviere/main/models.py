from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from paperclip.models import FileType as BaseFileType, Attachment as BaseAttachment
from geotrek.authent.models import StructureOrNoneRelated
from geotrek.common.mixins import AddPropertyMixin


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
        qs = cls.objects.none()
        if not topology.geom:
            return qs
        area = topology.geom.buffer(settings.BASE_INTERSECTION_MARGIN)
        qs = cls.objects.filter(geom__intersects=area)
        return qs


class DistanceToSource(models.Model):
    distance = models.FloatField(verbose_name=_("Distance"), default=0)
    stream = models.ForeignKey('river.Stream', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _("Distance to source")
        verbose_name_plural = _("Distance to sources")
        unique_together = ('content_type', 'object_id', 'stream')
