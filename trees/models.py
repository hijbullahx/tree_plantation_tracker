from django.db import models

class Tree(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    date_planted = models.DateField()
    image = models.ImageField(upload_to='tree_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.species})"


class HealthLog(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name='health_logs')
    date = models.DateField()
    health_status = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

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
