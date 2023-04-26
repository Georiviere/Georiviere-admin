from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.test import RequestFactory
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from geotrek.common.forms import CommonForm
from georiviere.flatpages.models import FlatPage, FlatPagePicture
from georiviere.flatpages.widgets import AdminFileWidget


if 'modeltranslation' in settings.INSTALLED_APPS:
    from modeltranslation.settings import AVAILABLE_LANGUAGES


class FlatPagePictureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rooturl = RequestFactory().get('/').build_absolute_uri('/')
        self.fields['picture'].widget = AdminFileWidget(attrs={'rooturl': rooturl})

    class Meta:
        model = FlatPagePicture
        fields = (
            'picture', 'flatpage'
        )


class FlatPageForm(CommonForm):
    content = forms.CharField(label=_("Content"), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['class'] = 'tiny-class'
        self.fields['portals'].help_text = None

    class Meta:
        model = FlatPage
        fields = (
            'title', 'order', 'portals', 'external_url', 'content',
        )

    def clean(self):
        cleaned_data = super().clean()
        for lang in AVAILABLE_LANGUAGES:
            external_url = cleaned_data.get('external_url', None)

            # Test if HTML was filled
            # Use strip_tags() to catch empty tags (e.g. ``<p></p>``)
            html_content = cleaned_data.get('content_{}'.format(lang), None) or ''
            if external_url and external_url.strip() and strip_tags(html_content):
                raise ValidationError(_('Choose between external URL and HTML content'))

        return cleaned_data

