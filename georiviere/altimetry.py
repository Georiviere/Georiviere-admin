from geotrek.altimetry.models import AltimetryMixin as BaseAltimetryMixin
from geotrek.common.mixins import TimeStampedModelMixin


class AltimetryMixin(BaseAltimetryMixin):
    def refresh(self):
        # Update object's computed values (reload from database)
        if self.pk:
            fromdb = self.__class__.objects.get(pk=self.pk)
            BaseAltimetryMixin.reload(self, fromdb)
            TimeStampedModelMixin.reload(self, fromdb)
        return self

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.refresh()

    class Meta:
        abstract = True
