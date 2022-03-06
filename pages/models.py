from typing import Any, Dict
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Pages(models.Model):
    slug = models.SlugField(
        max_length=100, unique=True, null=False, verbose_name="Adres strony"
    )
    title = models.CharField(max_length=100, unique=True, verbose_name="Tytuł")
    body = RichTextUploadingField(blank=True, null=True, verbose_name="Treść")
    edited = models.DateTimeField(
        auto_now=True, editable=False, verbose_name="Edytowany"
    )

    def serialize(self) -> Dict[str, Any]:
        return {"title": self.title, "body": self.body, "edited": self.edited}

    class Meta:
        verbose_name = "Strona"
        verbose_name_plural = "Strony"

    def __str__(self) -> str:
        return f"{self.title} ({self.pk})"
