# core/views.py

from django.shortcuts import render
from django.views.generic import ListView
from django.db import models
from .models import CrimeCase
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth import logout


def secret_deltarune_view(request):
    return render(request, 'secret_deltarune.html')


def custom_logout_view(request):
    logout(request)  # Удаляем сессию
    return redirect('/')  # Перенаправляем на главную (через GET)


def home_view(request):
    """Главная страница сайта — баннер с кнопками."""
    return render(request, 'home.html')


def about_view(request):
    """Страница 'О проекте'"""
    return render(request, 'about.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


class CrimeCaseListView(ListView):
    model = CrimeCase
    template_name = 'case_list.html'
    context_object_name = 'cases'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        crime_type_id = self.request.GET.get('crime_type')
        category_ids = self.request.GET.getlist('categories')
        is_solved = self.request.GET.get('is_solved')
        search = self.request.GET.get('q')

        if crime_type_id:
            queryset = queryset.filter(crime_type_id=crime_type_id)
        if category_ids:
            queryset = queryset.filter(categories__id__in=category_ids).distinct()
        if is_solved is not None:
            queryset = queryset.filter(is_solved=(is_solved == '1'))
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(description__icontains=search)
            )

        return queryset.order_by('-date_occurred')