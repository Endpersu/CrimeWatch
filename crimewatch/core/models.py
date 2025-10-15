from django.db import models
from django.contrib.auth.models import User


class CrimeType(models.Model):
    name = models.CharField(max_length=100, unique=True)  # "Преступления", "Киберпреступления"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # "Обычное", "Жестокое", "Неразгаданное"

    def __str__(self):
        return self.name


class CrimeCase(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_occurred = models.DateField()
    location = models.CharField(max_length=255, blank=True)
    is_solved = models.BooleanField(default=False)
    crime_type = models.ForeignKey(CrimeType, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title