from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CrimeCase, Category, CrimeType

class CrimeCaseModelTest(TestCase):
    def setUp(self):
        self.crime_type = CrimeType.objects.create(name="Преступления")
        self.category = Category.objects.create(name="Жестокое")
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_crime_case(self):
        case = CrimeCase.objects.create(
            title="Тестовое дело",
            description="Описание",
            date_occurred="2023-01-01",
            crime_type=self.crime_type,
            created_by=self.user
        )
        case.categories.add(self.category)
        self.assertEqual(case.title, "Тестовое дело")
        self.assertIn(self.category, case.categories.all())

class CategoryModelTest(TestCase):
    def test_unique_name(self):
        Category.objects.create(name="Обычное")
        with self.assertRaises(Exception):
            Category.objects.create(name="Обычное")

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.crime_type = CrimeType.objects.create(name="Преступления")
        self.case = CrimeCase.objects.create(
            title="Тест",
            description="Тестовое описание",
            date_occurred="2023-01-01",
            crime_type=self.crime_type
        )

    def test_case_list_view(self):
        response = self.client.get(reverse('case_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('cases', response.context)
        self.assertTrue(response.context['page_obj'])

    def test_filter_by_category(self):
        category = Category.objects.create(name="Неразгаданное")
        self.case.categories.add(category)
        response = self.client.get(reverse('case_list') + f'?categories={category.id}')
        self.assertEqual(len(response.context['cases']), 1)

    def test_search_by_title(self):
        response = self.client.get(reverse('case_list') + '?search=Тест')
        self.assertContains(response, "Тестовое дело")