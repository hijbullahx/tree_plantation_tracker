from django.contrib import admin
from .models import Tree, HealthLog, Task

@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'location', 'date_planted')

@admin.register(HealthLog)
class HealthLogAdmin(admin.ModelAdmin):
    list_display = ('tree', 'date', 'health_status')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('tree', 'task_type', 'scheduled_date', 'completed')
    list_filter = ('task_type', 'completed')
