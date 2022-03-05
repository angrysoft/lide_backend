from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Posts(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Tytuł")
    short = models.TextField(blank=True, null=True, verbose_name="Zajawka")
    body = RichTextUploadingField(blank=True, null=True, verbose_name="Treść")
    posted = models.BooleanField(default=False, null=False, verbose_name="Opublikowany")
    edited = models.DateTimeField(
        auto_now=True, editable=False, verbose_name="Edytowany"
    )

    def __str__(self) -> str:
        return f"{self.title} ({self.pk})"

    def serialize_short(self):
        return {
            "id": self.id,
            "title": self.title,
            "short": self.short,
            "edited": self.edited,
        }

    def serialize(self):
        result = self.serialize_short()
        result["body"] = self.body
        return result

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News-y"