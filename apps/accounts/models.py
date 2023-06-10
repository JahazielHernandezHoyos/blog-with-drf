from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_lifecycle import AFTER_CREATE, BEFORE_UPDATE, hook

from apps.accounts.choices import GENDERS
from apps.accounts.choices import GENDERS, STATUS
from apps.utils.models import BaseModel, BaseModelUser, BaseNameDescriptionModel
from apps.utils.redis import client as redis


class Account(BaseModelUser):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    