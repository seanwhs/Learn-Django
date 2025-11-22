# todo app models.py
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from category.models import Category

class Task(models.Model):
    PRIORITY_CHOICES = [('H', 'High'), ('M', 'Medium'), ('L', 'Low')]
    RECURRENCE_CHOICES = [('', 'None'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')]

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    due_date = models.DateField(blank=True, null=True)
    recurrence = models.CharField(max_length=10, choices=RECURRENCE_CHOICES, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.recurrence:  # Recurring tasks
            if self.due_date is not None:
                raise ValidationError({'due_date': "Recurring tasks cannot have a due date."})
            if self.is_done:
                raise ValidationError({'is_done': "Recurring tasks cannot be marked as done."})
        else:  # One-time tasks
            if not self.due_date:
                raise ValidationError({'due_date': "This field is required for one-time tasks."})
            if self.due_date < date.today():
                raise ValidationError({'due_date': "Due date cannot be in the past."})

    def is_overdue(self):
        return (
            self.due_date is not None
            and self.due_date < date.today()
            and not self.is_done
            and not self.recurrence  # recurring tasks never overdue
        )
    
    def __str__(self):
        return self.title
