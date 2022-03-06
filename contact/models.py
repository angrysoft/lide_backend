from django.db import models


class Message(models.Model):
    iam = models.CharField(max_length=100, verbose_name="Kontakt Jako")
    fname = models.CharField(max_length=100, verbose_name="Imię")
    lname = models.CharField(max_length=100, verbose_name="Nazwisko")
    email = models.EmailField(max_length=100, verbose_name="Mail")
    phone = models.CharField(max_length=100, verbose_name="Telefon")
    msg = models.TextField(verbose_name="Wiadomość")

    class Meta:
        verbose_name = "Wiadomość"
        verbose_name_plural = "Wiadomości"
