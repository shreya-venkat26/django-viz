from django.db import models

# Create your models here.
class Agent(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Dialogue(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.agent.name}: {self.text[:50]}...'