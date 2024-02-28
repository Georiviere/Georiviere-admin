from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

import math
import os
from mapentity.helpers import is_file_uptodate, smart_urljoin, capture_map_image
from mapentity.registry import app_settings

from geotrek.authent.models import StructureRelated, StructureOrNoneRelated
from geotrek.common.mixins import TimeStampedModelMixin
from geotrek.zoning.mixins import ZoningPropertiesMixin
from mapentity.models import MapEntityMixin

from georiviere.main.models import AddPropertyBufferMixin
from georiviere.altimetry import AltimetryMixin
from georiviere.finances_administration.models import AdministrativeFile
from georiviere.functions import ClosestPoint
from georiviere.knowledge.models import Knowledge, FollowUp
from georiviere.main.models import DistanceToSource
from georiviere.observations.models import Station
from georiviere.proceeding.models import Proceeding
from georiviere.maintenance.models import Intervention
from georiviere.studies.models import Study
from georiviere.watershed.mixins import WatershedPropertiesMixin

from geotrek.sensitivity.models import SensitiveArea


class TopologyMixin(object):
    structure_verbose_name = _("Structure")

    def get_topology(self, topology_type):
        start_position = self.topology.start_position
        end_position = self.topology.end_position
        topologies = self.topology.stream.topologies.filter(
            Q(start_position__lte=start_position, end_position__gte=start_position) | Q(
                start_position__lte=end_position,
                end_position__gte=end_position),
            **{f'{topology_type}__isnull': False})
        final_topologies = [getattr(topology, topology_type) for topology in topologies]
        return final_topologies


class ClassificationWaterPolicy(StructureOrNoneRelated):
    label = models.CharField(max_length=128, verbose_name=_("Label"), )

    class Meta:
        verbose_name = _("Classification water policy")
        verbose_name_plural = _("Classification water policies")

    def __str__(self):
        return self.label


class Stream(AddPropertyBufferMixin, TimeStampedModelMixin, WatershedPropertiesMixin, ZoningPropertiesMixin,
             MapEntityMixin, AltimetryMixin, StructureRelated):
    """Model for stream"""

    class FlowChoices(models.IntegerChoices):
        """Choices for stream flow"""
        TBD = 0, _('To be defined')
        PERMANENT = 1, _('Permanent')
        TEMPORARY = 2, _('Temporary')

    name = models.CharField(max_length=100, default=_('Stream'), verbose_name=_("Name"))
    geom = models.LineStringField(srid=settings.SRID, spatial_index=True)
    description = models.TextField(verbose_name=_("Description"), blank=True)
    flow = models.IntegerField(
        choices=FlowChoices.choices,
        default=FlowChoices.TBD,
        blank=True,
        verbose_name=_("Flow"),
    )
    data_source = models.ForeignKey('main.DataSource', on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name='streams',
                                    verbose_name=_("Data source"))

    source_location = models.PointField(verbose_name=_("Source location"),
                                        srid=settings.SRID,
                                        blank=True, null=True)
    classification_water_policy = models.ForeignKey('ClassificationWaterPolicy',
                                                    on_delete=models.SET_NULL,
                                                    null=True, blank=True, related_name='streams',
                                                    verbose_name=_("Classification water policy"))
    portals = models.ManyToManyField('portal.Portal',
                                     blank=True, related_name='streams',
                                     verbose_name=_("Published portals"))

    capture_map_image_waitfor = '.other_object_enum_loaded'

    class Meta:
        verbose_name = _("Stream")
        verbose_name_plural = _("Streams")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for model_topology in self.model_topologies:
            setattr(self, model_topology._meta.model_name, self.get_topology(model_topology._meta.model_name))

    def __str__(self):
        return self.name

    def is_public(self):
        return self.portals.exists()

    def get_printcontext_with_other_objects(self, modelnames):
        maplayers = [
            settings.LEAFLET_CONFIG['TILES'][0][0],
        ]
        return {"maplayers": maplayers, "additional_objects": modelnames}

    def get_map_image_path_with_other_objects(self, modelnames):
        basefolder = os.path.join(settings.MEDIA_ROOT, 'maps')
        if not os.path.exists(basefolder):
            os.makedirs(basefolder)
        return os.path.join(basefolder, '%s-%s-%s.png' % (self._meta.model_name, self.pk, '-'.join(sorted(modelnames))))

    def prepare_map_image_with_other_objects(self, rooturl, properties):
        path = self.get_map_image_path_with_other_objects(properties)
        # Do nothing if image is up-to-date
        dates_to_check = [self.get_date_update()]
        for prop in properties:
            if getattr(self, prop):
                dates_to_check.append(getattr(self, prop).latest('date_update').get_date_update())
        if all([is_file_uptodate(path, date) for date in dates_to_check]):
            return False
        url = smart_urljoin(rooturl, self.get_detail_url())
        extent = self.get_map_image_extent(3857)
        length = max(extent[2] - extent[0], extent[3] - extent[1])
        hint_size = app_settings['MAP_CAPTURE_SIZE']
        length_per_tile = 256 * length / hint_size
        RADIUS = 6378137
        CIRCUM = 2 * math.pi * RADIUS
        zoom = round(math.log(CIRCUM / length_per_tile, 2))
        size = math.ceil(length * 1.1 * 256 * 2 ** zoom / CIRCUM)
        printcontext = self.get_printcontext_with_other_objects(properties)
        capture_map_image(url, path, size=size, waitfor=self.capture_map_image_waitfor, printcontext=printcontext)
        return True

    @property
    def areas_ordered_area_type(self):
        return sorted(self.areas, key=lambda x: x.area_type.name)

    @property
    def slug(self):
        return slugify(self.name) or str(self.pk)

    def save(self, *args, **kwargs):
        if not self.source_location:
            self.source_location = Point(self.geom[0])
        super().save(*args, **kwargs)

    @classmethod
    def get_create_label(cls):
        return _("Add a new stream")

    @property
    def name_display(self):
        return '<a data-pk="%s" href="%s" title="%s" >%s</a>' % (self.pk,
                                                                 self.get_detail_url(),
                                                                 self,
                                                                 self)

    def get_topology(self, value):
        topologies = self.topologies.filter(**{f'{value}__isnull': False})
        topologies = [getattr(topology, value) for topology in topologies]
        return topologies

    def get_map_image_extent(self, srid=settings.API_SRID):
        extent = list(super().get_map_image_extent(srid))
        if self.source_location:
            self.source_location.transform(srid)
            extent[0] = min(extent[0], self.source_location.x)
            extent[1] = min(extent[1], self.source_location.y)
            extent[2] = max(extent[2], self.source_location.x)
            extent[3] = max(extent[3], self.source_location.y)
        return extent

    def snap(self, point):
        """
        Returns the point snapped (i.e closest) to the path line geometry.
        """
        if not self.pk:
            raise ValueError("Cannot compute snap on unsaved stream")
        if point.srid != self.geom.srid:
            point.transform(self.geom.srid)
        return self._meta.model.objects.filter(pk=self.pk).annotate(
            closest_point=ClosestPoint('geom', point)).first().closest_point

    def distance_to_source(self, element):
        """Returns distance from element to stream source"""
        ct = ContentType.objects.get_for_model(element)
        try:
            return DistanceToSource.objects.get(stream=self, content_type=ct, object_id=element.pk).distance
        except DistanceToSource.DoesNotExist:
            return None


class Topology(models.Model):
    stream = models.ForeignKey(Stream, verbose_name=_("Stream"),
                               on_delete=models.CASCADE, related_name='topologies')
    start_position = models.FloatField(verbose_name=_("Start position"), db_index=True, default=0)
    end_position = models.FloatField(verbose_name=_("End position"), db_index=True, default=1)
    qualified = models.BooleanField(verbose_name=_("Qualified"), null=False, default=False)

    def __str__(self):
        if hasattr(self, 'status'):
            return _("Status {}").format(self.status)
        elif hasattr(self, 'morphology'):
            return _("Morphology {}").format(self.morphology)
        else:
            return _("Topology {}").format(self.pk)

    class Meta:
        verbose_name = _("Topology")
        verbose_name_plural = _("Topologies")
        # triggers = [
        #     pgtrigger.Trigger(
        #         name="update_topology_geom",
        #         operation=pgtrigger.Update | pgtrigger.Insert,
        #         when=pgtrigger.After,
        #         declare=[('stream_geom', 'geometry')],
        #         func="""
        #             SELECT r.geom FROM river_stream r WHERE NEW.stream_id = r.id INTO stream_geom;
        #             UPDATE description_morphology
        #             SET geom = ST_LINESUBSTRING(stream_geom, NEW.start_position, NEW.end_position)
        #             WHERE topology_id = NEW.id;
        #             UPDATE description_status
        #             SET geom = ST_LINESUBSTRING(stream_geom, NEW.start_position, NEW.end_position)
        #             WHERE topology_id = NEW.id;
        #             RETURN NEW;
        #         """
        #     )]


Study.add_property('stations', Station.within_buffer, _("Stations"))
Study.add_property('knowledges', Knowledge.within_buffer, _("Knowledge"))
Study.add_property('proceedings', Proceeding.within_buffer, _("Proceedings"))
Study.add_property('streams', Stream.within_buffer, _("Streams"))

Station.add_property('studies', Study.within_buffer, _("Studies"))
Station.add_property('knowledges', Knowledge.within_buffer, _("Knowledge"))
Station.add_property('proceedings', Proceeding.within_buffer, _("Proceedings"))
Station.add_property('streams', Stream.within_buffer, _("Streams"))

Knowledge.add_property('stations', Station.within_buffer, _("Stations"))
Knowledge.add_property('studies', Study.within_buffer, _("Studies"))
Knowledge.add_property('proceedings', Proceeding.within_buffer, _("Proceedings"))
Knowledge.add_property('streams', Stream.within_buffer, _("Streams"))

FollowUp.add_property('stations', Station.within_buffer, _("Stations"))
FollowUp.add_property('studies', Study.within_buffer, _("Studies"))
FollowUp.add_property('proceedings', Proceeding.within_buffer, _("Proceedings"))
FollowUp.add_property('streams', Stream.within_buffer, _("Streams"))

Proceeding.add_property('stations', Station.within_buffer, _("Stations"))
Proceeding.add_property('studies', Study.within_buffer, _("Studies"))
Proceeding.add_property('knowledges', Knowledge.within_buffer, _("Knowledges"))
Proceeding.add_property('streams', Stream.within_buffer, _("Streams"))

Stream.add_property('stations', Station.within_buffer, _("Stations"))
Stream.add_property('studies', Study.within_buffer, _("Studies"))
Stream.add_property('knowledges', Knowledge.within_buffer, _("Knowledges"))
Stream.add_property('proceedings', Proceeding.within_buffer, _("Proceedings"))
Stream.add_property('followups', FollowUp.within_buffer, _("Follow-ups"))
Stream.add_property('followups_without_knowledges', FollowUp.within_buffer_without_knowledge, _("Follow-ups"))
Stream.add_property('interventions', Intervention.within_buffer, _("Interventions"))
Stream.add_property('interventions_without_knowledges', Intervention.within_buffer_without_knowledge, _("Interventions"))

Intervention.add_property('streams', Stream.within_buffer, _("Stream"))
AdministrativeFile.add_property('streams', Stream.within_buffer, _("Stream"))
SensitiveArea.add_property('streams', Stream.within_buffer, _("Stream"))
