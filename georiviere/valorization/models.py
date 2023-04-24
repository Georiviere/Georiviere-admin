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


class POIMixin(AddPropertyBufferMixin, TimeStampedModelMixin, StructureRelated):
    name = models.CharField(max_length=128, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"), blank=True, help_text=_("History, details,  ..."))
    geom = models.PointField(srid=settings.SRID, spatial_index=True)

    class Meta:
        abstract = True
        unique_together = (
            ('name', 'structure'),
        )

    @property
    def name_display(self):
        return '<a data-pk="%s" href="%s" title="%s" >%s</a>' % (self.pk,
                                                                 self.get_detail_url(),
                                                                 self,
                                                                 self)


class POIKnowledge(POIMixin, MapEntityMixin):
    type = models.ForeignKey('POIKnowledgeType', related_name='pois', verbose_name=_("Type"), on_delete=models.PROTECT)
    portals = models.ManyToManyField('portal.Portal', verbose_name=_("Portals"), related_name='poi_knowledges',
                                     blank=True, )

    class Meta:
        verbose_name = _("POI knowledge")
        verbose_name_plural = _("POIs knowledge ")

    def __str__(self):
        return self.name


class POIKnowledgeType(TimeStampedModelMixin, StructureOrNoneRelated):
    label = models.CharField(verbose_name=_("Name"), max_length=128)

    class Meta:
        verbose_name = _("POI knowledge type")
        verbose_name_plural = _("POI knowledge types")
        ordering = ['label']
        unique_together = (
            ('label', 'structure'),
        )

    def __str__(self):
        return self.label


class POIAction(POIMixin, MapEntityMixin):
    type = models.ForeignKey('POIActionType', related_name='pois', verbose_name=_("Type"), on_delete=models.PROTECT)
    portals = models.ManyToManyField('portal.Portal', verbose_name=_("Portals"), related_name='poi_actions', blank=True)

    class Meta:
        verbose_name = _("POI action")
        verbose_name_plural = _("POIs action")

    def __str__(self):
        return self.name


class POIActionType(TimeStampedModelMixin, StructureOrNoneRelated):
    label = models.CharField(verbose_name=_("Name"), max_length=128)

    class Meta:
        verbose_name = _("POI action type")
        verbose_name_plural = _("POI action types")
        ordering = ['label']
        unique_together = (
            ('label', 'structure'),
        )

    def __str__(self):
        return self.label


POIKnowledge.add_property('streams', Stream.within_buffer, _("Stream"))
POIKnowledge.add_property('status', Status.within_buffer, _("Status"))
POIKnowledge.add_property('morphologies', Morphology.within_buffer, _("Morphologies"))
POIKnowledge.add_property('usages', Usage.within_buffer, _("Usages"))
POIKnowledge.add_property('stations', Station.within_buffer, _("Station"))
POIKnowledge.add_property('studies', Study.within_buffer, _("Study"))
POIKnowledge.add_property('proceedings', Proceeding.within_buffer, _("Proceeding"))
POIKnowledge.add_property('knowledges', Knowledge.within_buffer, _("Knowledge"))


POIAction.add_property('streams', Stream.within_buffer, _("Stream"))
POIAction.add_property('status', Status.within_buffer, _("Status"))
POIAction.add_property('morphologies', Morphology.within_buffer, _("Morphologies"))
POIAction.add_property('usages', Usage.within_buffer, _("Usages"))
POIAction.add_property('stations', Station.within_buffer, _("Station"))
POIAction.add_property('studies', Study.within_buffer, _("Study"))
POIAction.add_property('proceedings', Proceeding.within_buffer, _("Proceeding"))
POIAction.add_property('knowledges', Knowledge.within_buffer, _("Knowledge"))

Stream.add_property('pois_knowledge', POIKnowledge.within_buffer, _("POIs Knowledge"))
POIAction.add_property('pois_knowledge', POIKnowledge.within_buffer, _("POIs Knowledge"))
Status.add_property('pois_knowledge', POIKnowledge.within_buffer, _("POIs Knowledge"))
Morphology.add_property('pois_knowledge', POIKnowledge.within_buffer, _("POIs Knowledge"))
Usage.add_property('pois_knowledge', POIKnowledge.within_buffer, _("POIs Knowledge"))
Station.add_property('pois_knowledge', POIKnowledge.within_buffer, _("POIs Knowledge"))
Study.add_property('pois_knowledge', POIKnowledge.within_buffer, _("POIs Knowledge"))
Proceeding.add_property('pois_knowledge', POIKnowledge.within_buffer, _("POIs Knowledge"))
Knowledge.add_property('pois_knowledge', POIKnowledge.within_buffer, _("POIs Knowledge"))

Stream.add_property('pois_action', POIAction.within_buffer, _("POIs Action"))
POIKnowledge.add_property('pois_action', POIAction.within_buffer, _("POIs Action"))
Status.add_property('pois_action', POIAction.within_buffer, _("POIs Action"))
Morphology.add_property('pois_action', POIAction.within_buffer, _("POIs Action"))
Usage.add_property('pois_action', POIAction.within_buffer, _("POIs Action"))
Station.add_property('pois_action', POIAction.within_buffer, _("POIs Action"))
Study.add_property('pois_action', POIAction.within_buffer, _("POIs Action"))
Proceeding.add_property('pois_action', POIAction.within_buffer, _("POIs Action"))
Knowledge.add_property('pois_action', POIAction.within_buffer, _("POIs Action"))
