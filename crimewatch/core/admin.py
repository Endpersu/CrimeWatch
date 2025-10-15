from django.contrib import admin
from .models import CrimeType, Category, CrimeCase


@admin.register(CrimeType)
class CrimeTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(CrimeCase)
class CrimeCaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'crime_type', 'is_solved', 'date_occurred', 'created_by')
    list_filter = ('crime_type', 'is_solved', 'categories', 'date_occurred')
    search_fields = ('title', 'description', 'location')
    filter_horizontal = ('categories',)
    readonly_fields = ('created_at', 'updated_at')