from typing import Dict, Any
from django.db import models


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
