# expenses/models.py

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ('name', 'user') # Garante que um usuário não tenha duas categorias com o mesmo nome

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    date = models.DateField(auto_now_add=True) # Data da criação do registro
    updated_at = models.DateTimeField(auto_now=True) # Data da última atualização

    class Meta:
        ordering = ['-date', '-updated_at'] # Ordena por data (mais recente primeiro) e depois por atualização

    def __str__(self):
        return f"R$ {self.amount} - {self.description} ({self.date})"