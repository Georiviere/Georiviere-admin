from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.contrib.gis.geos import GeometryCollection, LineString
from django.db.models import F, Sum
from django.utils.translation import gettext_lazy as _

from mapentity.models import MapEntityMixin
from geotrek.authent.models import StructureRelated, StructureOrNoneRelated
from geotrek.common.mixins import TimeStampedModelMixin
from geotrek.common.utils import classproperty
from geotrek.zoning.mixins import ZoningPropertiesMixin

from georiviere.main.models import AddPropertyBufferMixin
from georiviere.watershed.mixins import WatershedPropertiesMixin


class AdministrativeFilesMixin:
    """Get administrative files list from `administrative_operations`"""

    @property
    def administrative_files(self):
        return [operation.administrative_file for operation
                in self.administrative_operations.select_related('administrative_file').all()]


class Organism(StructureOrNoneRelated):
    """Model for Organism"""

    name = models.CharField(max_length=128, verbose_name=_("Organism"))

    class Meta:
        verbose_name = _("Organism")
        verbose_name_plural = _("Organisms")
        ordering = ['name']

    def __str__(self):
        if self.structure:
            return "{} ({})".format(self.name, self.structure.name)
        return self.name


class AdministrativeFileType(StructureOrNoneRelated):
    """Model for Administraive file type"""

    label = models.CharField(max_length=128, verbose_name=_("Label"))

    class Meta:
        verbose_name = _("Admin file type")
        verbose_name_plural = _("Admin file types")
        ordering = ['label']

    def __str__(self):
        if self.structure:
            return "{} ({})".format(self.label, self.structure.name)
        return self.label


class AdministrativeFileDomain(StructureOrNoneRelated):
    """Model for Administraive file domain"""

    label = models.CharField(max_length=128, verbose_name=_("Label"))

    class Meta:
        verbose_name = _("Admin file domain")
        verbose_name_plural = _("Admin file domains")
        ordering = ['label']

    def __str__(self):
        if self.structure:
            return "{} ({})".format(self.label, self.structure.name)
        return self.label


class AdministrativeFile(TimeStampedModelMixin, WatershedPropertiesMixin, ZoningPropertiesMixin,
                         AddPropertyBufferMixin, MapEntityMixin, StructureRelated):
    """Administrative and financial file
    Can be related to 0 or N content types with AdministrativeOperation model.
    """

    name = models.CharField(verbose_name=_("Name"), max_length=128)
    description = models.TextField(verbose_name=_("Description"), blank=True)

    begin_date = models.DateField(default=datetime.now,
                                  verbose_name=_("Begin date"))
    end_date = models.DateField(blank=True, null=True,
                                verbose_name=_("End date"))

    adminfile_type = models.ForeignKey('AdministrativeFileType',
                                       null=True, blank=True,
                                       on_delete=models.PROTECT,
                                       verbose_name=_("Admin file type"))
    domain = models.ForeignKey('AdministrativeFileDomain',
                               null=True, blank=True,
                               on_delete=models.PROTECT,
                               verbose_name=_("Admin file domain"))

    project_owners = models.ManyToManyField(Organism,
                                            related_name='owns',
                                            blank=True, verbose_name=_("Project owners"))
    project_managers = models.ManyToManyField(Organism,
                                              related_name='manages',
                                              blank=True, verbose_name=_("Project managers"))

    funders = models.ManyToManyField(Organism,
                                     through='Funding',
                                     verbose_name=_("Funders"))

    contractors = models.ManyToManyField(Organism,
                                         related_name="projects", blank=True,
                                         verbose_name=_("Contractors"))
    constraints = models.TextField(verbose_name=_("Constraints"), blank=True,
                                   help_text=_("Specific conditions, etc."))
    global_cost = models.DecimalField(verbose_name=_("Global cost"),
                                      max_digits=19, decimal_places=2, default=0)
    eid = models.CharField(verbose_name=_("External id"), max_length=1024,
                           blank=True, null=True)

    class Meta:
        verbose_name = _("Administrative file")
        verbose_name_plural = _("Administrative files")
        ordering = ['-begin_date', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._geom = None

    def __str__(self):
        return self.name

    @property
    def name_display(self):
        return '<a data-pk="{0}" href="{1}" title="{2}">{3}</a>'.format(
            self.pk,
            self.get_detail_url(),
            self,
            self.name
        )

    @property
    def funders_display(self):
        return [str(f) for f in self.funders.all()]

    @classmethod
    def get_create_label(cls):
        return _("Add a new admin file")

    @classproperty
    def geomfield(cls):
        # Fake field, TODO: still better than overkill code in views, but can do neater.
        c = GeometryCollection([LineString((0, 0), (1, 1))], srid=settings.SRID)
        c.name = 'geom'
        return c

    @property
    def geom(self):
        """ Merge all studies geometry into a collection
        Warning: Postgis 2.5+ with st_intersects on Collect
        """
        if self._geom is None:
            geoms = []
            for operation in self.operations.all():
                if getattr(operation.content_object, 'geom') is not None:
                    geoms.append(operation.content_object.geom)
            if geoms:
                self._geom = GeometryCollection(*geoms, srid=settings.SRID)
        return self._geom

    @property
    def api_geom(self):
        if not self.geom:
            return None
        return self.geom.transform(settings.API_SRID, clone=True)

    @geom.setter
    def geom(self, value):
        self._geom = value

    @property
    def total_costs(self):
        """Total costs for this administrative and financial file
        :return dict
        """
        results = self.operations.all().aggregate(
            estimated=Sum('estimated_cost'),
            material=Sum('material_cost'),
            subcontract=Sum('subcontract_cost'),
            mandays=Sum('manday_cost'),
            actual=Sum(F('material_cost') + F('subcontract_cost') + F('manday_cost')),
        )
        return results


class AdministrativeDeferral(StructureOrNoneRelated):
    label = models.CharField(verbose_name=_("Label"), max_length=128,
                             blank=True, null=True)

    class Meta:
        verbose_name = _("Administrative deferral")
        verbose_name_plural = _("Administrative deferrals")

    def __str__(self):
        if self.structure:
            return "{} ({})".format(self.label, self.structure.name)
        return self.label


class AdministrativePhase(models.Model):
    administrative_file = models.ForeignKey(AdministrativeFile,
                                            on_delete=models.CASCADE,
                                            related_name='phases',
                                            verbose_name=_("Phases"))
    name = models.CharField(verbose_name=_("Name"), max_length=128, default="", blank=True)
    estimated_budget = models.DecimalField(verbose_name=_("Estimated budget"),
                                           max_digits=19, decimal_places=2, default=0)
    revised_budget = models.DecimalField(verbose_name=_("Revised budget"),
                                         max_digits=19, decimal_places=2,
                                         blank=True, null=True)

    class Meta:
        verbose_name = _("Administrative phase")
        verbose_name_plural = _("Administrative phases")

    def __str__(self):
        return self.name

    @property
    def total_costs(self):
        """Total costs for this phase
        :return dict
        """
        cost = self.operations.all().aggregate(
            actual=Sum(F('material_cost') + F('subcontract_cost') + F('manday_cost')),
        )
        return cost


class AdministrativeOperation(models.Model):
    """Model to link projects to any other contents in a N-N relation"""

    administrative_file = models.ForeignKey(
        AdministrativeFile,
        on_delete=models.CASCADE,
        related_name="operations",
        verbose_name=_('Administrative file')
    )
    phase = models.ForeignKey(AdministrativePhase,
                              null=True, blank=True,
                              related_name='operations',
                              verbose_name=_("Phase"),
                              on_delete=models.SET_NULL)
    operation_status = models.ForeignKey('maintenance.InterventionStatus',
                                         null=True, blank=True,
                                         verbose_name=_("Status"),
                                         on_delete=models.CASCADE)
    deferral = models.ManyToManyField(AdministrativeDeferral,
                                      related_name='operations',
                                      blank=True, verbose_name=_("Deferral"))
    name = models.CharField(verbose_name=_("Name"), max_length=128, default="", blank=True)
    estimated_cost = models.DecimalField(verbose_name=_("Estimated cost"),
                                         max_digits=19, decimal_places=2, default=0)
    material_cost = models.DecimalField(verbose_name=_("Material cost"),
                                        max_digits=19, decimal_places=2, default=0)
    subcontract_cost = models.DecimalField(verbose_name=_("Subcontract cost"),
                                           max_digits=19, decimal_places=2, default=0)

    # Manday cost is computed on Manday save method, each time a Manday is updated or added to this operation
    manday_cost = models.DecimalField(verbose_name=_("Cost of man-day"),
                                      max_digits=19, decimal_places=2, default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _("Administrative operation")
        verbose_name_plural = _("Administrative operations")

    def __str__(self):
        return '{0} {1}'.format(
            self.content_type.name,
            str(self.content_object)
        )

    def _get_manday_cost(self):
        """Man-day costs computed for this operation"""
        if not self.mandays.count():
            return Decimal('0.00')
        result = self.mandays \
            .annotate(cost=F('nb_days') * F('job_category__man_day_cost')) \
            .aggregate(total=Sum('cost'))
        return result['total'].quantize(Decimal('1.00'))

    @property
    def actual_cost(self):
        """Actual costs computed : subcontract, material and man-day cost sum"""
        return self.subcontract_cost + self.material_cost + self.manday_cost

    @property
    def content_object_display(self):
        icon = self.content_object._meta.model_name
        title = str(self)
        url = self.content_object.get_detail_url()
        return '<img src="{}images/{}-16.png"> <a href={}>{}</a>'.format(
            settings.STATIC_URL,
            icon,
            url,
            title)


class Funding(models.Model):
    """Model for funding"""

    amount = models.DecimalField(verbose_name=_("Amount"),
                                 max_digits=19, decimal_places=2, default=0)
    administrative_file = models.ForeignKey(AdministrativeFile,
                                            verbose_name=_("Administrative file"),
                                            on_delete=models.CASCADE)
    organism = models.ForeignKey(Organism, verbose_name=_("Organism"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Funding")
        verbose_name_plural = _("Fundings")

    def __str__(self):
        return "{} : {:.2f} €".format(self.organism, self.amount)


class JobCategory(StructureOrNoneRelated):
    """Model for job category, used by man-days"""

    label = models.CharField(max_length=128, verbose_name=_("Label"))
    man_day_cost = models.DecimalField(
        verbose_name=_("Cost of man-day"),
        default=1.0,
        decimal_places=2,
        max_digits=8
    )
    active = models.BooleanField(verbose_name=_("Active"), default=True)

    class Meta:
        verbose_name = _("Job category")
        verbose_name_plural = _("Job categories")
        ordering = ['label']

    def __str__(self):
        if self.structure:
            return "{} ({})".format(self.label, self.structure.name)
        return self.label


class ManDay(models.Model):
    """Model for man-days"""

    nb_days = models.DecimalField(verbose_name=_("Man-days"), decimal_places=2, max_digits=6)
    operation = models.ForeignKey(AdministrativeOperation,
                                  related_name="mandays",
                                  verbose_name=_("Operation"),
                                  on_delete=models.CASCADE)
    job_category = models.ForeignKey(JobCategory,
                                     related_name="mandays",
                                     verbose_name=_("Job category"),
                                     on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Man-day")
        verbose_name_plural = _("Man-days")

    @property
    def cost(self):
        """Man-day costs according to job category, rounded to 2 digit"""
        return (self.nb_days * self.job_category.man_day_cost).quantize(Decimal('1.00'))

    def __str__(self):
        return str(self.nb_days)

    def save(self, *args, **kwargs):
        """Compute manday_cost value for related operation"""
        super().save(*args, **kwargs)
        self.operation.manday_cost = self.operation._get_manday_cost()
        self.operation.save()
