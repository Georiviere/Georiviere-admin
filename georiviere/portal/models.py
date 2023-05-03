from colorfield.fields import ColorField
from django.conf import settings
from django.contrib.gis.db.models import PolygonField
from django.db import models

from django.utils.translation import gettext_lazy as _

from geotrek.common.mixins import TimeStampedModelMixin


class MapBaseLayer(models.Model):
    label = models.CharField(max_length=50, unique=True)
    order = models.PositiveSmallIntegerField(default=0)
    url = models.CharField(max_length=255, blank=True, help_text=_("URL"))
    min_zoom = models.PositiveSmallIntegerField(default=0)
    max_zoom = models.PositiveSmallIntegerField(default=22)
    attribution = models.CharField(max_length=255, blank=True,
                                   help_text=_("Attribution of the baselayer. Example : '© OpenStreetMap"))
    bounds = models.CharField(max_length=255, blank=True, help_text=_("Bounds"))

    class Meta:
        verbose_name = _("Map base layer")
        verbose_name_plural = _("Map base layers")
        ordering = ('label',)

    def __str__(self):
        return self.label


class MapOverlayGroupLayer(models.Model):
    label = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField(default=0)
    layers = models.ManyToManyField('portal.MapOverlayLayer',
                                    verbose_name=_("Overlay layers"))

    class Meta:
        verbose_name = _("Map overlay group")
        verbose_name_plural = _("Map overlay groups")
        ordering = ('label',)

    def __str__(self):
        return self.label


class MapOverlayLayer(models.Model):
    label = models.CharField(max_length=50)
    url = models.CharField(max_length=255, blank=False, help_text=_("URL of the layer"), unique=True)
    default_active = models.BooleanField(default=False)
    style = models.JSONField(max_length=300, null=False, blank=False, default=dict, help_text=_("Style of the layer"))
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = _("Map overlay layer")
        verbose_name_plural = _("Map overlay layers")
        ordering = ('label',)
        unique_together = ('label', 'order')

    def __str__(self):
        return self.label


class Portal(TimeStampedModelMixin, models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=50, unique=True, help_text=_("Name of the portal"))
    website = models.URLField(verbose_name=_("Website"), max_length=256, unique=True)
    title = models.CharField(verbose_name=_("Title"), max_length=50, help_text=_("Title on Georiviere"),
                             default='')
    description = models.TextField(verbose_name=_("Description"), help_text=_("Description on Georiviere"),
                                   default='')
    main_color = ColorField(verbose_name=_("Main color"), default='#444444',
                            help_text=_("Main color"))
    map_base_layers = models.ManyToManyField('portal.MapBaseLayer', verbose_name=_("Map base layers"))
    map_group_overlay_layers = models.ManyToManyField('portal.MapOverlayGroupLayer',
                                                      verbose_name=_("Map group overlay layers"))
    min_zoom = models.PositiveSmallIntegerField(default=0)
    max_zoom = models.PositiveSmallIntegerField(default=22)
    spatial_extent = PolygonField(srid=settings.SRID, null=True)

    class Meta:
        verbose_name = _("Portal")
        verbose_name_plural = _("Portals")
        ordering = ('name',)

    def __str__(self):
        return self.name
