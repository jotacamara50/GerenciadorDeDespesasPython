# expense_manager/urls.py

from django.contrib import admin
from django.urls import path, include
from expenses.views import home
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Admin (acessível em /gerenciador/admin/) - AGORA COM O PREFIXO
    path('gerenciador/admin/login/', admin.site.urls),
    path('gerenciador/admin/', admin.site.urls),

    # Home Page (acessível em /gerenciador/) - AGORA COM O PREFIXO
    path('gerenciador/', home, name='home'),

    # API (DRF) (acessível em /gerenciador/api/) - AGORA COM O PREFIXO
    path('gerenciador/api/', include('expenses.urls')), # Inclui as URLs da sua app expenses

    # Autenticação JWT (acessível em /gerenciador/api/token/) - AGORA COM O PREFIXO
    path('gerenciador/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('gerenciador/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]