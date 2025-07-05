# expenses/views.py
from django.shortcuts import render
from django.http import HttpResponse # Adicione esta importação

def home(request):
    # Linha de log para depuração
    print(f"DEBUG: A view 'home' foi chamada com o path: {request.path}")
    
    # A linha abaixo vai retornar um texto simples em vez da sua página
    return HttpResponse(f"A view HOME foi chamada com o path: {request.path}. Verifique seus logs do Gunicorn.", status=200)

# Deixe o resto do seu arquivo views.py como estava
# ...