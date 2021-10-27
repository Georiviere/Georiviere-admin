from geotrek.altimetry.models import AltimetryMixin as BaseAltimetryMixin

from georiviere.functions import ElevationInfos, Length3D


class AltimetryMixin(BaseAltimetryMixin):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        elevation_infos = self._meta.model.objects.filter(pk=self.pk) \
            .annotate(infos=ElevationInfos('geom')).first().infos
        draped_geom = elevation_infos.get('draped')
        self.geom_3d = draped_geom
        self.slope = elevation_infos.get('slope')
        self.min_elevation = elevation_infos.get('min_elevation')
        self.max_elevation = elevation_infos.get('max_elevation')
        self.ascent = elevation_infos.get('positive_gain')
        self.descent = elevation_infos.get('negative_gain')
        compute_results = self._meta.model.objects.filter(pk=self.pk) \
            .annotate(length_3d=Length3D(draped_geom)).first()
        self.length = compute_results.length_3d
        super().save(force_insert=False,
                     update_fields=[
                         'geom_3d',
                         'slope',
                         'min_elevation',
                         'max_elevation',
                         'ascent',
                         'descent',
                         'length'
                     ])
