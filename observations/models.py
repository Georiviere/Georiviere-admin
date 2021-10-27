from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from mapentity.models import MapEntityMixin
from geotrek.authent.models import StructureRelated, StructureOrNoneRelated

from geotrek.common.mixins import TimeStampedModelMixin
from geotrek.zoning.mixins import ZoningPropertiesMixin

from main.models import AddPropertyBufferMixin
from finances_administration.models import AdministrativeOperation, AdministrativeFilesMixin
from maintenance.models import Intervention
from watershed.mixins import WatershedPropertiesMixin


class ParameterManager(models.Manager):
    """Use this manager for performances"""

    def get_queryset(self):
        return super().get_queryset().select_related('unit')


class StationProfile(StructureOrNoneRelated):
    """Station profile
    ex : Physico-chemical station, Hydrometric station…
    """
    code = models.CharField(max_length=6, unique=True, null=False, verbose_name=_("Station profile code"))
    label = models.CharField(max_length=200, null=False, verbose_name=_("Station profile label"))

    class Meta:
        verbose_name = _("Station profile")
        verbose_name_plural = _("Station profiles")

    def __str__(self):
        return "{1} ({0})".format(self.code, self.label)


class Station(TimeStampedModelMixin, WatershedPropertiesMixin, ZoningPropertiesMixin,
              AdministrativeFilesMixin, AddPropertyBufferMixin, MapEntityMixin, StructureRelated):
    """Station model"""

    class LocalInfluenceChoices(models.IntegerChoices):
        """Choices for local influence"""
        UNKNOWN = 0, _('Unknown')
        NULL = 1, _('Null')
        LOW_WATER_ONLY = 2, _('Low water only')
        STRONG = 3, _('Strong')
        HIGH_WATER_ONLY = 4, _('High water only')

    code = models.CharField(max_length=50, unique=True, null=False, verbose_name=_("Station code"))
    label = models.CharField(max_length=200, null=False, verbose_name=_("Station label"))
    station_profiles = models.ManyToManyField(
        StationProfile,
        verbose_name=_("Station profile"))

    description = models.TextField(blank=True, default="", verbose_name=_("Station description"))
    geom = models.GeometryField(srid=settings.SRID, spatial_index=True)
    site_code = models.CharField(max_length=50, blank=True, default="", verbose_name=_("Site code"))
    station_uri = models.URLField(blank=True, default="", verbose_name=_("Station URI"))
    purpose_code = models.CharField(max_length=50, blank=True, default="", verbose_name=_("Station purpose"))
    in_service = models.BooleanField(blank=True, null=True, verbose_name=_("In service"))

    local_influence = models.IntegerField(
        choices=LocalInfluenceChoices.choices,
        default=LocalInfluenceChoices.UNKNOWN,
        verbose_name=_("Local influence"),
        help_text=_("For hydrometric station profile"),
    )
    hardness = models.IntegerField(
        blank=True, null=True,
        verbose_name=_("Hardness"),
        help_text=_("For physico-chemical station profile"),
    )

    # generic relations
    interventions = GenericRelation(
        Intervention,
        content_type_field='target_type',
        object_id_field='target_id',
    )

    administrative_operations = GenericRelation(AdministrativeOperation)

    class Meta:
        verbose_name = _("Station")
        verbose_name_plural = _("Stations")

    def __str__(self):
        return "{1} ({0})".format(self.code, self.label)

    @property
    def code_display(self):
        return '<a data-pk="{0}" href="{1}" title="{2}">{3}</a>'.format(
            self.pk,
            self.get_detail_url(),
            self,
            self.code
        )

    @property
    def label_display(self):
        return '<a data-pk="{0}" href="{1}" title="{2}">{3}</a>'.format(
            self.pk,
            self.get_detail_url(),
            self,
            self.label
        )

    @property
    def local_influence_display(self):
        return self.get_local_influence_display()

    @property
    def station_profiles_display(self):
        return ', '.join([str(el) for el in self.station_profiles.all()])

    def get_parameters_tracked(self):
        return self.parametertracking_set.select_related('parameter__unit').all()

    @classmethod
    def get_create_label(cls):
        return _("Add a new station")


class Unit(models.Model):
    """Model for unit, for exemple mg/l, m3/h, % …"""
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Code"))
    label = models.CharField(max_length=200, verbose_name=_("Label"))
    symbol = models.CharField(max_length=200, verbose_name=_("Symbol"))

    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")
        ordering = ["label"]

    def __str__(self):
        return self.symbol


class ParameterCategory(StructureOrNoneRelated):
    """Model for parameter category, for exemple Physical, Environmental, Microbiological"""
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Code"))
    label = models.CharField(max_length=200, verbose_name=_("Label"))
    definition = models.TextField(blank=True, default="", verbose_name=_("Definition"))

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = _("Parameter category")
        verbose_name_plural = _("Parameter categories")
        ordering = ["label"]


class Parameter(StructureOrNoneRelated):
    """Model for parameter, for exemple temperature, flow, arsenic"""

    class ParameterTypeChoice(models.IntegerChoices):
        """Choices for local influence"""
        QUALITATIVE = 1, _('Qualitative')
        QUANTITATIVE = 2, _('Quantitative')

    code = models.CharField(max_length=10, unique=True, verbose_name=_("Code"))
    label = models.CharField(max_length=200, verbose_name=_("Label"))
    definition = models.TextField(blank=True, default="", verbose_name=_("Definition"))
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Unit"))
    categories = models.ManyToManyField(ParameterCategory, related_name="parameters")
    parameter_type = models.IntegerField(
        null=False,
        choices=ParameterTypeChoice.choices,
        default=ParameterTypeChoice.QUANTITATIVE,
        verbose_name=_("Parameter type"),
    )

    objects = ParameterManager()

    class Meta:
        verbose_name = _("Parameter")
        verbose_name_plural = _("Parameters")
        ordering = ["label"]

    def __str__(self):
        if self.unit:
            return "{0} ({1})".format(self.label, self.unit)
        else:
            return self.label


class ParameterTracking(StructureOrNoneRelated):
    """Model for parameter trackin, related to a station and a parameter"""

    class DataAvailabilityChoice(models.IntegerChoices):
        """Choices for local influence"""
        ONLINE = 1, _('Online')
        ONDEMAND = 2, _('On demand')

    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name=_("Parameter"))
    station = models.ForeignKey(Station, on_delete=models.CASCADE, verbose_name=_("Station"))

    label = models.CharField(
        max_length=200, verbose_name=_("Label"),
        blank=True, default=""
    )
    measure_frequency = models.CharField(
        max_length=200, verbose_name=_("Measure frequency"),
        blank=True, default=""
    )
    transmission_frequency = models.CharField(
        max_length=200, verbose_name=_("Transmission frequency"),
        blank=True, default=""
    )
    data_availability = models.IntegerField(
        choices=DataAvailabilityChoice.choices,
        blank=True, null=True,
        verbose_name=_("Data availability")
    )
    measure_start_date = models.DateField(verbose_name=_("Measure start date"), blank=True, null=True)
    measure_end_date = models.DateField(verbose_name=_("Measure end date"), blank=True, null=True)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = _("Parameter tracking")
        verbose_name_plural = _("Parameter trackings")
        ordering = ["parameter"]

    @property
    def data_availability_display(self):
        return self.get_data_availability_display()
