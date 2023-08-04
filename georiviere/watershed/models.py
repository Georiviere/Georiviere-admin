from colorfield.fields import ColorField

from django.conf import settings
from django.contrib.gis.db import models

from django.utils.translation import gettext_lazy as _


class WatershedType(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    color = ColorField(verbose_name=_("Color"), default='#444444', help_text=_("Color shown on map"))
    portals = models.ManyToManyField('portal.Portal',
                                     blank=True, related_name='watersheds',
                                     verbose_name=_("Published portals"))

    class Meta:
        verbose_name = _("Watershed type")

    def __str__(self):
        return self.name


class Watershed(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("Name"))
    geom = models.MultiPolygonField(srid=settings.SRID, spatial_index=True)
    eid = models.CharField(verbose_name=_("External id"), max_length=1024, blank=True, null=True, default=None,
                           unique=True)
    watershed_type = models.ForeignKey(WatershedType, verbose_name=_("Watershed"), on_delete=models.PROTECT)

    class Meta:
        ordering = ['watershed_type', 'name']
        verbose_name = _("Watershed")
        verbose_name_plural = _("Watersheds")

    def __str__(self):
        return "{} - {}".format(self.watershed_type.name, self.name)
