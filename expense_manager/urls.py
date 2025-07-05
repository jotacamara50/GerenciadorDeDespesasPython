# expense_manager/urls.py
from django.contrib import admin
from django.urls import path, include
from expenses.views import home

urlpatterns = [
    # Admin agora acessível em /gerenciador/admin/
    path('admin/', admin.site.urls),

    # Home Page agora acessível em /gerenciador/
    path('', home, name='home'),

    # API agora acessível em /gerenciador/api/
    path('api/', include('expenses.urls')),
]