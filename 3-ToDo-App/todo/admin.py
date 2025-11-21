# todo app admin.py
from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'due_date','is_done', 'recurrence','created_at', 'updated_at', )
    list_filter = ('category', 'is_done',)
    search_fields = ('title', 'description',)
    ordering = ('updated_at',)

admin.site.register(Task, TaskAdmin)
