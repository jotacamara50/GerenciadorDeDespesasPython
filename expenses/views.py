# expenses/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Expense, Category
from .serializers import ExpenseSerializer, CategorySerializer
from django.db.models import Sum
from datetime import date, timedelta

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retorna as categorias pertencentes ao usuário logado.
        """
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Associa a categoria ao usuário logado na criação.
        """
        serializer.save(user=self.request.user)

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retorna as despesas pertencentes ao usuário logado.
        """
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Associa a despesa ao usuário logado na criação.
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def daily_summary(self, request):
        """
        Retorna o resumo diário de despesas para o usuário logado.
        """
        today = date.today()
        expenses_today = self.get_queryset().filter(date=today)
        total_today = expenses_today.aggregate(Sum('amount'))['amount__sum'] or 0.00
        return Response({'date': today, 'total_expenses': total_today})

    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        """
        Retorna o resumo mensal de despesas por categoria para o usuário logado.
        """
        current_month = date.today().month
        current_year = date.today().year

        monthly_expenses = self.get_queryset().filter(
            date__month=current_month,
            date__year=current_year
        ).values('category__name').annotate(total=Sum('amount'))

        return Response(monthly_expenses)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'expenses/index.html')