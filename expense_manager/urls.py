# expense_manager/urls.py
from django.contrib import admin
from django.urls import path, include
from expenses.views import home
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Admin
    path('admin/login/', admin.site.urls), # Login do admin
    path('admin/', admin.site.urls), # Acesso completo ao admin

    # Home Page do seu projeto
    path('', home, name='home'),

    # API (DRF)
    path('api/', include('expenses.urls')),

    # Autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]