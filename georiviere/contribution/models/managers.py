from django.contrib.gis.db import models
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Cast


class SelectableUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(userprofile__isnull=False)


class CustomContributionManager(models.Manager):
    def with_type_values(self, custom_type):
        annotations = {}
        qs = self.get_queryset()
        for field in custom_type.fields.all():
            output_field = models.CharField()
            if field.value_type == 'integer':
                output_field = models.IntegerField()
            elif field.value_type == 'float':
                output_field = models.FloatField()
            elif field.value_type == 'boolean':
                output_field = models.BooleanField()
            elif field.value_type == 'date':
                output_field = models.DateField()
            elif field.value_type == 'datetime':
                output_field = models.DateTimeField()
            annotations[field.key] = Cast(KeyTextTransform(field.key, 'data'), output_field=output_field)
        if annotations:
            qs = qs.annotate(**annotations)
        return qs
