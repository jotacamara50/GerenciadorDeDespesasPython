# expenses/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User # NOVO: Importe o modelo User
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

# Serializer para Registro de Usuário (COMPLETO E CORRIGIDO)
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}) # Campo para confirmar senha

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email'] # Inclua 'email' se for usar na view
        extra_kwargs = {'password': {'write_only': True}} # Garante que a senha não seja retornada

    # Método de validação customizado para confirmar senhas
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "As senhas não conferem."})
        return data

    # Método para criar o usuário
    def create(self, validated_data):
        # Remove password2 antes de criar o usuário
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user