from colorfield.fields import ColorField
from django.db import models

from django.utils.translation import gettext_lazy as _

from geotrek.common.mixins import TimeStampedModelMixin


class Portal(TimeStampedModelMixin, models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=50, unique=True, help_text=_("Name of the portal"))
    website = models.URLField(verbose_name=_("Website"), max_length=256, unique=True)
    title = models.CharField(verbose_name=_("Title"), max_length=50, help_text=_("Title on Georiviere"),
                             default='')
    description = models.TextField(verbose_name=_("Description"), help_text=_("Description on Georiviere"),
                                   default='')
    main_color = ColorField(verbose_name=_("Main color"), default='#444444',
                            help_text=_("Main color"))

    class Meta:
        verbose_name = _("Portal")
        verbose_name_plural = _("Portals")
        ordering = ('name',)

    def __str__(self):
        return self.name
