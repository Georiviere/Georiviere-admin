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
        ordering = ['label']

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
        ordering = ['label']

    def __str__(self):
        return self.label


class VegetationStrata(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Vegetation strata")
        verbose_name_plural = _("Vegetation stratas")
        ordering = ['label']

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
        ordering = ['label']

    def __str__(self):
        return self.label


class WorkType(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Work type")
        verbose_name_plural = _("Work types")
        ordering = ['label']

    def __str__(self):
        return self.label


class WorkMaterial(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Work material")
        verbose_name_plural = _("Work materials")
        ordering = ['label']

    def __str__(self):
        return self.label


class WorkState(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Work state")
        verbose_name_plural = _("Work states")
        ordering = ['label']

    def __str__(self):
        return self.label


class WorkBankEffect(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Work bank effect")
        verbose_name_plural = _("Work bank effects")
        ordering = ['label']

    def __str__(self):
        return self.label


class WorkStreamInfluence(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Work stream influence")
        verbose_name_plural = _("Work stream influences")

    def __str__(self):
        return self.label


class WorkWaterEffect(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Work water effect")
        verbose_name_plural = _("Work water effects")
        ordering = ['label']

    def __str__(self):
        return self.label


class WorkBedEffect(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Work bed effect")
        verbose_name_plural = _("Work bed effects")
        ordering = ['label']

    def __str__(self):
        return self.label


class WorkSedimentEffect(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Work sediment effect")
        verbose_name_plural = _("Work sediment effects")
        ordering = ['label']

    def __str__(self):
        return self.label


class WorkFishContinuityEffect(models.Model):
    label = models.CharField(verbose_name=_("Label"), max_length=128)

    class Meta:
        verbose_name = _("Work fish continuity effect")
        verbose_name_plural = _("Work fish continuity effects")
        ordering = ['label']

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

    contributions = GenericRelation(
        'contribution.Contribution',
        content_type_field='linked_object_type',
        object_id_field='linked_object_id',
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
        verbose_name=_("Vegetation Stratas"),
        blank=True,
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
    water_effect = models.ForeignKey(
        'knowledge.WorkWaterEffect',
        verbose_name=_("Water effect"),
        null=True, blank=True,
        related_name='works',
        on_delete=models.CASCADE
    )
    upstream_bed_effect = models.ForeignKey(
        'knowledge.WorkBedEffect',
        verbose_name=_("Upstream bed effect"),
        null=True, blank=True,
        related_name='upstream_effect_works',
        on_delete=models.CASCADE
    )
    downstream_bed_effect = models.ForeignKey(
        'knowledge.WorkBedEffect',
        verbose_name=_("Downstream bed effect"),
        null=True, blank=True,
        related_name='downstream_effect_works',
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
    contributions = GenericRelation(
        'contribution.Contribution',
        content_type_field='linked_object_type',
        object_id_field='linked_object_id',
    )

    # generic relations
    administrative_operations = GenericRelation(AdministrativeOperation)

    class Meta:
        verbose_name = _("Follow-up")
        verbose_name_plural = _("Follow-ups")

    @classmethod
    def within_buffer_without_knowledge(cls, topology):
        area = topology.geom.buffer(settings.BASE_INTERSECTION_MARGIN)
        qs = cls.objects.filter(_geom__intersects=area).filter(knowledge__isnull=True)
        return qs

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


class OfflineKnowledge(models.Model):
    uuid = models.TextField(primary_key=True)
    gra_id = models.IntegerField(null=True)  # FK on 'knowledge.Knowledge'
    geom = models.GeometryField(srid=settings.SRID, spatial_index=True, null=True)
    name = models.TextField(null=True)
    code = models.TextField(null=True)
    description = models.TextField(null=True)
    date_insert = models.DateTimeField(null=True)
    date_update = models.DateTimeField(null=True)
    knowledge_type = models.IntegerField(null=True)  # FK on 'knowledge.KnowledgeType'
    # Fields from vegetation 1-to-1
    vegetation_type = models.IntegerField(null=True)  # FK on 'knowledge.VegetationType'
    vegetation_state = models.IntegerField(null=True)  # FK on 'knowledge.VegetationState'
    thickness = models.IntegerField(null=True)  # FK on 'knowledge.VegetationThicknessType'
    age_class_diversity = models.IntegerField(null=True)  # FK on 'knowledge.VegetationAgeClassDiversity'
    specific_diversity = models.IntegerField(null=True)  # FK on 'knowledge.VegetationSpecificDiversity'
    other_information = models.TextField(null=True)
    # Fields from work 1-to-1
    work_type = models.IntegerField(null=True)  # FK on 'knowledge.WorkType'
    material = models.IntegerField(null=True)  # FK on 'knowledge.WorkMaterial'
    work_state = models.IntegerField(null=True)  # FK on 'knowledge.WorkState'
    downstream_bank_effect = models.IntegerField(null=True)  # FK on 'knowledge.WorkBankEffect'
    upstream_bank_effect = models.IntegerField(null=True)  # FK on 'knowledge.WorkBankEffect'
    downstream_influence = models.IntegerField(null=True)  # FK on 'knowledge.WorkStreamInfluence'
    upstream_influence = models.IntegerField(null=True)  # FK on 'knowledge.WorkStreamInfluence'
    sediment_effect = models.IntegerField(null=True)  # FK on 'knowledge.WorkSedimentEffect'
    water_effect = models.IntegerField(null=True)  # FK on 'knowledge.WorkWaterEffect'
    upstream_bed_effect = models.IntegerField(null=True)  # FK on 'knowledge.WorkBedEffect'
    downstream_bed_effect = models.IntegerField(null=True)  # FK on 'knowledge.WorkBedEffect'
    fish_continuity_effect = models.IntegerField(null=True)  # FK on 'knowledge.WorkFishContinuityEffect'
    usage = models.TextField(null=True)
    width = models.FloatField(null=True)
    height = models.FloatField(null=True)
    length = models.FloatField(null=True)
    drop_height = models.FloatField(null=True)
    filling = models.FloatField(null=True)
    username = models.TextField(null=True)


class OfflineKnowledgeVegetationStrata(models.Model):
    uuid = models.TextField(primary_key=True)
    vegetation_strata_id = models.IntegerField(null=True)  # FK on VegetationStrata
    knowledge_uuid = models.TextField(null=True)  # FK on OfflineKnowledge

class OfflineFollowup(models.Model):
    uuid = models.TextField(primary_key=True)
    gra_id = models.IntegerField(null=True)  # FK on 'knowledge.FollowUp'
    geom = models.GeometryField(srid=settings.SRID, spatial_index=True, null=True)
    knowledge_uuid = models.TextField(null=True)  # FK on 'OfflineKnowledge'
    name = models.CharField(max_length=128, null=True)
    date = models.DateField(null=True)
    measure_frequency = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    length = models.FloatField(default=0.0, null=True)
    width = models.FloatField(default=0.0, null=True)
    height = models.FloatField(default=0.0, null=True)
    date_insert = models.DateTimeField(null=True)
    date_update = models.DateTimeField(null=True)
    followup_type = models.IntegerField(null=True)  # FK on 'FollowUpType'
    username = models.TextField(null=True)
