from datetime import datetime

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from mapentity.models import MapEntityMixin
from geotrek.authent.models import StructureRelated
from geotrek.common.mixins import TimeStampedModelMixin
from geotrek.zoning.mixins import ZoningPropertiesMixin

from georiviere.finances_administration.models import AdministrativeOperation, AdministrativeFilesMixin
from georiviere.maintenance.models import Intervention
from georiviere.watershed.mixins import WatershedPropertiesMixin
from georiviere.main.models import AddPropertyBufferMixin


class KnowledgeType(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Knowledge type")
        verbose_name_plural = _("Knowledge types")

    def __str__(self):
        return self.label


class VegetationAgeClassDiversity(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Age class diversity")
        verbose_name_plural = _("Age class diversities")

    def __str__(self):
        return self.label


class VegetationSpecificDiversity(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Specific diversity")
        verbose_name_plural = _("Specific diversities")

    def __str__(self):
        return self.label


class VegetationState(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Vegetation state")
        verbose_name_plural = _("Vegetation states")

    def __str__(self):
        return self.label


class VegetationStrata(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Vegetation strata")
        verbose_name_plural = _("Vegetation stratas")

    def __str__(self):
        return self.label


class VegetationThicknessType(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Vegetation thickness type")
        verbose_name_plural = _("Vegetation thickness types")

    def __str__(self):
        return self.label


class VegetationType(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Vegetation type")
        verbose_name_plural = _("Vegetation types")

    def __str__(self):
        return self.label


class WorkType(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Work type")
        verbose_name_plural = _("Work types")

    def __str__(self):
        return self.label


class WorkMaterial(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Work material")
        verbose_name_plural = _("Work materials")

    def __str__(self):
        return self.label


class WorkState(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Work state")
        verbose_name_plural = _("Work states")

    def __str__(self):
        return self.label


class WorkBankEffect(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Work bank effect")
        verbose_name_plural = _("Work bank effects")

    def __str__(self):
        return self.label


class WorkStreamInfluence(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Work stream influence")
        verbose_name_plural = _("Work stream influences")

    def __str__(self):
        return self.label


class WorkSedimentEffect(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Work sediment effect")
        verbose_name_plural = _("Work sediment effects")

    def __str__(self):
        return self.label


class WorkFishContinuityEffect(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Work fish continuity effect")
        verbose_name_plural = _("Work fish continuity effects")

    def __str__(self):
        return self.label


class Knowledge(WatershedPropertiesMixin, TimeStampedModelMixin, ZoningPropertiesMixin,
                AddPropertyBufferMixin, MapEntityMixin, StructureRelated):
    """Model for knowledge"""
    name = models.CharField(max_length=100, null=False, verbose_name=_("Name"))
    knowledge_type = models.ForeignKey(
        'knowledge.KnowledgeType',
        verbose_name=_("Knowledge type"),
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    code = models.CharField(verbose_name=_("Code"), blank=True, default='', max_length=50)
    description = models.TextField(verbose_name=_("Description"), blank=True, help_text="")
    geom = models.GeometryField(srid=settings.SRID, spatial_index=True)

    # generic relations
    interventions = GenericRelation(
        Intervention,
        content_type_field='target_type',
        object_id_field='target_id',
    )

    class Meta:
        verbose_name = _("Knowledge")
        verbose_name_plural = _("Knowledges")

    def __str__(self):
        return self.name

    @property
    def name_display(self):
        return '<a data-pk="%s" href="%s" title="%s" >%s</a>' % (self.pk,
                                                                 self.get_detail_url(),
                                                                 self,
                                                                 self)

    @classmethod
    def get_create_label(cls):
        return _("Add a new knowledge")


class Vegetation(models.Model):
    """Model for Vegetation"""
    knowledge = models.OneToOneField(
        'knowledge.Knowledge',
        verbose_name=_("Knowledge"),
        on_delete=models.CASCADE
    )
    vegetation_type = models.ForeignKey(
        'knowledge.VegetationType',
        verbose_name=_("Vegetation type"),
        on_delete=models.CASCADE
    )
    state = models.ForeignKey(
        'knowledge.VegetationState',
        verbose_name=_("Vegetation state"),
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    thickness = models.ForeignKey(
        'knowledge.VegetationThicknessType',
        verbose_name=_("Thickness type"),
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    stratas = models.ManyToManyField(
        'knowledge.VegetationStrata',
        verbose_name=_("Vegetation Strata"),
        related_name='vegetations'
    )
    age_class_diversity = models.ForeignKey(
        'knowledge.VegetationAgeClassDiversity',
        verbose_name=_("Age class diversity"),
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    specific_diversity = models.ForeignKey(
        'knowledge.VegetationSpecificDiversity',
        verbose_name=_("Specific diversity"),
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    other_information = models.TextField(
        verbose_name=_("Other information"),
        blank=True, default=""
    )

    class Meta:
        verbose_name = _("Vegetation")
        verbose_name_plural = _("Vegetations")

    def __str__(self):
        return str(self.knowledge)


class Work(models.Model):
    """Model for Vegetation"""
    knowledge = models.OneToOneField(
        'knowledge.Knowledge',
        verbose_name=_("Knowledge"),
        on_delete=models.CASCADE
    )
    work_type = models.ForeignKey(
        'knowledge.WorkType',
        verbose_name=_("Work type"),
        related_name='works',
        on_delete=models.CASCADE
    )
    material = models.ForeignKey(
        'knowledge.WorkMaterial',
        verbose_name=_("Work material"),
        related_name='works',
        on_delete=models.CASCADE
    )
    state = models.ForeignKey(
        'knowledge.WorkState',
        verbose_name=_("Work state"),
        null=True, blank=True,
        related_name='works',
        on_delete=models.CASCADE
    )
    downstream_bank_effect = models.ForeignKey(
        'knowledge.WorkBankEffect',
        verbose_name=_("Downstream bank effect"),
        null=True, blank=True,
        related_name='downstream_effect_works',
        on_delete=models.CASCADE
    )
    upstream_bank_effect = models.ForeignKey(
        'knowledge.WorkBankEffect',
        verbose_name=_("Upstream bank effect"),
        null=True, blank=True,
        related_name='upstream_effect_works',
        on_delete=models.CASCADE
    )
    downstream_influence = models.ForeignKey(
        'knowledge.WorkStreamInfluence',
        verbose_name=_("Downstream influence"),
        null=True, blank=True,
        related_name='downstream_effect_works',
        on_delete=models.CASCADE
    )
    upstream_influence = models.ForeignKey(
        'knowledge.WorkStreamInfluence',
        verbose_name=_("Upstream influence"),
        null=True, blank=True,
        related_name='upstream_effect_works',
        on_delete=models.CASCADE
    )
    sediment_effect = models.ForeignKey(
        'knowledge.WorkSedimentEffect',
        verbose_name=_("Sediment effect"),
        null=True, blank=True,
        related_name='works',
        on_delete=models.CASCADE
    )
    fish_continuity_effect = models.ForeignKey(
        'knowledge.WorkFishContinuityEffect',
        verbose_name=_("Fish Continuity effect"),
        null=True, blank=True,
        related_name='works',
        on_delete=models.CASCADE
    )

    usage = models.TextField(verbose_name=_("Usage"), blank=True, default="")
    width = models.FloatField(default=0.0, blank=True, null=True, verbose_name=_("Width"))
    height = models.FloatField(default=0.0, blank=True, null=True, verbose_name=_("Height"))
    length = models.FloatField(default=0.0, null=True, blank=True, verbose_name=_("Length"))
    drop_height = models.FloatField(default=0.0, null=True, blank=True, verbose_name=_("Drop height"))
    filling = models.FloatField(default=0.0, null=True, blank=True, verbose_name=_("Pit height"))

    class Meta:
        verbose_name = _("Work")
        verbose_name_plural = _("Works")

    def __str__(self):
        return str(self.knowledge)


class FollowUpType(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Follow-up type")
        verbose_name_plural = _("Follow-up types")

    def __str__(self):
        return self.label


class FollowUp(TimeStampedModelMixin, WatershedPropertiesMixin, ZoningPropertiesMixin,
               AdministrativeFilesMixin, AddPropertyBufferMixin, MapEntityMixin, StructureRelated):
    """Follow up related to a knowledge or / and an intervention, or standalone."""

    name = models.CharField(verbose_name=_("Name"), max_length=128)
    date = models.DateField(default=datetime.now, verbose_name=_("Date"))

    _geom = models.GeometryField(srid=settings.SRID, spatial_index=True, null=True, blank=True)

    followup_type = models.ForeignKey(
        'FollowUpType',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='followups',
        verbose_name=_("Follow-up type")
    )

    measure_frequency = models.CharField(
        max_length=200, verbose_name=_("Measure frequency"),
        blank=True, default=""
    )

    knowledge = models.ForeignKey(
        'Knowledge',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="followups",
        verbose_name=_("Knowledge"),
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, help_text="")

    # Technical information
    length = models.FloatField(default=0.0, blank=True, null=True, verbose_name=_("Length"))
    width = models.FloatField(default=0.0, blank=True, null=True, verbose_name=_("Width"))
    height = models.FloatField(default=0.0, blank=True, null=True, verbose_name=_("Height"))

    # generic relations
    administrative_operations = GenericRelation(AdministrativeOperation)

    class Meta:
        verbose_name = _("Follow-up")
        verbose_name_plural = _("Follow-ups")

    @classmethod
    def get_create_label(cls):
        return _("Add a new follow-up")

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
    def knowledge_display(self):
        """Return html to display knowledge"""
        if not self.knowledge:
            return ""
        icon = self.knowledge._meta.model_name
        title = str(self.knowledge)
        url = self.knowledge.get_detail_url()
        return '<img src="{}images/{}-16.png"> <a href={}>{}</a>'.format(
            settings.STATIC_URL,
            icon,
            url,
            title)

    @property
    def geom(self):
        if self._geom is None:
            if self.knowledge:
                self._geom = getattr(self.knowledge, 'geom')
        return self._geom

    @geom.setter
    def geom(self, value):
        self._geom = value

    @property
    def api_geom(self):
        if not self.geom:
            return None
        return self.geom.transform(settings.API_SRID, clone=True)

    def __str__(self):
        return self.name


class FollowUpMeasure(models.Model):
    """Follow up measure"""

    follow_up = models.ForeignKey(
        'FollowUp',
        on_delete=models.CASCADE,
        related_name="measures",
        verbose_name=_("Follow-up"),
    )

    date = models.DateField(default=datetime.now, verbose_name=_("Date"))
    results = models.TextField(verbose_name=_("Results"))
