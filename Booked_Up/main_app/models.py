from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    is_available = models.BooleanField()
    created_at = models.DateField(auto_now_add=True)
    image = models.CharField()

    def __str__(self):
        return f"{self.title} written by  {self.author}"