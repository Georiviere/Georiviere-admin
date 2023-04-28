from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from geotrek.common.forms import CommonForm
from georiviere.flatpages.models import FlatPage, FlatPagePicture
from georiviere.flatpages.widgets import AdminFileWidget


class FlatPagePictureForm(forms.ModelForm):

    class Meta:
        model = FlatPagePicture
        fields = (
            'picture', 'flatpage'
        )


class FlatPagePictureFormSet(forms.BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for form in self.forms:
            rooturl = self.request.build_absolute_uri('/')
            form.fields['picture'].widget = AdminFileWidget(attrs={'rooturl': rooturl})


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
        external_url = cleaned_data.get('external_url', None)

        # Test if HTML was filled
        # Use strip_tags() to catch empty tags (e.g. ``<p></p>``)
        html_content = cleaned_data.get('content', None) or ''
        if external_url and external_url.strip() and strip_tags(html_content):
            raise ValidationError(_('Choose between external URL and HTML content'))

        return cleaned_data
