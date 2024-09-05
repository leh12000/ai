from django.db import models

from level.models import Level
from category.models import Category

class Book(models.Model):

    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,)
    level=models.ForeignKey(Level,on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    description = models.TextField()
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    coverPrompt=models.TextField()
    def __str__(self):
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    content = models.TextField()
    promptDescription = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f"Chapter: {self.title} - Book: {self.book.title}"

# Create your models here.

