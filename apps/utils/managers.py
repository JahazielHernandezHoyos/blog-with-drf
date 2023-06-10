from django.db import models


class ModelQuerySet(models.QuerySet):
    def all(self):
        return self.filter(deleted=False)

    def deleted(self):
        return self.filter(deleted=True)


class ModelManager(models.Manager):
    def get_queryset(self):
        return ModelQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    def deleted(self):
        return self.get_queryset().deleted()