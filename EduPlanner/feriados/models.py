from django.db import models

class Feriado(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    region = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
