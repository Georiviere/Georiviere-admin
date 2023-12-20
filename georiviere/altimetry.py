from geotrek.altimetry.models import AltimetryMixin as BaseAltimetryMixin


class AltimetryMixin(BaseAltimetryMixin):
    class Meta:
        abstract = True
