from django.conf import settings
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from mapentity.models import MapEntityMixin

from geotrek.common.mixins import TimeStampedModelMixin
from geotrek.common.utils import classproperty
from geotrek.zoning.mixins import ZoningPropertiesMixin

from georiviere.description.models import Status, Morphology, Usage
from georiviere.river.models import Stream
from georiviere.knowledge.models import Knowledge
from georiviere.main.models import AddPropertyBufferMixin
from georiviere.observations.models import Station
from georiviere.proceeding.models import Proceeding
from georiviere.studies.models import Study
from georiviere.watershed.mixins import WatershedPropertiesMixin


class SeverityType(models.Model):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Severity type")
        verbose_name_plural = _("Severity types")

    def __str__(self):
        return self.label


class Contribution(TimeStampedModelMixin, WatershedPropertiesMixin, ZoningPropertiesMixin,
                   AddPropertyBufferMixin, MapEntityMixin):
    """contribution model"""
    geom = models.GeometryField(srid=settings.SRID, spatial_index=True)
    name_author = models.CharField(max_length=128, verbose_name=_("Name author"), blank=True)
    first_name_author = models.CharField(max_length=128, verbose_name=_("First name author"), blank=True)
    email_author = models.EmailField(verbose_name=_("Email"))
    date_observation = models.DateTimeField(editable=True, verbose_name=_("Observation's date"))
    severity = models.ForeignKey(SeverityType, verbose_name=_("Severity"), on_delete=models.PROTECT, null=True,
                                 blank=True, related_name='contributions')
    description = models.TextField(verbose_name=_("Description"), help_text=_("Description of the contribution"),
                                   blank=True)
    portal = models.ForeignKey('portal.Portal',
                               verbose_name=_("Portal"), blank=True, related_name='contributions',
                               on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("Contribution")
        verbose_name_plural = _("Contributions")

    @classproperty
    def category_verbose_name(cls):
        return _("Name")

    def __str__(self):
        if hasattr(self, 'potential_damage'):
            return f'{self.email_author} {ContributionPotentialDamage._meta.verbose_name.title()} ' \
                   f'{self.potential_damage.get_type_display()}'
        elif hasattr(self, 'fauna_flora'):
            return f'{self.email_author} {ContributionFaunaFlora._meta.verbose_name.title()} ' \
                   f'{self.fauna_flora.get_type_display()}'
        elif hasattr(self, 'quality'):
            return f'{self.email_author} {ContributionQuality._meta.verbose_name.title()} ' \
                   f'{self.quality.get_quality_water_type_display()}'
        elif hasattr(self, 'quantity'):
            return f'{self.email_author} {ContributionQuantity._meta.verbose_name.title()} ' \
                   f'{self.quantity.get_water_level_type_display()}'
        elif hasattr(self, 'landscape_elements'):
            return f'{self.email_author} {ContributionLandscapeElements._meta.verbose_name.title()} ' \
                   f'{self.landscape_elements.get_type_display()}'
        return f'{self.email_author}'

    @property
    def category(self):
        if hasattr(self, 'potential_damage'):
            return self.potential_damage
        elif hasattr(self, 'fauna_flora'):
            return self.fauna_flora
        elif hasattr(self, 'quality'):
            return self.quality
        elif hasattr(self, 'quantity'):
            return self.quantity
        elif hasattr(self, 'landscape_elements'):
            return self.landscape_elements
        return _('No category')

    @property
    def category_display(self):
        return '<a data-pk="%s" href="%s" title="%s" >%s</a>' % (self.pk,
                                                                 self.get_detail_url(),
                                                                 self.category,
                                                                 self.category)


class LandingType(models.Model):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Contribution potential damage type")
        verbose_name_plural = _("Contribution potential damage types")

    def __str__(self):
        return self.label


class JamType(models.Model):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Jam type")
        verbose_name_plural = _("Jam types")

    def __str__(self):
        return self.label


class DiseaseType(models.Model):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Disease type")
        verbose_name_plural = _("Disease types")

    def __str__(self):
        return self.label


class DeadSpecies(models.Model):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Dead species")
        verbose_name_plural = _("Dead species")

    def __str__(self):
        return self.label


class ContributionPotentialDamage(models.Model):

    class TypeChoice(models.IntegerChoices):
        """Choices for local influence"""
        LANDING = 1, _('Landing')
        EXCESSIVE_CUTTING_RIPARIAN_FOREST = 2, _('Excessive cutting of riparian forest')
        ROCKSLIDES = 3, _('Rockslides')
        DISRUPTIVE_JAM = 4, _('Disruptive jam')
        BANK_EROSION = 5, _('Bank erosion')
        RIVER_BED_INCISION = 6, _('River bed incision (sinking)')
        FISH_DISEASES = 7, _('Fish diseases (appearance of fish)')
        FISH_MORTALITY = 8, _('Fish mortality')
        TRAMPLING_LIVESTOCK = 9, _('Trampling by livestock (impacting)')

    type = models.IntegerField(
        null=False,
        choices=TypeChoice.choices,
        default=TypeChoice.LANDING,
        verbose_name=_("Type"),
    )
    landing_type = models.ForeignKey(LandingType, on_delete=models.PROTECT, null=True)
    excessive_cutting_length = models.FloatField(default=0.0, null=True, blank=True,
                                                 verbose_name=_("Excessive cutting length in meters"))
    jam_type = models.ForeignKey(JamType, on_delete=models.PROTECT, null=True)
    length_bank_erosion = models.FloatField(default=0.0, null=True, blank=True,
                                            verbose_name=_("Length bank erosoion"),
                                            help_text=_('Distance between the foot of the bank and the foot of '
                                                        'the erosion.'))
    bank_height = models.FloatField(default=0.0, null=True, blank=True,
                                    verbose_name=_("Bank height"),
                                    help_text=_('Bank height (measured between the foot of the bank and the top '
                                                'of the bank) in meters'))
    disease_type = models.ForeignKey(DiseaseType, on_delete=models.PROTECT, null=True)
    number_death = models.IntegerField(default=0, null=True, blank=True,
                                       verbose_name=_("Number death"),
                                       help_text=_('Number of dead individuals'))
    dead_species = models.ForeignKey(DeadSpecies, on_delete=models.PROTECT, null=True)
    contribution = models.OneToOneField(Contribution, parent_link=True, on_delete=models.CASCADE,
                                        related_name='potential_damage')

    class Meta:
        verbose_name = _("Contribution potential damage")
        verbose_name_plural = _("contributions potential damage")

    def __str__(self):
        return f'{ContributionPotentialDamage._meta.verbose_name.title()} {self.get_type_display()}'


class InvasiveSpecies(models.Model):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Invasive species")
        verbose_name_plural = _("Invasive species")

    def __str__(self):
        return self.label


class HeritageSpecies(models.Model):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Heritage species")
        verbose_name_plural = _("Heritage species")

    def __str__(self):
        return self.label


class HeritageObservation(models.Model):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Heritage observation")
        verbose_name_plural = _("Heritage observations")

    def __str__(self):
        return self.label


class FishSpecies(models.Model):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Fish species")
        verbose_name_plural = _("Fish species")

    def __str__(self):
        return self.label


class ContributionFaunaFlora(models.Model):

    class TypeChoice(models.IntegerChoices):
        """Choices for local influence"""
        INVASIVE_SPECIES = 1, _('Invasive species')
        HERITAGE_SPECIES = 2, _('Heritage species')
        FISH_SPECIES = 3, _('Fish species')

    type = models.IntegerField(
        null=False,
        choices=TypeChoice.choices,
        default=TypeChoice.INVASIVE_SPECIES,
        verbose_name=_("Type"),
    )
    home_area = models.FloatField(default=0.0, null=True, blank=True,
                                  verbose_name=_("Home area"),
                                  help_text=_('Home area in meters'))
    invasive_species = models.ForeignKey(InvasiveSpecies, on_delete=models.PROTECT, null=True)
    number_heritage_species = models.IntegerField(default=0, null=True, blank=True,
                                                  verbose_name=_("Number heritage species"))
    heritage_species = models.ForeignKey(HeritageSpecies, on_delete=models.PROTECT, null=True)
    heritage_observation = models.ForeignKey(HeritageObservation, on_delete=models.PROTECT, null=True)
    number_fish_species = models.IntegerField(default=0, null=True, blank=True,
                                              verbose_name=_("Number fish species"))
    fish_species = models.ForeignKey(FishSpecies, on_delete=models.PROTECT, null=True)
    contribution = models.OneToOneField(Contribution, parent_link=True, on_delete=models.CASCADE,
                                        related_name='fauna_flora')

    class Meta:
        verbose_name = _("Contribution fauna-flora")
        verbose_name_plural = _("contributions fauna-flora")

    def __str__(self):
        return f'{ContributionFaunaFlora._meta.verbose_name.title()} {self.get_type_display()}'


class ContributionQuantity(models.Model):
    class TypeChoice(models.IntegerChoices):
        """Choices for local influence"""
        DRY = 1, _('Dry')
        PROCESS_DRYING_OUT = 2, _('In the process of drying out')
        OVERFLOW = 3, _('Overflow')

    water_level_type = models.IntegerField(
        null=False,
        choices=TypeChoice.choices,
        default=TypeChoice.DRY,
        verbose_name=_("Water level type"),
    )
    landmark = models.TextField(blank=True, verbose_name='Landmark')
    contribution = models.OneToOneField(Contribution, parent_link=True, on_delete=models.CASCADE,
                                        related_name='quantity')

    class Meta:
        verbose_name = _("Contribution quantity")
        verbose_name_plural = _("contributions quantity")

    def __str__(self):
        return f'{ContributionQuantity._meta.verbose_name.title()} {self.get_water_level_type_display()}'


class NaturePollution(models.Model):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Nature pollution")
        verbose_name_plural = _("Natures pollution")

    def __str__(self):
        return self.label


class TypePollution(models.Model):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Type pollution")
        verbose_name_plural = _("Types pollution")

    def __str__(self):
        return self.label


class ContributionQuality(models.Model):
    class TypeChoice(models.IntegerChoices):
        """Choices for local influence"""
        ALGAL_DEVELOPMENT = 1, _('Algal development')
        POLLUTION = 2, _('Pollution')
        WATER_TEMPERATURE = 3, _('Water temperature')

    quality_water_type = models.IntegerField(
        null=False,
        choices=TypeChoice.choices,
        default=TypeChoice.ALGAL_DEVELOPMENT,
        verbose_name=_("Quality water type"),
    )
    nature_pollution = models.ForeignKey(NaturePollution, on_delete=models.PROTECT, null=True)
    type_pollution = models.ForeignKey(TypePollution, on_delete=models.PROTECT, null=True)
    contribution = models.OneToOneField(Contribution, parent_link=True, on_delete=models.CASCADE,
                                        related_name='quality')

    class Meta:
        verbose_name = _("Contribution quality")
        verbose_name_plural = _("contributions quality")

    def __str__(self):
        return f'{ContributionQuality._meta.verbose_name.title()} {self.get_quality_water_type_display()}'


class ContributionLandscapeElements(models.Model):
    class TypeChoice(models.IntegerChoices):
        """Choices for local influence"""
        SINKHOLE = 1, _('Sinkhole')
        FOUNTAIN = 2, _('Fountain')
        CHASM = 3, _('Chasm')
        LESINE = 4, _('Lesine')
        POND = 5, _('Pond')
        LOSING_STREAM = 6, _('Losing stream')
        RESURGENCE = 7, _('Resurgence')

    type = models.IntegerField(
        null=False,
        choices=TypeChoice.choices,
        default=TypeChoice.SINKHOLE,
        verbose_name=_("Type"),
    )
    contribution = models.OneToOneField(Contribution, parent_link=True, on_delete=models.CASCADE,
                                        related_name='landscape_elements')

    class Meta:
        verbose_name = _("Contribution quantity")
        verbose_name_plural = _("contributions quantity")

    def __str__(self):
        return f'{ContributionLandscapeElements._meta.verbose_name.title()} {self.get_type_display()}'


Contribution.add_property('streams', Stream.within_buffer, _("Stream"))
Contribution.add_property('status', Status.within_buffer, _("Status"))
Contribution.add_property('morphologies', Morphology.within_buffer, _("Morphologies"))
Contribution.add_property('usages', Usage.within_buffer, _("Usages"))
Contribution.add_property('stations', Station.within_buffer, _("Station"))
Contribution.add_property('studies', Study.within_buffer, _("Study"))
Contribution.add_property('proceedings', Proceeding.within_buffer, _("Proceeding"))
Contribution.add_property('knowledges', Knowledge.within_buffer, _("Knowledge"))
