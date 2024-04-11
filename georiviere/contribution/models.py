import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.core.mail import mail_managers
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from geotrek.common.mixins import BasePublishableMixin, TimeStampedModelMixin
from geotrek.common.utils import classproperty
from geotrek.zoning.mixins import ZoningPropertiesMixin
from mapentity.models import MapEntityMixin

from georiviere.description.models import Morphology, Status, Usage
from georiviere.knowledge.models import Knowledge
from georiviere.main.models import AddPropertyBufferMixin
from georiviere.observations.models import Station
from georiviere.proceeding.models import Proceeding
from georiviere.river.models import Stream
from georiviere.studies.models import Study
from georiviere.watershed.mixins import WatershedPropertiesMixin

from .managers import SelectableUserManager

logger = logging.getLogger(__name__)


class SeverityType(models.Model):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Severity type")
        verbose_name_plural = _("Severity types")

    def __str__(self):
        return self.label


class ContributionStatus(TimeStampedModelMixin, models.Model):
    label = models.CharField(verbose_name=_("Status"), max_length=128)

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Status")

    def __str__(self):
        return self.label


class SelectableUser(User):
    objects = SelectableUserManager()

    class Meta:
        proxy = True


def status_default():
    """Set status to New by default"""
    new_status_query = ContributionStatus.objects.filter(label="Informé")
    if new_status_query:
        return new_status_query.get().pk
    return None


class Contribution(BasePublishableMixin, TimeStampedModelMixin, WatershedPropertiesMixin, ZoningPropertiesMixin,
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
    published = models.BooleanField(verbose_name=_("Published"), default=False,
                                    help_text=_("Make it visible on portal"))
    portal = models.ForeignKey('portal.Portal',
                               verbose_name=_("Portal"), blank=True, related_name='contributions',
                               on_delete=models.PROTECT)
    assigned_user = models.ForeignKey(
        SelectableUser,
        blank=True,
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_("Supervisor"),
        related_name="contributions"
    )
    status_contribution = models.ForeignKey(
        "ContributionStatus",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        default=status_default,
        verbose_name=_("Status"),
    )
    validated = models.BooleanField(verbose_name=_("Validated"), default=False,
                                    help_text=_("Validate the contribution"))
    linked_object_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    linked_object_id = models.PositiveIntegerField(blank=True, null=True)
    linked_object = GenericForeignKey('linked_object_type', 'linked_object_id')

    class Meta:
        verbose_name = _("Contribution")
        verbose_name_plural = _("Contributions")

    @classproperty
    def category_verbose_name(cls):
        return _("Category")

    @classproperty
    def type_verbose_name(cls):
        return _("Type")

    @classproperty
    def linked_object_verbose_name(cls):
        return _("Linked object")

    @property
    def linked_object_model_name(self):
        if self.linked_object:
            return self.linked_object._meta.verbose_name
        return None

    def __str__(self):
        # Use the category and the type (One to One field) to generate what it will show on the list / detail / etc...
        # It will generate like that :
        # test@test.test Potential Damage Landing
        if hasattr(self, 'potential_damage'):
            return f'{self.email_author} {ContributionPotentialDamage._meta.verbose_name.title()} ' \
                   f'{self.potential_damage.get_type_display()}'
        elif hasattr(self, 'fauna_flora'):
            return f'{self.email_author} {ContributionFaunaFlora._meta.verbose_name.title()} ' \
                   f'{self.fauna_flora.get_type_display()}'
        elif hasattr(self, 'quality'):
            return f'{self.email_author} {ContributionQuality._meta.verbose_name.title()} ' \
                   f'{self.quality.get_type_display()}'
        elif hasattr(self, 'quantity'):
            return f'{self.email_author} {ContributionQuantity._meta.verbose_name.title()} ' \
                   f'{self.quantity.get_type_display()}'
        elif hasattr(self, 'landscape_element'):
            return f'{self.email_author} {ContributionLandscapeElements._meta.verbose_name.title()} ' \
                   f'{self.landscape_element.get_type_display()}'
        return f'{self.email_author}'

    @property
    def category(self):
        # The category is the reverse of the one to one fields :
        # For example :
        # Potential damage
        if hasattr(self, 'potential_damage'):
            return self.potential_damage
        elif hasattr(self, 'fauna_flora'):
            return self.fauna_flora
        elif hasattr(self, 'quality'):
            return self.quality
        elif hasattr(self, 'quantity'):
            return self.quantity
        elif hasattr(self, 'landscape_element'):
            return self.landscape_element
        return _('No category')

    @property
    def type(self):
        if hasattr(self.category, 'get_type_display'):
            return self.category.get_type_display()
        return _('No type')

    @property
    def category_display(self):
        s = '<a data-pk="%s" href="%s" title="%s" >%s</a>' % (self.pk,
                                                              self.get_detail_url(),
                                                              self.category,
                                                              self.category)
        if self.published:
            s = '<span class="badge badge-success" title="%s">&#x2606;</span> ' % _("Published") + s
        return s

    def send_report_to_managers(self, template_name="contribution/report_email.txt"):
        # Send report to managers when a contribution has been created (MANAGERS settings)
        subject = _("Feedback from {email}").format(email=self.email_author)
        message = render_to_string(template_name, {"contribution": self})
        mail_managers(subject, message, fail_silently=False)

    def try_send_report_to_managers(self):
        try:
            self.send_report_to_managers()
        except Exception as e:
            logger.error("Email could not be sent to managers.")
            logger.exception(e)  # This sends an email to admins :)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Contribution updates should do nothing more
        self.try_send_report_to_managers()


# Contributions has a category in the list :
# Potential damage
# Fauna flora
# Quality
# Quantity
# Landscape elements

# Contributions has a type depending on its category
# Potential damage => Landing, Excessive cutting of riparian forest, Rockslides, Disruptive jam, Bank erosion
#                     River bed incision (sinking), Fish diseases (appearance of fish), Fish mortality,
#                     Trampling by livestock (impacting)
# Fauna flora => Invasive species, Heritage species, Fish species
# Quantity => Dry, In the process of drying out, Overflow
# Quality => Algal development, Pollution, Water temperature
# Landscape elements => Sinkhole, Fountain, Chasm, Lesine, Pond, Losing stream, Resurgence

# Depending on its type of contribution, some fields are available or not.
# Everything is summarize on :
# https://github.com/Georiviere/Georiviere-admin/issues/139


class LandingType(models.Model):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)

    class Meta:
        verbose_name = _("Landing type")
        verbose_name_plural = _("Landing types")

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
    landing_type = models.ForeignKey(LandingType, on_delete=models.PROTECT, null=True,
                                     verbose_name=_("Landing type"))
    excessive_cutting_length = models.FloatField(default=0.0, null=True, blank=True,
                                                 verbose_name=_("Excessive cutting length (in meters)"))
    jam_type = models.ForeignKey(JamType, on_delete=models.PROTECT, null=True)
    length_bank_erosion = models.FloatField(default=0.0, null=True, blank=True,
                                            verbose_name=_("Length bank erosion (in meters)"),
                                            help_text=_('Distance between the foot of the bank and the foot of '
                                                        'the erosion.'))
    bank_height = models.FloatField(default=0.0, null=True, blank=True,
                                    verbose_name=_("Bank height (in meters)"),
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
                                  verbose_name=_("Home area (in square meters)"),
                                  help_text=_('Home area in square meters'))
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

    type = models.IntegerField(
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
        return f'{ContributionQuantity._meta.verbose_name.title()} {self.get_type_display()}'


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

    type = models.IntegerField(
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
        return f'{ContributionQuality._meta.verbose_name.title()} {self.get_type_display()}'


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
                                        related_name='landscape_element')

    class Meta:
        verbose_name = _("Contribution landscape element")
        verbose_name_plural = _("contributions landscape elements")

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


## Custom Contribution

class CustomContributionType(models.Model):
    label = models.CharField(max_length=128, verbose_name=_("Label"), unique=True)
    linked_to_station = models.BooleanField(default=False, verbose_name=_("Linked to station"))

    class Meta:
        verbose_name = _("Custom contribution type")
        verbose_name_plural = _("Custom contribution types")

    def __str__(self):
        return self.label


class CustomContributionTypeField(models.Model):
    class FieldTypeChoices(models.TextChoices):
        """Choices for field type"""
        TEXT = 'text', _('Text')
        INTEGER = 'integer', _('Integer')
        FLOAT = 'float', _('Float')
        DATE = 'date', _('Date')
        DATETIME = 'datetime', _('Datetime')
        BOOLEAN = 'boolean', _('Boolean')

        @classmethod
        def get_model_field(self, field_type):
            if field_type == self.TEXT:
                return models.CharField
            if field_type == self.INTEGER:
                return models.IntegerField
            if field_type == self.FLOAT:
                return models.FloatField
            if field_type == self.DATE:
                return models.DateField
            if field_type == self.DATETIME:
                return models.DateTimeField
            if field_type == self.BOOLEAN:
                return models.BooleanField


    label = models.CharField(max_length=128, verbose_name=_("Label"))
    key = models.SlugField(max_length=150, verbose_name=_("Key"), help_text="Key used in JSON field", editable=False)
    value_type = models.CharField(max_length=16, verbose_name=_("Type"),
                                  choices=FieldTypeChoices.choices, default=FieldTypeChoices.TEXT)
    required = models.BooleanField(default=False, verbose_name=_("Required"))
    options = models.JSONField(null=False, blank=True, default=dict)
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Order"))
    custom_type = models.ForeignKey(CustomContributionType, on_delete=models.CASCADE, related_name='fields')

    def __str__(self):
        return f"{self.label}: ({self.value_type})"

    def get_slug_as_field_name(self, label):
        return slugify(label).replace('-', '_')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = self.get_slug_as_field_name(self.label)
        return super().save(*args, **kwargs)

    def get_form_field(self, initial=None):
        options = self.options.copy()
        if initial:
            options.update(initial)
        return self.FieldTypeChoices.get_model_field(self.value_type)().formfield(label=self.label, required=self.required, **self.options)

    class Meta:
        verbose_name = _("Custom contribution type field")
        verbose_name_plural = _("Custom contribution type fields")
        unique_together = (
            ('label', 'custom_type'),  # label by type should be unique
        )


class CustomContribution(TimeStampedModelMixin, models.Model):
    geom = models.GeometryField(srid=settings.SRID, spatial_index=True)
    custom_type = models.ForeignKey(CustomContributionType, on_delete=models.PROTECT,
                                    related_name='contributions')
    properties = models.JSONField(null=False, blank=True, default=dict)
    portal = models.ForeignKey('portal.Portal', verbose_name=_("Portal"), blank=True, null=True, related_name='custom_contributions',
                               on_delete=models.PROTECT)
    validated = models.BooleanField(default=False, verbose_name=_("Validated"))

    class Meta:
        verbose_name = _("Custom contribution")
        verbose_name_plural = _("Custom contributions")

    def __str__(self):
        return f"{self.custom_type.label} - {self.pk}"

    def get_properties(self):
        return self.properties

    def set_properties(self, properties):
        self.properties = properties
