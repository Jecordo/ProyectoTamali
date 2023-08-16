from django.db import models

# Create your models here.
class persona(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)