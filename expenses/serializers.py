# expenses/serializers.py

from rest_framework import serializers
from .models import Expense, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['user'] # O usuário será definido automaticamente

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'user', 'amount', 'description', 'category', 'category_name', 'date', 'updated_at']
        read_only_fields = ['user'] # O usuário será definido automaticamente