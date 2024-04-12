from django.contrib.gis.db import models
from django.db.models.fields.json import KeyTextTransform


class SelectableUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(userprofile__isnull=False)


class CustomContributionManager(models.Manager):
    def with_type_values(self, custom_type):
        annotations = {}
        qs = self.get_queryset()
        for field in custom_type.fields.all():
            annotations[field.key] = models.Value(KeyTextTransform(field.key, 'properties'),
                                                  output_field=field.value_type.get_field_type())
        if annotations:
            qs = qs.annotate(**annotations).omit('properties')
        return qs
