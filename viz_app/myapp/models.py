from django.db import models

class Document(models.Model):
    name = models.CharField(max_length=255)  # Document name provided by user
    date_uploaded = models.DateTimeField(auto_now_add=True)  # Auto-set the date when uploaded

    def __str__(self):
        return self.name

class Dialogue(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='dialogues')  # Foreign key to Document
    agent = models.CharField(max_length=100)
    text = models.TextField()
    named_entities = models.TextField(blank=True, null=True)
    serial_number = models.IntegerField()

    def __str__(self):
        return f"{self.agent}: {self.text[:50]}"
