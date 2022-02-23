from typing import Any, Dict
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Positions(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Nazwa Stanowiska"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Stanowisko"
        verbose_name_plural = "Stanowiska"


class Locations(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Miejsce Pracy")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Lokalizacja"
        verbose_name_plural = "Lokalizacje"


class EmploymentType(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Forma Zatrudnienia"
        verbose_name_plural = "Formy Zatrudnienia"


class Offers(models.Model):
    position = models.ForeignKey(
        Positions, on_delete=models.PROTECT, verbose_name="Stanowisko"
    )
    location = models.ManyToManyField(Locations, verbose_name="Lokalizacja")
    employment_type = models.ManyToManyField(
        EmploymentType, verbose_name="Forma zatrudnienia"
    )
    details = RichTextUploadingField(blank=True, null=True, verbose_name="Szczegóły")
    posted = models.BooleanField(default=False, null=False, verbose_name="Opublikowany")
    edited = models.DateTimeField(
        auto_now=True, auto_created=True, editable=False, verbose_name="Edytowany"
    )

    def serialize_short(self):
        return {
            "id": self.id,
            "position": self.position.name,
            "location": [location.name for location in self.location.all()],
            "employmentType": [
                emplType.name for emplType in self.employment_type.all()
            ],
            "edited": self.edited,
        }

    def serialize(self) -> Dict[str, Any]:
        result = self.serialize_short()
        result["details"] = self.details
        return result

    def __str__(self) -> str:
        return f"Oferta Pracy: {self.position} ({self.pk}) "

    class Meta:
        verbose_name = "Oferta Pracy"
        verbose_name_plural = "Oferty Pracy"


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


class Contacts(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nazwa kontaktu")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    mail = models.EmailField(verbose_name="Email")

    def __str__(self) -> str:
        return str(self.name)

    def serialize(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "mail": self.mail,
        }

    class Meta:
        verbose_name = "Kontakt"
        verbose_name_plural = "Kontakty"
