from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.urls import reverse

from mapentity.serializers import plain_text
from geotrek.common.mixins import TimeStampedModelMixin


class FlatPagePicture(TimeStampedModelMixin):
    picture = models.FileField(verbose_name=_("Pictogram"), upload_to='flatpages',
                               max_length=512, null=True)
    flatpage = models.ForeignKey('flatpages.FlatPage', on_delete=models.PROTECT, related_name='pictures')

    class Meta:
        verbose_name = _('Flat page picture')
        verbose_name_plural = _('Flat page pictures')


class FlatPage(TimeStampedModelMixin):
    """
    Manage *Georiviere* static pages from Georiviere admin.
    """
    title = models.CharField(verbose_name=_('Title'), max_length=200, unique=True)
    external_url = models.URLField(verbose_name=_('External URL'), blank=True, default='',
                                   help_text=_('Link to external website instead of HTML content'))
    content = models.TextField(verbose_name=_('Content'), null=True, blank=True,
                               help_text=_('HTML content'))
    portals = models.ManyToManyField('portal.Portal',
                                     blank=True, related_name='flatpages',
                                     verbose_name=_("Published portals"))
    order = models.IntegerField(default=None, null=True, blank=True,
                                help_text=_("ID order if blank", ),
                                verbose_name=_("Order"), unique=True)
    hidden = models.BooleanField(verbose_name=_("Hidden"), default=False)

    @property
    def slug(self):
        return slugify(self.title)

    class Meta:
        verbose_name = _('Flat page')
        verbose_name_plural = _('Flat pages')
        ordering = ['order', 'id']
        permissions = (
            ("read_flatpage", "Can read FlatPage"),
        )

    def __str__(self):
        return self.title

    def get_permission_codename(self, *args):
        return

    def get_add_url(self):
        return reverse('admin:flatpages_flatpage_add')

    def get_update_url(self):
        return reverse('admin:flatpages_flatpage_change', args=[self.pk])

    def get_delete_url(self):
        return reverse('admin:flatpages_flatpage_delete', args=[self.pk])
