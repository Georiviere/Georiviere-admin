from django.conf import settings
from paperclip.models import FileType as BaseFileType, Attachment as BaseAttachment
from geotrek.authent.models import StructureOrNoneRelated
from geotrek.common.mixins import AddPropertyMixin


class FileType(StructureOrNoneRelated, BaseFileType):
    class Meta(BaseFileType.Meta):
        pass


class Attachment(BaseAttachment):
    pass


class AddPropertyBufferMixin(AddPropertyMixin):
    """Add function to test if it is in a buffer"""

    @classmethod
    def within_buffer(cls, topology):
        area = topology.geom.buffer(settings.BASE_INTERSECTION_MARGIN)
        qs = cls.objects.filter(geom__intersects=area)
        return qs
