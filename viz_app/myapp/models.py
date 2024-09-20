from django.db import models

# Create your models here.
class Agent(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Dialogue(models.Model):
    agent = Agent
    serial_number = models.IntegerField(default=0)
    text = models.TextField()
    timestamp = models.DateTimeField(default=None)
    proper_nouns = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Speech {self.serial_number}"