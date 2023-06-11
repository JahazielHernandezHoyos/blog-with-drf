from django.db import models
from django_lifecycle import AFTER_CREATE, BEFORE_UPDATE, hook

from apps.utils.models import BaseModel, BaseModelUser, BaseNameDescriptionModel


class Account(BaseModelUser):
    """
    Account all models fields (account roles: admin, editor, blogger)
    """

    biography = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures", blank=True, null=True
    )

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    @hook(AFTER_CREATE)
    def on_create(self):
        self.set_raw_password()

    @hook(BEFORE_UPDATE)
    def on_update(self):
        self.set_raw_password()


class HistoricalPurchase(BaseNameDescriptionModel):
    message = models.CharField(max_length=128)
    user = models.ForeignKey("accounts.Account", on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Punto usuario"
        verbose_name_plural = "Puntos usuarios"


class Comments(BaseModel):
    """
    Comments with relations to users and entraces
    """

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    entrace = models.ForeignKey("Entrace", on_delete=models.CASCADE)
    comment = models.TextField()
    likes = models.ManyToManyField(Account, related_name="comment_likes", blank=True)

    def __str__(self):
        return self.comment


class Entrace(BaseModel):
    """
    Entrace with relations to likes, comments and users
    """

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to="entraces")
    likes = models.ManyToManyField(Account, related_name="likes", blank=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tags", blank=True)

    def __str__(self):
        return self.title


class Category(BaseNameDescriptionModel):
    """
    Category with relations to entraces
    """

    def __str__(self):
        return self.name


class Tags(BaseNameDescriptionModel):
    """
    Tags with relations to entraces
    """

    def __str__(self):
        return self.name
