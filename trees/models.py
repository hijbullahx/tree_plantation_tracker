from django.db import models
from django.utils import timezone

class Tree(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100, blank=True)  # Make species optional
    country = models.CharField(max_length=100, blank=True)
    division = models.CharField(max_length=100, blank=True)  # state/province/region
    district = models.CharField(max_length=100, blank=True)
    other_location = models.CharField(max_length=255, blank=True)  # for uncommon or specific
    location = models.CharField(max_length=255, blank=True)  # full location string for backward compatibility
    latitude = models.FloatField(blank=True, null=True)  # Added for map
    longitude = models.FloatField(blank=True, null=True) # Added for map
    date_planted = models.DateField()
    image = models.ImageField(upload_to='tree_images/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_dead = models.BooleanField(default=False)
    death_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.species})"


class HealthLog(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name='health_logs')
    date = models.DateField()
    health_status = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    is_dead = models.BooleanField(default=False)
    death_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Health on {self.date} - {self.tree.name}"


class Task(models.Model):
    TASK_TYPES = [
        ('Watering', 'Watering'),
        ('Fertilizing', 'Fertilizing'),
        ('Pest Control', 'Pest Control'),
        ('Other', 'Other'),
    ]

    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name='tasks')
    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    scheduled_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task_type} for {self.tree.name} on {self.scheduled_date}"
