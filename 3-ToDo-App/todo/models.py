from os import name
from django.db import models

class Todo(models.Model):
    name = models.CharField(max_length=255)
    due_date = models.DateField()

    def __str__(self):
        return self.name