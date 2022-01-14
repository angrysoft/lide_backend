from django.db import models

class Positions(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nazwa Stanowiska")
    

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Stanowisko'
        verbose_name_plural = 'Stanowiska'


class Locations(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Miejsce Pracy")

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Lokalizacja"
        verbose_name_plural = 'Lokalizacje'


class EmploymentType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Forma Zatrudnienia'
        verbose_name_plural = 'Formay Zatrudnienia'


class Offers(models.Model):
    position = models.OneToOneField(Positions, on_delete=models.PROTECT)
    location = models.ManyToManyField(Locations)
    employment_type = models.ManyToManyField(EmploymentType)
    details = models.TextField(blank=True, null=True, verbose_name='Szczegóły')
    posted = models.BooleanField(default=False, null=False)
    post_date = models.DateTimeField(auto_created=True, editable=True) 
    edited = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = "Oferta Pracy"
        verbose_name_plural = 'Oferty Pracy'


class Posts(models.Model):
    title = models.CharField(max_length=100, unique=True)
    body = models.TextField()
    posted = models.BooleanField(default=False, null=False)
    post_date = models.DateTimeField(auto_created=True, auto_now=True, editable=False) 
    edited = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = 'News-y'

