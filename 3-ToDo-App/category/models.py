# category app models.py
from django.db import models

class Category(models.Model):
    title=models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('title',)

    def __str__(self):
        return self.title
