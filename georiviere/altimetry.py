from geotrek.altimetry.models import AltimetryMixin as BaseAltimetryMixin


class AltimetryMixin(BaseAltimetryMixin):
    def reload(self, *args, **kwargs):
        # Update object's computed values (reload from database)
        if self.pk:
            fromdb = self.__class__.objects.get(pk=self.pk)
            super().reload(fromdb)
        return self

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.reload()

    class Meta:
        abstract = True
