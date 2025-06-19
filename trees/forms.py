from django import forms
from .models import Tree, HealthLog, Task

class TreeForm(forms.ModelForm):
    class Meta:
        model = Tree
        fields = ['name', 'species', 'location', 'date_planted', 'image']
        widgets = {
            'date_planted': forms.DateInput(attrs={'type': 'date'})
        }

class HealthLogForm(forms.ModelForm):
    class Meta:
        model = HealthLog
        fields = ['date', 'health_status', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_type', 'scheduled_date', 'completed']
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'})
        }
