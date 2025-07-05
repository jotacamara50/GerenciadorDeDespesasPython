# expenses/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, CategoryViewSet, UserRegistrationView # Certifique-se de importar UserRegistrationView

# NOVO: Importe as views JWT aqui, pois agora elas estarão neste arquivo
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)), # Inclui as rotas do router (ex: /expenses/, /categories/)

    # NOVO: Adicione o endpoint de registro.
    # Este endpoint será acessível em /gerenciador/api/register/
    path('register/', UserRegistrationView.as_view({'post': 'create'}), name='register-user'),

    # NOVO: Adicione as URLs JWT AQUI!
    # Estes endpoints serão acessíveis em /gerenciador/api/token/ e /gerenciador/api/token/refresh/
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]