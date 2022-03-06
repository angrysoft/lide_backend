from itertools import chain
from django.db import models


class Settings(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=160)

    def __str__(self) -> str:
        return str(self.name)
