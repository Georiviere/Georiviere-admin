import logging

from django.conf import settings
from django.contrib.gis.db import models

from django.utils.translation import gettext_lazy as _

from geotrek.authent.models import StructureOrNoneRelated, StructureRelated
from geotrek.common.mixins import TimeStampedModelMixin

from mapentity.models import MapEntityMixin

from georiviere.description.models import Morphology, Status, Usage
from georiviere.knowledge.models import Knowledge
from georiviere.main.models import AddPropertyBufferMixin
from georiviere.observations.models import Station
from georiviere.proceeding.models import Proceeding
from georiviere.river.models import Stream
from georiviere.studies.models import Study

logger = logging.getLogger(__name__)


class POICategory(TimeStampedModelMixin, StructureOrNoneRelated):
    label = models.CharField(max_length=128, verbose_name=_("Label"))

    class Meta:
        verbose_name = _("POI Category")
        verbose_name_plural = _("POI Categories")
        ordering = ['label']
        unique_together = (
            ('label', 'structure'),
        )

    def __str__(self):
        if self.structure:
            return f'{self.label} ({self.structure})'
        return self.label


class POIType(TimeStampedModelMixin, StructureOrNoneRelated):
    label = models.CharField(verbose_name=_("Name"), max_length=128)
    category = models.ForeignKey(POICategory, related_name='types', on_delete=models.PROTECT,
                                 verbose_name=_("Category"))
    pictogram = models.FileField(verbose_name=_("Pictogram"), upload_to=settings.UPLOAD_DIR,
                                 max_length=512, null=True)

    class Meta:
        verbose_name = _("POI type")
        verbose_name_plural = _("POI types")
        ordering = ['label']
        unique_together = (
            ('label', 'structure', 'category'),
        )

    def __str__(self):
        if self.structure:
            return f'{self.label} ({self.structure})'
        return self.label


class POI(AddPropertyBufferMixin, TimeStampedModelMixin, StructureRelated, MapEntityMixin):
    name = models.CharField(max_length=128, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"), blank=True, help_text=_("History, details,  ..."))
    geom = models.PointField(srid=settings.SRID, spatial_index=True)
    type = models.ForeignKey(POIType, related_name='pois',
                             verbose_name=_("Type"),
                             on_delete=models.PROTECT)
    portals = models.ManyToManyField('portal.Portal', verbose_name=_("Portals"), related_name='pois',
                                     blank=True, )

    class Meta:
        verbose_name = _("POI")
        verbose_name_plural = _("POIs")
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def name_display(self):
        return '<a data-pk="%s" href="%s" title="%s" >%s</a>' % (self.pk,
                                                                 self.get_detail_url(),
                                                                 self,
                                                                 self)

    @property
    def type_display(self):
        return f'{self.type.label} - {self.type.category.label}'

    def is_public(self):
        return self.portals.exists()


POI.add_property('streams', Stream.within_buffer, _("Stream"))
POI.add_property('status', Status.within_buffer, _("Status"))
POI.add_property('morphologies', Morphology.within_buffer, _("Morphologies"))
POI.add_property('usages', Usage.within_buffer, _("Usages"))
POI.add_property('stations', Station.within_buffer, _("Station"))
POI.add_property('studies', Study.within_buffer, _("Study"))
POI.add_property('proceedings', Proceeding.within_buffer, _("Proceeding"))
POI.add_property('knowledges', Knowledge.within_buffer, _("Knowledge"))

Stream.add_property('pois', POI.within_buffer, _("POIs"))
POI.add_property('pois', POI.within_buffer, _("POIs"))
Status.add_property('pois', POI.within_buffer, _("POIs"))
Morphology.add_property('pois', POI.within_buffer, _("POIs"))
Usage.add_property('pois', POI.within_buffer, _("POIs"))
Station.add_property('pois', POI.within_buffer, _("POIs"))
Study.add_property('pois', POI.within_buffer, _("POIs"))
Proceeding.add_property('pois', POI.within_buffer, _("POIs"))
Knowledge.add_property('pois', POI.within_buffer, _("POIs"))
