from django.db import models
from django.urls import reverse

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    is_available = models.BooleanField()
    created_at = models.DateField(auto_now_add=True)
    image = models.TextField()

    def __str__(self):
        return f"{self.title} written by  {self.author}"
    
    def get_absolute_url(self):

        return reverse('book-detail', kwargs={'book_id': self.id})