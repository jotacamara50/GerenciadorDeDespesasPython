# expenses/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Category, Expense
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class CategoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.tokens = get_tokens_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tokens["access"]}')

    def test_create_category(self):
        url = reverse('category-list')
        data = {'name': 'Alimentação'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'Alimentação')
        self.assertEqual(Category.objects.get().user, self.user)

    def test_list_categories(self):
        Category.objects.create(name='Moradia', user=self.user)
        url = reverse('category-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Moradia')

class ExpenseTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.tokens = get_tokens_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tokens["access"]}')
        self.category = Category.objects.create(name='Transporte', user=self.user)

    def test_create_expense(self):
        url = reverse('expense-list')
        data = {
            'amount': 50.00,
            'description': 'Táxi',
            'category': self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(Expense.objects.get().amount, 50.00)
        self.assertEqual(Expense.objects.get().user, self.user)

    def test_daily_summary(self):
        Expense.objects.create(user=self.user, amount=10.00, description='Café')
        Expense.objects.create(user=self.user, amount=20.00, description='Almoço')
        url = reverse('expense-daily-summary') # 'expense-list' + 'daily_summary'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total_expenses']), 30.00)