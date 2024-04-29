from django.db import models
from georiviere.utils.mixins.managers import TruncateManagerMixin


class RiverManager(TruncateManagerMixin, models.Manager):
    pass
