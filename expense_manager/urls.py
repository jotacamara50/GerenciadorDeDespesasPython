# expense_manager/urls.py

from django.contrib import admin
from django.urls import path, include
from expenses.views import home # Importe a view home do seu app 'expenses'
from rest_framework_simplejwt.views import ( # Importe as views do simplejwt
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # URLs do Admin
    path('gerenciador/admin/', admin.site.urls),

    # URL para a Home Page do seu projeto Django (que está no app 'expenses')
    # Esta é a página de login/registro
    path('gerenciador/', home, name='home'),

    # URLs da API (DRF) - incluindo as do seu app 'expenses'
    path('gerenciador/api/', include('expenses.urls')),

    # URLs para autenticação JWT (simplejwt)
    path('gerenciador/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('gerenciador/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Se você tiver outras URLs de apps no futuro, adicione-as aqui
    # Exemplo: path('gerenciador/outros_dados/', include('meu_outro_app.urls')),
]

# Nota: O bloco 'if settings.DEBUG: urlpatterns += static(...)' não é necessário aqui
# pois o Nginx cuidará dos arquivos estáticos em produção. Mantenha ele se quiser para
# desenvolvimento local, mas remova-o para o arquivo final de produção se preferir
# manter as URLs mais limpas para o deploy.
# Por enquanto, vou omitir para o deploy, pois o Nginx vai gerenciar os estáticos.