# category app models.py
from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def clean(self):
        # Normalize title
        self.title = self.title.strip().title()
        if Category.objects.exclude(id=self.id).filter(title__iexact=self.title).exists():
            raise ValidationError({'title': 'Category already exists.'})

    def __str__(self):
        return self.title
