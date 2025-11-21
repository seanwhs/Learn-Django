# todo forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['category', 'title', 'description', 'priority', 'due_date', 'recurrence', 'is_done']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
