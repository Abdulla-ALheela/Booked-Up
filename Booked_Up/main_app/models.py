from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    image = models.TextField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} written by  {self.author}"
    
    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'book_id': self.id})
    
class BorrowCart(models.Model):
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField()

    def __str__(self):
        return f"{self.user} cart"

    def get_absolute_url(self):
        return reverse('cart-detail', kwargs={'cart_id': self.id})
    
class BorrowList(models.Model):
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_at = models.DateField()
    due_date = models.DateField()
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} borrow at {self.borrow_at}"

    def get_absolute_url(self):
        return reverse('cart-detail', kwargs={'cart_id': self.id})