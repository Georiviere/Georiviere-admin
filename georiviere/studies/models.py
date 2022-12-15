from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from mapentity.models import MapEntityMixin
from geotrek.authent.models import StructureRelated, StructureOrNoneRelated

from geotrek.common.mixins.models import TimeStampedModelMixin
from geotrek.zoning.mixins import ZoningPropertiesMixin

from georiviere.main.models import AddPropertyBufferMixin
from georiviere.finances_administration.models import AdministrativeOperation, AdministrativeFilesMixin
from georiviere.watershed.mixins import WatershedPropertiesMixin


class StudyType(StructureOrNoneRelated):
    """Study type model"""
    label = models.CharField(max_length=200, null=False, verbose_name=_("Label"))

    class Meta:
        verbose_name = _("Study type")
        verbose_name_plural = _("Study types")

    def __str__(self):
        return self.label


class Study(TimeStampedModelMixin, WatershedPropertiesMixin, ZoningPropertiesMixin,
            AdministrativeFilesMixin, AddPropertyBufferMixin, MapEntityMixin, StructureRelated):
    """Study model"""

    title = models.CharField(max_length=500, verbose_name=_("Title"))
    geom = models.GeometryField(srid=settings.SRID, spatial_index=True)
    study_types = models.ManyToManyField(
        StudyType,
        blank=False,
        verbose_name=_("Study types")
    )
    year = models.IntegerField(verbose_name=_("Year"))
    study_authors = models.TextField(blank=True, default="", verbose_name=_("Authors"))
    description = models.TextField(blank=True, default="", verbose_name=_("Description"))

    # generic relations
    administrative_operations = GenericRelation(AdministrativeOperation)

    class Meta:
        verbose_name = _("Study")
        verbose_name_plural = _("Studies")

    def __str__(self):
        return self.title

    @property
    def title_display(self):
        return '<a data-pk="{0}" href="{1}" title="{2}">{3}</a>'.format(
            self.pk,
            self.get_detail_url(),
            self,
            self.title
        )

    @classmethod
    def get_create_label(cls):
        return _("Add a new study")

    @property
    def study_types_display(self):
        return ', '.join([str(el) for el in self.study_types.all()])
