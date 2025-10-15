from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import CrimeCase, Category, CrimeType
from .forms import CrimeCaseForm


class CrimeCaseListView(ListView):
    model = CrimeCase
    template_name = 'core/case_list.html'
    context_object_name = 'cases'
    paginate_by = 10

    def get_queryset(self):
        queryset = CrimeCase.objects.all()
        crime_type = self.request.GET.get('crime_type')
        categories = self.request.GET.getlist('categories')
        is_solved = self.request.GET.get('is_solved')
        search = self.request.GET.get('search')

        if crime_type:
            queryset = queryset.filter(crime_type__id=crime_type)
        if categories:
            queryset = queryset.filter(categories__id__in=categories).distinct()
        if is_solved in ['True', 'False']:
            queryset = queryset.filter(is_solved=(is_solved == 'True'))
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        return queryset.order_by('-date_occurred')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crime_types'] = CrimeType.objects.all()
        context['categories'] = Category.objects.all()
        return context


class CrimeCaseDetailView(DetailView):
    model = CrimeCase
    template_name = 'core/case_detail.html'
    context_object_name = 'case'


class CrimeCaseCreateView(LoginRequiredMixin, CreateView):
    model = CrimeCase
    form_class = CrimeCaseForm
    template_name = 'core/case_form.html'
    success_url = reverse_lazy('case_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CrimeCaseUpdateView(LoginRequiredMixin, UpdateView):
    model = CrimeCase
    form_class = CrimeCaseForm
    template_name = 'core/case_form.html'
    success_url = reverse_lazy('case_list')


class CrimeCaseDeleteView(LoginRequiredMixin, DeleteView):
    model = CrimeCase
    template_name = 'core/case_confirm_delete.html'
    success_url = reverse_lazy('case_list')