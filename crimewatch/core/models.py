# core/models.py

from django.db import models

class CrimeType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип преступления"
        verbose_name_plural = "Типы преступлений"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class CrimeCase(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_occurred = models.DateField()
    location = models.CharField(max_length=200, blank=True)
    is_solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    crime_type = models.ForeignKey(CrimeType, on_delete=models.PROTECT, related_name='cases')
    categories = models.ManyToManyField(Category, related_name='cases')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Дело"
        verbose_name_plural = "Дела"
        ordering = ['-date_occurred']