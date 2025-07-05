# expenses/views.py

# --- IMPORTS ORIGINAIS E NECESSÁRIOS ---
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import date, timedelta
from django.http import HttpResponse # Import para o nosso debug

from .models import Expense, Category
from .serializers import ExpenseSerializer, CategorySerializer, UserRegistrationSerializer

# --- VIEW 'HOME' MODIFICADA PARA DEBUG ---
# Esta view agora nos ajudará a diagnosticar o problema de roteamento.
def home(request):
    print(f"DEBUG: A view 'home' foi chamada com o path: {request.path}")
    return HttpResponse(f"A view HOME foi chamada com o path: {request.path}. Verifique seus logs do Gunicorn.", status=200)


# --- SUAS CLASSES DE API ORIGINAIS RESTAURADAS ---
# O erro 'ImportError' aconteceu porque estas classes estavam faltando.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def daily_summary(self, request):
        today = date.today()
        expenses_today = self.get_queryset().filter(date=today)
        total_today = expenses_today.aggregate(Sum('amount'))['amount__sum'] or 0.00
        return Response({'date': today, 'total_expenses': total_today})

    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        current_month = date.today().month
        current_year = date.today().year

        monthly_expenses = self.get_queryset().filter(
            date__month=current_month,
            date__year=current_year
        ).values('category__name').annotate(total=Sum('amount'))

        return Response(monthly_expenses)


class UserRegistrationView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Usuário registrado com sucesso!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)