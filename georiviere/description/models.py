from django.conf import settings
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.utils.functional import classproperty
from django.utils.translation import gettext_lazy as _

from mapentity.models import MapEntityMixin

from georiviere.altimetry import AltimetryMixin
from geotrek.authent.models import StructureRelated, StructureOrNoneRelated
from geotrek.common.mixins import TimeStampedModelMixin
from geotrek.zoning.mixins import ZoningPropertiesMixin

from georiviere.main.models import AddPropertyBufferMixin
from georiviere.watershed.mixins import WatershedPropertiesMixin
from georiviere.river.models import Stream, Topology, TopologyMixin
from georiviere.observations.models import Station
from georiviere.proceeding.models import Proceeding
from georiviere.studies.models import Study
from georiviere.knowledge.models import Knowledge


class PlanLayoutType(StructureOrNoneRelated):
    label = models.CharField(max_length=128, verbose_name=_("Label"), )

    class Meta:
        verbose_name = _("Plan layout type")
        verbose_name_plural = _("Plan layout types")

    def __str__(self):
        return self.label


class HabitatType(StructureOrNoneRelated):
    label = models.CharField(max_length=128, verbose_name=_("Label"), )

    class Meta:
        verbose_name = _("Habitat type")
        verbose_name_plural = _("Habitat types")

    def __str__(self):
        return self.label


class HabitatsDiversity(StructureOrNoneRelated):
    label = models.CharField(max_length=128, verbose_name=_("Label"), )

    class Meta:
        verbose_name = _("Habitats diversity")
        verbose_name_plural = _("Habitats diversities")

    def __str__(self):
        return self.label


class BankState(StructureOrNoneRelated):
    label = models.CharField(max_length=128, verbose_name=_("Label"), )

    class Meta:
        verbose_name = _("Bank state")
        verbose_name_plural = _("Bank states")

    def __str__(self):
        return self.label


class SedimentDynamic(StructureOrNoneRelated):
    label = models.CharField(max_length=128, verbose_name=_("Label"), )

    class Meta:
        verbose_name = _("Sediment dynamic")
        verbose_name_plural = _("Sediment dynamics")

    def __str__(self):
        return self.label


class GranulometricDiversity(StructureOrNoneRelated):
    label = models.CharField(max_length=128, verbose_name=_("Label"), )

    class Meta:
        verbose_name = _("Granulometric diversity")
        verbose_name_plural = _("Granulometric diversities")

    def __str__(self):
        return self.label


class FaciesDiversity(StructureOrNoneRelated):
    label = models.CharField(max_length=128, verbose_name=_("Label"), )

    class Meta:
        verbose_name = _("Facies diversity")
        verbose_name_plural = _("Facies diversities")

    def __str__(self):
        return self.label


class WorkingSpaceType(StructureOrNoneRelated):
    label = models.CharField(max_length=128, verbose_name=_("Label"), )

    class Meta:
        verbose_name = _("Working space type")
        verbose_name_plural = _("Working space types")

    def __str__(self):
        return self.label


class FlowType(StructureOrNoneRelated):
    label = models.CharField(max_length=128, verbose_name=_("Label"), )

    class Meta:
        verbose_name = _("Flow type")
        verbose_name_plural = _("Flow types")

    def __str__(self):
        return self.label


class Morphology(AddPropertyBufferMixin, TopologyMixin, TimeStampedModelMixin,
                 WatershedPropertiesMixin, ZoningPropertiesMixin,
                 AltimetryMixin, MapEntityMixin, models.Model):
    topology = models.OneToOneField(Topology, on_delete=models.CASCADE, related_name='morphology')
    good_working_space_left = models.ForeignKey(
        WorkingSpaceType, verbose_name=_("Left good Working space"),
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='good_working_space_left'
    )
    good_working_space_right = models.ForeignKey(
        WorkingSpaceType, verbose_name=_("Right good Working space"),
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='good_working_space_right'
    )
    facies_diversity = models.ForeignKey(
        FaciesDiversity, verbose_name=_("Facies diversity"),
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='facies_diversity'
    )
    main_flow = models.ForeignKey(
        FlowType, verbose_name=_("Main flow"),
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='main_flow'
    )
    secondary_flows = models.ManyToManyField(
        FlowType, verbose_name=_("Secondary flow"),
        blank=True,
        related_name='morphologies_on_second'
    )
    granulometric_diversity = models.ForeignKey(
        GranulometricDiversity,
        verbose_name=_("Granulometric diversity"),
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    full_edge_height = models.FloatField(
        default=0.0, null=True, blank=True,
        verbose_name=_("Full edge height")
    )
    full_edge_width = models.FloatField(
        default=0.0, null=True, blank=True,
        verbose_name=_("Full edge width")
    )
    sediment_dynamic = models.ForeignKey(
        SedimentDynamic, verbose_name=_("Sediment dynamic"),
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    bank_state_left = models.ForeignKey(
        BankState, verbose_name=_("Bank state left"),
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='bank_state_left'
    )
    bank_state_right = models.ForeignKey(
        BankState, verbose_name=_("Bank state right"),
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='bank_state_right'
    )
    habitats_diversity = models.ForeignKey(
        HabitatsDiversity, verbose_name=_("Habitats diversity"),
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    main_habitat = models.ForeignKey(
        HabitatType, verbose_name=_("Main habitat"),
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='main_habitat'
    )
    secondary_habitats = models.ManyToManyField(
        HabitatType, verbose_name=_("Secondary habitat"),
        blank=True,
        related_name='morphologies_on_second'
    )
    plan_layout = models.ForeignKey(
        PlanLayoutType, verbose_name=_("Plan layout"),
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    description = models.TextField(verbose_name=_("Description"), blank=True)
    geom = models.LineStringField(srid=settings.SRID, spatial_index=True)

    class Meta:
        verbose_name = _("Morphology")
        verbose_name_plural = _("Morphologies")
        triggers = AltimetryMixin.Meta.triggers

    def __str__(self):
        if self.main_flow:
            return f"{self.main_flow}"
        else:
            return f"{self.pk}"

    @classproperty
    def name_verbose_name(cls):
        return _("Name")

    @property
    def name(self):
        return self.main_flow_csv_display

    @property
    def main_flow_display(self):
        display_name = self.main_flow or _("Not completed")
        return f'<a data-pk="{self.pk}" href="{self.get_detail_url()}" >{display_name}</a>'

    @property
    def main_flow_csv_display(self):
        return self.main_flow

    @classmethod
    def get_create_label(cls):
        return _("Add a new morphology")


class LandType(StructureOrNoneRelated):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Land type")
        verbose_name_plural = _("Land types")
        ordering = ['label']

    def __str__(self):
        return self.label


class ControlType(StructureOrNoneRelated):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Control type")
        verbose_name_plural = _("Control types")
        ordering = ['label']

    def __str__(self):
        if self.structure:
            return "{} ({})".format(self.label, self.structure.name)
        return self.label


class Land(AddPropertyBufferMixin, TimeStampedModelMixin, WatershedPropertiesMixin,
           ZoningPropertiesMixin, AltimetryMixin, MapEntityMixin, StructureRelated):
    geom = models.GeometryField(srid=settings.SRID, spatial_index=True)
    land_type = models.ForeignKey(LandType, verbose_name=_("Land type"), on_delete=models.CASCADE)
    owner = models.TextField(verbose_name=_("Owner"), blank=True)
    agreement = models.BooleanField(verbose_name=_("Agreement"), default=False)
    description = models.TextField(verbose_name=_("Description"), blank=True)
    identifier = models.CharField(verbose_name=_("Identifier"), blank=True, max_length=255)
    control_type = models.ForeignKey(ControlType, verbose_name=_("Control type"), null=True, blank=True,
                                     on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("Land")
        verbose_name_plural = _("Lands")
        triggers = AltimetryMixin.Meta.triggers

    def __str__(self):
        return f"{self.land_type}"

    @property
    def name(self):
        return self.land_type_csv_display

    @property
    def land_type_display(self):
        return f'<a data-pk="{self.pk}" href="{self.get_detail_url()}" >{self.land_type}</a>'

    @property
    def land_type_csv_display(self):
        return f"{self.land_type}"


class UsageType(StructureOrNoneRelated):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Usage type")
        verbose_name_plural = _("Usage types")
        ordering = ['label']

    def __str__(self):
        return self.label


class Usage(AddPropertyBufferMixin, TimeStampedModelMixin, WatershedPropertiesMixin, ZoningPropertiesMixin, AltimetryMixin,
            MapEntityMixin, StructureRelated):
    geom = models.GeometryField(srid=settings.SRID, spatial_index=True)
    usage_types = models.ManyToManyField(UsageType, verbose_name=_("Usage types"))
    description = models.TextField(verbose_name=_("Description"), blank=True)

    class Meta:
        verbose_name = _("Usage")
        verbose_name_plural = _("Usages")
        triggers = AltimetryMixin.Meta.triggers

    def __str__(self):
        return ', '.join(self.usage_types.values_list("label", flat=True))

    @classproperty
    def name_verbose_name(cls):
        return _("Name")

    @property
    def name(self):
        return self.usage_types_csv_display

    @property
    def usage_types_display(self):
        usage_types = ', '.join([str(n) for n in self.usage_types.all()])
        return f'<a data-pk="{self.pk}" href="{self.get_detail_url()}" >{usage_types}</a>'

    @property
    def usage_types_csv_display(self):
        return f"{self.usage_types}"


class StatusType(StructureOrNoneRelated):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Status type")
        verbose_name_plural = _("Status types")
        ordering = ['label']

    def __str__(self):
        return self.label


class Status(TopologyMixin, AddPropertyBufferMixin, TimeStampedModelMixin, WatershedPropertiesMixin,
             ZoningPropertiesMixin, AltimetryMixin, MapEntityMixin, models.Model):
    topology = models.OneToOneField(Topology, on_delete=models.CASCADE, related_name='status')
    geom = models.LineStringField(srid=settings.SRID, spatial_index=True)
    status_types = models.ManyToManyField(StatusType, related_name="status", verbose_name=_("Status type"), blank=True)
    regulation = models.BooleanField(default=False, help_text=_("Your status is a regulation status"),
                                     verbose_name=_("Regulation"))
    referencial = models.BooleanField(default=False, help_text=_("Your status is a referencial status"),
                                      verbose_name=_("Referencial"))
    description = models.TextField(verbose_name=_("Description"), blank=True)

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Statuses")
        triggers = AltimetryMixin.Meta.triggers

    def __str__(self):
        if self.status_types.count():
            return ', '.join([value.label for value in self.status_types.all()])
        else:
            return f"{self.pk}"

    def clean(self):
        if hasattr(self, 'topology') and self.topology is not None:
            if self.topology.qualified and not self.status_types.exists():
                raise ValidationError(
                    _("Status cannot be qualified but without type")
                )

    @classproperty
    def name_verbose_name(cls):
        return _("Name")

    @property
    def name(self):
        return self.status_types_csv_display

    @property
    def status_types_display(self):
        if self.status_types.exists():
            return f'<a data-pk="{self.pk}" href="{self.get_detail_url()}" >{self}</a>'
        return f'<a data-pk="{self.pk}" href="{self.get_detail_url()}" >{_("No type")}</a>'

    @property
    def status_types_csv_display(self):
        return str(self.status_types)

    @classmethod
    def get_create_label(cls):
        return _("Add a new status")


Land.add_property('streams', Stream.within_buffer, _("Stream"))
Land.add_property('status', Status.within_buffer, _("Status"))
Land.add_property('morphologies', Morphology.within_buffer, _("Morphologies"))
Land.add_property('usages', Usage.within_buffer, _("Usages"))
Land.add_property('stations', Station.within_buffer, _("Station"))
Land.add_property('studies', Study.within_buffer, _("Study"))
Land.add_property('proceedings', Proceeding.within_buffer, _("Proceeding"))
Land.add_property('knowledges', Knowledge.within_buffer, _("Knowledge"))

Morphology.add_property('streams', lambda self: [self.topology.stream], _("Stream"))
Morphology.add_property('status', lambda self: self.get_topology('status'), _("Status"))
Morphology.add_property('lands', Land.within_buffer, _("Lands"))
Morphology.add_property('usages', Usage.within_buffer, _("Usages"))
Morphology.add_property('stations', Station.within_buffer, _("Station"))
Morphology.add_property('studies', Study.within_buffer, _("Study"))
Morphology.add_property('proceedings', Proceeding.within_buffer, _("Proceeding"))
Morphology.add_property('knowledges', Knowledge.within_buffer, _("Knowledge"))

Status.add_property('streams', lambda self: [self.topology.stream], _("Stream"))
Status.add_property('morphologies', lambda self: self.get_topology('morphology'), _("Morphologies"))
Status.add_property('lands', Land.within_buffer, _("Lands"))
Status.add_property('usages', Usage.within_buffer, _("Usages"))
Status.add_property('stations', Station.within_buffer, _("Station"))
Status.add_property('studies', Study.within_buffer, _("Study"))
Status.add_property('proceedings', Proceeding.within_buffer, _("Proceeding"))
Status.add_property('knowledges', Knowledge.within_buffer, _("Knowledge"))

Usage.add_property('streams', Stream.within_buffer, _("Stream"))
Usage.add_property('lands', Land.within_buffer, _("Lands"))
Usage.add_property('morphologies', Morphology.within_buffer, _("Morphologies"))
Usage.add_property('statuses', Status.within_buffer, _("Statuses"))
Usage.add_property('stations', Station.within_buffer, _("Station"))
Usage.add_property('studies', Study.within_buffer, _("Study"))
Usage.add_property('proceedings', Proceeding.within_buffer, _("Proceeding"))
Usage.add_property('knowledges', Knowledge.within_buffer, _("Knowledge"))

Stream.add_property('lands', Land.within_buffer, _("Lands"))
Stream.add_property('usages', Usage.within_buffer, _("Usages"))

Station.add_property('morphologies', Morphology.within_buffer, _("Morphologies"))
Station.add_property('lands', Land.within_buffer, _("Lands"))
Station.add_property('usages', Usage.within_buffer, _("Usages"))
Station.add_property('statuses', Status.within_buffer, _("Statuses"))

Study.add_property('morphologies', Morphology.within_buffer, _("Morphologies"))
Study.add_property('lands', Land.within_buffer, _("Lands"))
Study.add_property('usages', Usage.within_buffer, _("Usages"))
Study.add_property('statuses', Status.within_buffer, _("Statuses"))

Proceeding.add_property('morphologies', Morphology.within_buffer, _("Morphologies"))
Proceeding.add_property('lands', Land.within_buffer, _("Lands"))
Proceeding.add_property('usages', Usage.within_buffer, _("Usages"))
Proceeding.add_property('statuses', Status.within_buffer, _("Statuses"))

Knowledge.add_property('morphologies', Morphology.within_buffer, _("Morphologies"))
Knowledge.add_property('lands', Land.within_buffer, _("Lands"))
Knowledge.add_property('usages', Usage.within_buffer, _("Usages"))
Knowledge.add_property('statuses', Status.within_buffer, _("Statuses"))
