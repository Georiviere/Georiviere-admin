from datetime import datetime

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from mapentity.models import MapEntityMixin

from geotrek.authent.models import StructureRelated, StructureOrNoneRelated
from geotrek.common.mixins import TimeStampedModelMixin
from geotrek.common.utils import classproperty
from geotrek.zoning.mixins import ZoningPropertiesMixin

from georiviere.finances_administration.models import AdministrativeOperation, AdministrativeFilesMixin
from georiviere.main.models import AddPropertyBufferMixin
from georiviere.watershed.mixins import WatershedPropertiesMixin


class Intervention(TimeStampedModelMixin, WatershedPropertiesMixin, ZoningPropertiesMixin,
                   AdministrativeFilesMixin, AddPropertyBufferMixin, MapEntityMixin, StructureRelated):

    target_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey('target_type', 'target_id')

    name = models.CharField(verbose_name=_("Name"), max_length=128)
    date = models.DateField(default=datetime.now, verbose_name=_("Date"))

    _geom = models.GeometryField(srid=settings.SRID, spatial_index=True, null=True, blank=True)

    intervention_status = models.ForeignKey('InterventionStatus',
                                            verbose_name=_("Status"),
                                            on_delete=models.CASCADE)

    intervention_type = models.ForeignKey('InterventionType',
                                          null=True, blank=True,
                                          on_delete=models.CASCADE,
                                          verbose_name=_("Type"))

    stake = models.ForeignKey('InterventionStake',
                              null=True, blank=True,
                              on_delete=models.CASCADE,
                              related_name='interventions',
                              verbose_name=_("Stake"))

    disorders = models.ManyToManyField('InterventionDisorder',
                                       related_name="interventions",
                                       verbose_name=_("Disorders"), blank=True)

    description = models.TextField(blank=True,
                                   verbose_name=_("Description"),
                                   help_text=_("Remarks and notes"))

    # Technical information
    length = models.FloatField(default=0.0, blank=True, null=True, verbose_name=_("Length"))
    width = models.FloatField(default=0.0, blank=True, null=True, verbose_name=_("Width"))
    height = models.FloatField(default=0.0, blank=True, null=True, verbose_name=_("Height"))
    area = models.FloatField(editable=False, default=0, blank=True, null=True, verbose_name=_("Area"))

    # generic relations
    administrative_operations = GenericRelation(AdministrativeOperation)
    contributions = GenericRelation(
        'contribution.Contribution',
        content_type_field='linked_object_type',
        object_id_field='linked_object_id',
    )

    class Meta:
        verbose_name = _("Intervention")
        verbose_name_plural = _("Interventions")

    @classmethod
    def get_create_label(cls):
        return _("Add a new intervention")

    @classmethod
    def within_buffer_without_knowledge(cls, topology):
        area = topology.geom.buffer(settings.BASE_INTERSECTION_MARGIN)
        from georiviere.description.models import Knowledge
        target_type = Knowledge.get_content_type_id()
        qs = cls.objects.filter(_geom__intersects=area).exclude(target_type=target_type)
        return qs

    @property
    def name_display(self):
        return '<a data-pk="{}" href="{}" title="{}" >{}</a>'.format(
            self.pk,
            self.get_detail_url(),
            self.name,
            self.name)

    @property
    def name_csv_display(self):
        return self.name

    @property
    def geom(self):
        if self._geom is None:
            if self.target:
                self._geom = getattr(self.target, 'geom')
        return self._geom

    @geom.setter
    def geom(self, value):
        self._geom = value

    @property
    def api_geom(self):
        if not self.geom:
            return None
        return self.geom.transform(settings.API_SRID, clone=True)

    @classproperty
    def target_verbose_name(cls):
        return _("On")

    @property
    def target_display(self):
        """Return html to display target"""
        if not self.target:
            return ""
        icon = self.target._meta.model_name
        title = str(self.target)
        url = self.target.get_detail_url()
        return '<img src="{}images/{}-16.png"> <a href={}>{}</a>'.format(
            settings.STATIC_URL,
            icon,
            url,
            title)

    @property
    def target_csv_display(self):
        return "{}: {} ({})".format(
            _(self.target._meta.verbose_name),
            self.target,
            self.target.pk)

    def __str__(self):
        return "{} ({})".format(self.name, self.date)


class InterventionStatus(StructureOrNoneRelated):

    label = models.CharField(verbose_name=_("Label"), max_length=128)
    order = models.PositiveSmallIntegerField(default=None, null=True, blank=True, verbose_name=_("Display order"))

    class Meta:
        verbose_name = _("Intervention's status")
        verbose_name_plural = _("Intervention's statuses")
        ordering = ['order', 'label']

    def __str__(self):
        if self.structure:
            return "{} ({})".format(self.label, self.structure.name)
        return self.label


class InterventionType(StructureOrNoneRelated):

    label = models.CharField(max_length=128, verbose_name=_("Label"))

    class Meta:
        verbose_name = _("Intervention's type")
        verbose_name_plural = _("Intervention's types")
        ordering = ['label']

    def __str__(self):
        if self.structure:
            return "{} ({})".format(self.label, self.structure.name)
        return self.label


class InterventionStake(StructureOrNoneRelated):

    label = models.CharField(max_length=128, verbose_name=_("Label"))

    class Meta:
        verbose_name = _("Intervention's stake")
        verbose_name_plural = _("Intervention's stakes")
        ordering = ['label']

    def __str__(self):
        if self.structure:
            return "{} ({})".format(self.label, self.structure.name)
        return self.label


class InterventionDisorder(StructureOrNoneRelated):

    label = models.CharField(max_length=128, verbose_name=_("Label"))

    class Meta:
        verbose_name = _("Intervention's disorder")
        verbose_name_plural = _("Intervention's disorders")
        ordering = ['label']

    def __str__(self):
        if self.structure:
            return "{} ({})".format(self.label, self.structure.name)
        return self.label


class OfflineIntervention(models.Model):
    uuid = models.TextField(primary_key=True)
    gra_id = models.IntegerField(null=True)  # FK on 'maintenance.Intervention'
    geom = models.GeometryField(srid=settings.SRID, spatial_index=True, null=True)
    knowledge_uuid = models.TextField(null=True)  # FK on 'OfflineKnowledge'
    name = models.CharField(max_length=128, null=True)
    date = models.DateField(null=True)
    intervention_status = models.IntegerField(null=True)  # FK on 'InterventionStatus'
    intervention_type = models.IntegerField(null=True)  # FK on 'InterventionType'
    stake = models.IntegerField(null=True)  # FK on 'InterventionStake'
    description = models.TextField(null=True)
    length = models.FloatField(default=0.0, null=True)
    width = models.FloatField(default=0.0, null=True)
    height = models.FloatField(default=0.0, null=True)
    date_insert = models.DateTimeField(null=True)
    date_update = models.DateTimeField(null=True)
    username = models.TextField(null=True)


class OfflineInterventionDisorder(models.Model):
    uuid = models.TextField(primary_key=True)
    disorder_id = models.IntegerField(null=True)  # FK on InterventionDisorder
    intervention_uuid = models.TextField(null=True)  # FK on OfflineIntervention
